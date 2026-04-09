from groq import Groq
import config
from modules.context import get_location, get_datetime_str

_client = None
_history = []


def get_client():
    global _client
    if _client is None:
        _client = Groq(api_key=config.GROQ_API_KEY)
    return _client


def _build_system_message():
    context = (
        f"Current date and time: {get_datetime_str()}. "
        f"User's location: {get_location()}."
    )
    return f"{config.JARVIS_SYSTEM_PROMPT} {context}"


def think(user_input):
    client = get_client()

    _history.append({"role": "user", "content": user_input})

    messages = [{"role": "system", "content": _build_system_message()}] + _history

    response = client.chat.completions.create(
        model=config.GROQ_MODEL,
        messages=messages,
    )

    reply = response.choices[0].message.content.strip()
    _history.append({"role": "assistant", "content": reply})

    return reply


def reset_history():
    global _history
    _history = []
