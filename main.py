import sys
from modules import tts, listener, stt, brain, wake_word
from modules.ui import (
    console,
    show_banner,
    show_system_info,
    show_initializing,
    show_online,
    show_wake_waiting,
    show_wake_detected,
    show_listening,
    show_transcribing,
    show_thinking,
    show_user_message,
    show_jarvis_message,
    show_no_input,
    show_error,
    show_separator,
    show_shutdown,
)


def run_pipeline(engine):
    show_wake_detected()

    with show_listening():
        audio = listener.record_audio()

    with show_transcribing():
        text = stt.transcribe(audio)

    if not text:
        show_no_input()
        tts.speak("I didn't catch that. Could you repeat?", engine)
        return

    show_user_message(text)

    with show_thinking():
        reply = brain.think(text)

    show_jarvis_message(reply)
    tts.speak(reply, engine)
    show_separator()


def main():
    show_banner()
    show_system_info()

    with show_initializing("Loading TTS engine..."):
        engine = tts.create_engine()

    with show_initializing("Loading Whisper model..."):
        stt.load_model()

    with show_initializing("Loading wake word model..."):
        model = wake_word.load_model()

    show_online()
    tts.speak("JARVIS online. Say 'Hey JARVIS' to begin.", engine)

    while True:
        try:
            with show_wake_waiting():
                wake_word.listen_for_wake_word(model)
            run_pipeline(engine)
        except KeyboardInterrupt:
            show_shutdown()
            tts.speak("Goodbye.", engine)
            sys.exit(0)
        except Exception as e:
            show_error(str(e))
            show_separator()


if __name__ == "__main__":
    main()
