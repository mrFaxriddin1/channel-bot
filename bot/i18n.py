import json
from pathlib import Path

LOCALES_DIR = Path(__file__).parent / "locales"
DEFAULT_LANG = "uz"
SUPPORTED_LANGS = ("uz", "en", "ru")


def _load_translations() -> dict[str, dict[str, str]]:
    translations = {}
    for lang in SUPPORTED_LANGS:
        path = LOCALES_DIR / f"{lang}.json"
        with open(path, encoding="utf-8") as f:
            translations[lang] = json.load(f)
    return translations


TRANSLATIONS = _load_translations()


def t(key: str, lang: str = DEFAULT_LANG, **kwargs) -> str:
    text = TRANSLATIONS.get(lang, {}).get(key)
    if text is None:
        text = TRANSLATIONS[DEFAULT_LANG].get(key, key)
    return text.format(**kwargs)
