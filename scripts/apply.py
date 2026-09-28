#!/usr/bin/env python3
"""apply.py FILE RESULTS

RESULTS — JSON-файл {key: "тэкст перакладу", ...}.
Запісвае "custom" толькі для запісаў, дзе ён зараз пусты. Іншыя палі і
парадак файла не мяняюцца (сурагатнае тэкставае рэдагаванне, без
перазапісу ўсяго JSON праз json.dump).
"""
import json
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from common import load, read_raw, json_str_escape, json_str_unescape, ENTRY_RE, is_empty_custom


def main():
    if len(sys.argv) != 3:
        print("Ужыванне: apply.py FILE RESULTS", file=sys.stderr)
        sys.exit(1)
    path, results_path = sys.argv[1], sys.argv[2]

    with open(results_path, encoding="utf-8") as f:
        results = json.load(f)

    data = load(path)
    empty_keys = {e["key"] for e in data if is_empty_custom(e)}
    all_keys = {e["key"] for e in data}

    raw = read_raw(path)

    applied = []
    skipped_filled = []
    not_found = []
    not_empty_now = []

    def repl(m):
        key = json_str_unescape(m.group(1))
        if key not in results:
            return m.group(0)
        if key not in all_keys:
            not_found.append(key)
            return m.group(0)
        if key not in empty_keys:
            not_empty_now.append(key)
            return m.group(0)
        new_text = results[key]
        applied.append(key)
        return f'"key": "{m.group(1)}",\n    "custom": "{json_str_escape(new_text)}"'

    new_raw = ENTRY_RE.sub(repl, raw)

    for key in results:
        if key not in all_keys:
            if key not in not_found:
                not_found.append(key)

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_raw)

    print(f"Прыменена: {len(applied)}")
    if not_empty_now:
        print(f"Прапушчана (custom ужо запоўнены): {len(not_empty_now)} -> {not_empty_now[:20]}")
    if not_found:
        print(f"Не знойдзена ключоў у файле: {len(not_found)} -> {not_found[:20]}")


if __name__ == "__main__":
    main()
