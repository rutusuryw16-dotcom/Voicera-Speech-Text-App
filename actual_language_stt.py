import sounddevice as sd
import wave
import os
from faster_whisper import WhisperModel

RATE = 16000
DURATION = 8

print("LOADING MULTILINGUAL WHISPER...", flush=True)

model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)

print("MULTILINGUAL STT READY", flush=True)


def record_audio():

    print("🎤 Listening...", flush=True)

    audio = sd.rec(
        int(DURATION * RATE),
        samplerate=RATE,
        channels=1,
        dtype="int16",
        device=0
    )

    sd.wait()

    return audio


def save_wav(audio):

    path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "speech_input.wav"
    )

    with wave.open(path, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(RATE)
        wf.writeframes(audio.tobytes())

    return path


def recognize(audio):

    wav_path = save_wav(audio)

    segments, info = model.transcribe(
        wav_path,
        beam_size=5,
        vad_filter=False
    )

    text = " ".join(
        segment.text.strip()
        for segment in segments
        if segment.text.strip()
    ).strip()

    if text:

        print(
            "LANGUAGE:",
            info.language,
            flush=True
        )

        print(
            ">>>",
            text,
            flush=True
        )


while True:

    try:

        audio = record_audio()

        print("Processing...", flush=True)

        recognize(audio)

        print("Listening...", flush=True)

    except KeyboardInterrupt:

        print("Stopping...", flush=True)
        break

    except Exception as error:

        print(
            "Error:",
            error,
            flush=True
        )

        break
