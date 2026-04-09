import numpy as np
import sounddevice as sd
from openwakeword.model import Model
import config

CHUNK_SIZE = 1280


def load_model():
    return Model(wakeword_models=[config.WAKE_WORD_MODEL], inference_framework="onnx")


def listen_for_wake_word(model):
    detected = False

    def callback(indata, frames, time, status):
        nonlocal detected
        if detected:
            return

        audio_chunk = indata.flatten().astype(np.int16)
        model.predict(audio_chunk)

        scores = model.prediction_buffer.get(config.WAKE_WORD_MODEL, [])
        if len(scores) > 0 and scores[-1] >= 0.5:
            detected = True
            raise sd.CallbackStop

    with sd.InputStream(
        samplerate=config.SAMPLE_RATE,
        channels=1,
        dtype="int16",
        blocksize=CHUNK_SIZE,
        callback=callback,
    ):
        try:
            while not detected:
                sd.sleep(100)
        except sd.CallbackStop:
            pass
