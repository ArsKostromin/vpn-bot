import json
from pathlib import Path

LOCALE = "ru"
BASE_DIR = Path(__file__).resolve().parent
TEXTS_FILE = BASE_DIR / f"{LOCALE}.json"

with open(TEXTS_FILE, "r", encoding="utf-8") as f:
    _texts = json.load(f)

def get_text(key: str, **kwargs) -> str:
    text = _texts.get(key, "")
    return text.format(**kwargs)
