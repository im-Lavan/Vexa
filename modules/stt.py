import whisper
import config

_model = None


def load_model():
    global _model
    if _model is None:
        _model = whisper.load_model(config.WHISPER_MODEL)
    return _model


def transcribe(audio):
    model = load_model()
    result = model.transcribe(audio, fp16=False)
    return result["text"].strip()
