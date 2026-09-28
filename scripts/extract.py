#!/usr/bin/env python3
"""extract.py FILE START COUNT

Выводзіць у stdout (JSONL, адзін запіс на радок) COUNT запісаў з пустым
"custom", пачынаючы з START-га (0-indexed) сярод усіх пустых запісаў файла.
Палі: key, en, ru, bel, bel_alt, pl (толькі тыя, што прысутнічаюць).
"""
import json
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from common import load, is_empty_custom, FIELDS


def main():
    if len(sys.argv) != 4:
        print("Ужыванне: extract.py FILE START COUNT", file=sys.stderr)
        sys.exit(1)
    path, start, count = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    data = load(path)
    empty = [e for e in data if is_empty_custom(e)]
    chunk = empty[start:start + count]
    for e in chunk:
        row = {k: e.get(k, "") for k in FIELDS if k in e}
        print(json.dumps(row, ensure_ascii=False))
    print(f"# усяго пустых: {len(empty)}, выведзена: {len(chunk)} (з {start})", file=sys.stderr)


if __name__ == "__main__":
    main()
