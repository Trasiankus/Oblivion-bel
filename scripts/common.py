"""Агульныя функцыі для extract.py / apply.py / validate.py."""
import json
import re

FIELDS = ["key", "en", "ru", "bel", "bel_alt", "pl"]

# Тэгі / плэйсхолдэры, якія павінны супадаць паміж en і custom.
TAG_RE = re.compile(r"\{[^{}]*\}|<[^<>]*>")

# ICU-канструкцыі кшталту {Count}|plural(one=...,other=...) або
# |ordinal(one=st,two=nd,...). Ключавыя словы (plural/ordinal/one/few/...)
# застаюцца лацінкай заўсёды - гэта сінтаксіс, не тэкст для перакладу.
# Для беларускай мовы дазволена ДАДАВАЦЬ формы (one/few/many/other), таму
# змесціва дужак у en і custom могуць адрознівацца - параўноўваем толькі
# наяўнасць самой канструкцыі (plural/ordinal), не яе змесціва.
ICU_RE = re.compile(r"\|(?:plural|ordinal|selectordinal)\([^()]*\)")


def strip_icu(text):
    return ICU_RE.sub("", text or "")

# Рэгулярка для пошуку блока "key": "...",\n    "custom": "..."
ENTRY_RE = re.compile(
    r'"key"\s*:\s*"((?:[^"\\]|\\.)*)"'
    r'\s*,\s*\n\s*'
    r'"custom"\s*:\s*"((?:[^"\\]|\\.)*)"'
)


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def read_raw(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def json_str_escape(s):
    # json.dumps дае "текст" - прыбіраем знешнія двукоссі
    return json.dumps(s, ensure_ascii=False)[1:-1]


def json_str_unescape(s):
    return json.loads('"' + s + '"')


def is_empty_custom(entry):
    return not entry.get("custom")


def extract_tags(text):
    return TAG_RE.findall(text or "")
