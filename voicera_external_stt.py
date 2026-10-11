
import argparse
import os
import sounddevice as sd
import wave
import numpy as np
from faster_whisper import WhisperModel


RATE = 16000
DURATION = 8


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--language",
        default=None
    )

    parser.add_argument(
        "--auto-detect",
        action="store_true"
    )

    args = parser.parse_args()

    print(
        "VOICERA STT READY",
        flush=True
    )

    model = WhisperModel(
        "small",
        device="cpu",
        compute_type="int8"
    )

    print(
        "🎤 Listening...",
        flush=True
    )

    audio = sd.rec(
        int(RATE * DURATION),
        samplerate=RATE,
        channels=1,
        dtype="int16",
        device=0
    )

    sd.wait()

    samples = audio.astype(
        "float32"
    ).flatten()

    # Remove DC offset.
    samples = samples - float(
        np.mean(samples)
    )

    peak = float(
        np.max(np.abs(samples))
    ) if len(samples) else 0.0

    rms = float(
        np.sqrt(
            np.mean(samples * samples)
        )
    ) if len(samples) else 0.0

    if peak < 500 or rms < 35:

        print(
            "NO_SPEECH",
            flush=True
        )

        return

    # Keep the same successful weak-audio compensation.
    if peak < 12000:

        gain = min(
            6.0,
            18000.0 / max(peak, 1.0)
        )

        samples = samples * gain

    samples = samples.clip(
        -32768,
        32767
    )

    audio = samples.astype(
        "int16"
    ).reshape(
        (-1, 1)
    )

    wav_path = os.path.join(
        os.path.dirname(
            os.path.abspath(__file__)
        ),
        "voicera_input.wav"
    )

    with wave.open(
        wav_path,
        "wb"
    ) as wf:

        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(RATE)
        wf.writeframes(
            audio.tobytes()
        )

    print(
        "Processing speech...",
        flush=True
    )

    source_language = None

    if not args.auto_detect:
        source_language = args.language

    segments, info = model.transcribe(
        wav_path,
        beam_size=5,
        vad_filter=False,
        language=source_language,
        temperature=0,
        condition_on_previous_text=False,
        no_speech_threshold=0.6,
        compression_ratio_threshold=2.4,
        log_prob_threshold=-1.0
    )

    text = " ".join(
        segment.text.strip()
        for segment in segments
        if segment.text.strip()
    ).strip()

    print(
        "LANGUAGE:",
        info.language,
        flush=True
    )

    if text:

        print(
            ">>>",
            text,
            flush=True
        )

    else:

        print(
            "NO_SPEECH",
            flush=True
        )

    try:
        os.remove(wav_path)
    except Exception:
        pass


if __name__ == "__main__":
    main()
