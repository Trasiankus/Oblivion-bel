#!/usr/bin/env python3
"""validate.py [FILES...]

Правярае файлы (па змоўчанні - усе вядомыя):
- JSON валідны;
- ключы і парадак запісаў не змяніліся, змянілася толькі "custom"
  (параўнанне з git show HEAD:файл);
- тэгі/плэйсхолдэры ў custom супадаюць з en (колькасць і назвы);
- няма рускіх літар и/щ/ъ і лацінкі па-за тэгамі (акрамя custom == en);
- прабелы ў пачатку/канцы і канцавы знак прыпынку адпавядаюць en.

Вывад: справаздача па кожным файле + агульная колькасць памылак.
Exit code 0 калі памылак няма, інакш 1.
"""
import json
import subprocess
import sys
from collections import Counter

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from common import load, extract_tags, ICU_RE, strip_icu

DEFAULT_FILES = [
    "same_bel_belalt_case_insensitive.json",
    "different_bel_belalt_case_insensitive.json",
    "ST_AltarDynamicTexts.json",
    "ST_AltarStaticTexts.json",
    "ST_HardcodedContent.json",
    "ST_MissingEntries.json",
    "ST_ResponseTexts.json",
    "ST_ScriptContent.json",
    "ST_LogEntries.json",
    "ST_BookContent.json",
    "ST_Descriptions.json",
]

RU_ONLY_LETTERS = set("иИщЩъЪ")
LATIN_RE_CHARS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")


def get_head_version(path):
    try:
        out = subprocess.run(
            ["git", "show", f"HEAD:{path}"],
            capture_output=True, check=True, cwd=None,
        )
        return json.loads(out.stdout.decode("utf-8"))
    except (subprocess.CalledProcessError, json.JSONDecodeError):
        return None


def remove_tags(text):
    import re
    from common import TAG_RE
    return TAG_RE.sub("", text)


def check_letters(custom, en, key, errors):
    if custom == en:
        return  # тэхнічны ID або тэкст, аднолькавы з en
    no_tags = remove_tags(strip_icu(custom))
    bad_ru = sorted(set(ch for ch in no_tags if ch in RU_ONLY_LETTERS))
    if bad_ru:
        errors.append(f"{key}: рускія літары {bad_ru} у custom")
    bad_latin = sorted(set(ch for ch in no_tags if ch in LATIN_RE_CHARS))
    if bad_latin:
        errors.append(f"{key}: лацінскія літары {bad_latin} у custom па-за тэгамі")


def check_tags(custom, en, key, errors):
    en_tags = Counter(extract_tags(strip_icu(en)))
    custom_tags = Counter(extract_tags(strip_icu(custom)))
    if en_tags != custom_tags:
        errors.append(
            f"{key}: тэгі не супадаюць en={dict(en_tags)} custom={dict(custom_tags)}"
        )
    en_icu = len(ICU_RE.findall(en))
    custom_icu = len(ICU_RE.findall(custom))
    if bool(en_icu) != bool(custom_icu):
        errors.append(
            f"{key}: ICU-канструкцыя plural/ordinal ёсць толькі ў адным з en/custom"
        )


def check_whitespace_punct(custom, en, key, errors):
    if not en:
        return
    if (custom != custom.strip()) != (en != en.strip()):
        errors.append(f"{key}: прабелы ў пачатку/канцы не супадаюць з en")
    en_last = en[-1] if en else ""
    custom_last = custom[-1] if custom else ""
    en_punct = en_last in ".,!?:;…"
    custom_punct = custom_last in ".,!?:;…"
    if en_punct != custom_punct:
        errors.append(f"{key}: канцавы знак прыпынку не адпавядае en ('{en_last}' vs '{custom_last}')")


def validate_file(path):
    errors = []
    try:
        data = load(path)
    except json.JSONDecodeError as e:
        return [f"{path}: НЕВАЛІДНЫ JSON: {e}"], 0

    head = get_head_version(path)
    if head is not None:
        head_by_key = {e["key"]: e for e in head}
        cur_keys = [e["key"] for e in data]
        head_keys = [e["key"] for e in head]
        if cur_keys != head_keys:
            errors.append(f"{path}: змяніўся парадак/склад ключоў адносна HEAD")
        for e in data:
            h = head_by_key.get(e["key"])
            if h is None:
                continue
            for field in e:
                if field == "custom":
                    continue
                if e.get(field) != h.get(field):
                    errors.append(f"{path}:{e['key']}: поле '{field}' зменена адносна HEAD")

    filled = 0
    for e in data:
        custom = e.get("custom", "")
        en = e.get("en", "")
        if not custom:
            continue
        filled += 1
        check_tags(custom, en, e["key"], errors)
        check_letters(custom, en, e["key"], errors)
        check_whitespace_punct(custom, en, e["key"], errors)

    return errors, filled


def main():
    files = sys.argv[1:] if len(sys.argv) > 1 else DEFAULT_FILES
    total_errors = 0
    for path in files:
        errors, filled = validate_file(path)
        print(f"== {path} == (запоўнена custom: {filled})")
        if errors:
            for e in errors[:200]:
                print(f"  ПАМЫЛКА: {e}")
            if len(errors) > 200:
                print(f"  ... і яшчэ {len(errors) - 200} памылак")
        else:
            print("  ОК")
        total_errors += len(errors)
        print()
    print(f"УСЯГО ПАМЫЛАК: {total_errors}")
    sys.exit(0 if total_errors == 0 else 1)


if __name__ == "__main__":
    main()
