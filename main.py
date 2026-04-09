import sys
import time
from modules import tts, listener, stt, brain, wake_word
from modules import context as ctx
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
    show_conversation_mode,
    show_returning_to_standby,
    show_no_input,
    show_error,
    show_separator,
    show_shutdown,
)
import config

EXIT_PHRASES = {"goodbye", "bye", "stop", "exit", "shut down", "shutdown", "go to sleep"}


def conversation_loop(engine):
    misses = 0

    while misses < config.CONVERSATION_MAX_MISSES:
        with show_listening():
            audio = listener.record_audio()

        with show_transcribing():
            text = stt.transcribe(audio)

        if not text:
            misses += 1
            show_no_input()
            show_conversation_mode(misses, config.CONVERSATION_MAX_MISSES)
            if misses < config.CONVERSATION_MAX_MISSES:
                tts.speak("I didn't catch that.", engine)
            continue

        misses = 0
        show_user_message(text)

        if any(phrase in text.lower() for phrase in EXIT_PHRASES):
            reply = "Understood. Going back to standby mode."
            show_jarvis_message(reply)
            tts.speak(reply, engine)
            break

        with show_thinking():
            reply = brain.think(text)

        show_jarvis_message(reply)
        tts.speak(reply, engine)
        time.sleep(config.POST_TTS_DELAY)

    show_returning_to_standby()
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

    with show_initializing("Fetching location..."):
        ctx.fetch_location()

    show_online()
    tts.speak("JARVIS online. Say 'Hey JARVIS' to begin.", engine)

    while True:
        try:
            with show_wake_waiting():
                wake_word.listen_for_wake_word(model)
            show_wake_detected()
            conversation_loop(engine)
        except KeyboardInterrupt:
            show_shutdown()
            tts.speak("Goodbye.", engine)
            sys.exit(0)
        except Exception as e:
            show_error(str(e))
            show_separator()


if __name__ == "__main__":
    main()
