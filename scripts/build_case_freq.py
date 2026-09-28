"""Дапаможны скрыпт для Кроку 2: частата вялікай/малой літары для слоў
не ў пачатку сказа, пабудаваная з ужо гатовых (чалавекам) `custom`.
Выкарыстоўваецца ў scripts/step2_same.py.
"""
import collections
import json
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

data = json.load(open(os.path.join(BASE, 'different_bel_belalt_case_insensitive.json'), encoding='utf-8')) + \
       json.load(open(os.path.join(BASE, 'same_bel_belalt_case_insensitive.json'), encoding='utf-8'))

WORD_RE = re.compile(r"[A-Za-zА-Яа-яЁёІіЎў'’\-]+")

freq = collections.defaultdict(lambda: [0, 0])  # word_lower -> [cap_count, low_count]

for e in data:
    custom = e.get('custom')
    if not custom:
        continue
    words = WORD_RE.findall(custom)
    for i, w in enumerate(words):
        if i == 0:
            continue  # skip sentence-initial word
        wl = w.lower()
        if w[0].isupper():
            freq[wl][0] += 1
        else:
            freq[wl][1] += 1

out = {}
for w, (cap, low) in freq.items():
    total = cap + low
    if total >= 2:
        out[w] = {'cap': cap, 'low': low, 'ratio': cap / total}

json.dump(out, open(os.path.join(BASE, 'scripts', 'case_freq.json'), 'w', encoding='utf-8'), ensure_ascii=False)
print(f"words tracked: {len(out)}")
