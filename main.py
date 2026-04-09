import sys
from modules import tts, listener, stt, brain, wake_word


def run_pipeline(engine):
    print("Listening...")
    audio = listener.record_audio()

    print("Transcribing...")
    text = stt.transcribe(audio)
    print(f"You: {text}")

    if not text:
        tts.speak("I didn't catch that. Could you repeat?", engine)
        return

    print("Thinking...")
    reply = brain.think(text)
    print(f"JARVIS: {reply}")

    tts.speak(reply, engine)


def main():
    print("Initializing JARVIS...")
    engine = tts.create_engine()
    model = wake_word.load_model()

    tts.speak("JARVIS online. Say 'Hey JARVIS' to begin.", engine)

    while True:
        print("Waiting for wake word...")
        try:
            wake_word.listen_for_wake_word(model, lambda: run_pipeline(engine))
        except KeyboardInterrupt:
            print("\nShutting down.")
            tts.speak("Goodbye.", engine)
            sys.exit(0)


if __name__ == "__main__":
    main()
