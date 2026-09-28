#!/usr/bin/env python3
"""suggest.py PORTION.jsonl

Для кожнага запісу партыі (з extract.py): калі ў ЎЖО ЗАПОЎНЕНЫХ custom
(ва ўсіх файлах) ці ў аўтаматычнай табліцы glossary.md ёсць дакладнае
супадзенне па `en` - прапануе гатовы тэкст (для адзінства тэрміналогіі).
Інакш пазначае NEEDS_DECISION. Толькі дапаможны інструмент, канчатковае
рашэнне заўсёды застаецца за чалавекам/перакладчыкам.
"""
import json
import sys
import os
import collections

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FILES = [
    "different_bel_belalt_case_insensitive.json",
    "same_bel_belalt_case_insensitive.json",
    "ST_AltarDynamicTexts.json",
    "ST_AltarStaticTexts.json",
    "ST_HardcodedContent.json",
    "ST_MissingEntries.json",
]


def load_custom_map():
    en_to_custom = collections.defaultdict(collections.Counter)
    for fname in FILES:
        path = os.path.join(BASE, fname)
        if not os.path.exists(path):
            continue
        data = json.load(open(path, encoding='utf-8'))
        for e in data:
            if e.get('custom'):
                en_to_custom[e['en']][e['custom']] += 1
    return en_to_custom


def main():
    portion_path = sys.argv[1]
    en_to_custom = load_custom_map()
    with open(portion_path, encoding='utf-8') as f:
        lines = [json.loads(l) for l in f if l.strip()]
    for row in lines:
        en = row['en']
        c = en_to_custom.get(en)
        if c:
            best, cnt = c.most_common(1)[0]
            print(f"MATCH\t{row['key']}\t{best}\t(x{cnt})\t{en}")
        else:
            print(f"DECIDE\t{row['key']}\t\t\t{en}\tbel={row.get('bel')!r}\tbel_alt={row.get('bel_alt')!r}")


if __name__ == '__main__':
    main()
