import requests
from datetime import datetime


_location_cache = None


def fetch_location():
    global _location_cache
    try:
        resp = requests.get("http://ip-api.com/json/", timeout=4)
        data = resp.json()
        parts = [data.get("city", ""), data.get("regionName", ""), data.get("country", "")]
        _location_cache = ", ".join(p for p in parts if p) or "unknown location"
    except Exception:
        _location_cache = "unknown location"
    return _location_cache


def get_location():
    return _location_cache or "unknown location"


def get_datetime_str():
    now = datetime.now()
    return now.strftime("%A, %B %d %Y at %I:%M %p")
