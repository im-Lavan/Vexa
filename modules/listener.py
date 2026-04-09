import numpy as np
import sounddevice as sd
import config


def record_audio():
    frames = int(config.SAMPLE_RATE * config.RECORD_SECONDS)
    audio = sd.rec(frames, samplerate=config.SAMPLE_RATE, channels=1, dtype="float32")
    sd.wait()
    return audio.flatten()


def audio_to_float32(audio):
    return audio.astype(np.float32)
