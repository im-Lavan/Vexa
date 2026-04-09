import pyttsx3
import config


def create_engine():
    engine = pyttsx3.init()
    engine.setProperty("rate", config.TTS_RATE)
    engine.setProperty("volume", config.TTS_VOLUME)
    return engine


def speak(text, engine=None):
    if engine is None:
        engine = create_engine()
    engine.say(text)
    engine.runAndWait()
