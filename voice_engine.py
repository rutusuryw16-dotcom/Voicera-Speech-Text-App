import os
import sys
import subprocess
import tempfile
import asyncio


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ============================================================
# SPEECH TO TEXT
# ============================================================

def speech_to_text(language_code=None):
    """
    Uses the existing tested VOICERA external STT engine.
    Returns recognized text.
    """

    backend_file = os.path.join(
        BASE_DIR,
        "backend",
        "voicera_external_stt.py"
    )

    python_executable = sys.executable

    try:
        result = subprocess.run(
            [
                python_executable,
                backend_file
            ],
            capture_output=True,
            text=True,
            timeout=120
        )

        output = result.stdout.strip()

        if result.returncode != 0:
            error = result.stderr.strip()

            return {
                "success": False,
                "text": "",
                "error": error or "Speech recognition failed."
            }

        text = ""

        for line in output.splitlines():
            line = line.strip()

            if line.startswith(">>>"):
                text = line[3:].strip()
                break

        if not text:
            return {
                "success": False,
                "text": "",
                "error": "No speech detected."
            }

        return {
            "success": True,
            "text": text,
            "error": ""
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "text": "",
            "error": "Speech recognition timed out."
        }

    except Exception as e:
        return {
            "success": False,
            "text": "",
            "error": str(e)
        }


# ============================================================
# TEXT TO SPEECH
# ============================================================

TTS_VOICES = {
    "English": "en-US-AriaNeural",
    "Hindi": "hi-IN-SwaraNeural",
    "Marathi": "mr-IN-AarohiNeural",
    "Gujarati": "gu-IN-DhwaniNeural",
    "Bengali": "bn-IN-TanishaaNeural",
    "Tamil": "ta-IN-PallaviNeural",
    "Telugu": "te-IN-ShrutiNeural",
    "Kannada": "kn-IN-SapnaNeural",
    "Malayalam": "ml-IN-SobhanaNeural",
    "Punjabi": "pa-IN-VaaniNeural"
}


async def _generate_speech(text, voice, output_file):
    import edge_tts

    communicator = edge_tts.Communicate(
        text,
        voice
    )

    await communicator.save(output_file)


def text_to_speech(text, language="English"):
    """
    Converts text into speech using Edge TTS.
    """

    text = text.strip()

    if not text:
        return {
            "success": False,
            "file": "",
            "error": "Please enter some text."
        }

    voice = TTS_VOICES.get(
        language,
        TTS_VOICES["English"]
    )

    output_file = os.path.join(
        tempfile.gettempdir(),
        "voicera_output.mp3"
    )

    try:
        asyncio.run(
            _generate_speech(
                text,
                voice,
                output_file
            )
        )

        return {
            "success": True,
            "file": output_file,
            "voice": voice,
            "error": ""
        }

    except Exception as e:
        return {
            "success": False,
            "file": "",
            "voice": voice,
            "error": str(e)
        }


# ============================================================
# ENGINE INFORMATION
# ============================================================

def get_tts_voice(language):
    return TTS_VOICES.get(
        language,
        TTS_VOICES["English"]
    )


def get_supported_tts_languages():
    return list(TTS_VOICES.keys())
