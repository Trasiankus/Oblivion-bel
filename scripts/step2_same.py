"""Крок 2: механічнае запаўненне custom у same_bel_belalt_case_insensitive.json.

Патрабуе спачатку `scripts/build_case_freq.py` (стварае case_freq.json).
Вынік: results.json (key -> тэкст), які падаецца ў apply.py.
"""
import json
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE, 'same_bel_belalt_case_insensitive.json')
FREQ_PATH = os.path.join(BASE, 'scripts', 'case_freq.json')
RESULTS_PATH = os.path.join(BASE, 'scripts', 'step2_results.json')

WORD_RE = re.compile(r"[A-Za-zА-Яа-яЁёІіЎў'’\-]+")

PROPER_STEMS = [
    # расы
    "аргоні", "брэтон", "каджыт", "норд", "рэдгард", "альтмер", "дунмер",
    # даэдрычныя прынцы
    "азур", "баэц", "боэці", "клавікус", "хермэ", "гермеус", "хірсін", "херсін",
    "малакат", "мехрунс", "мефал", "мерыды", "молаг", "наміра", "накцюрнал",
    "ноктюрнал", "перайт", "перыайт", "сангвін", "шэагор", "шэагар", "вэрмін",
    "вермін", "джыгалаг", "умарыл",
    # геаграфія Cyrodiil
    "анвіл", "бравіл", "брум", "чэйдзінхол", "чэйдынхол", "чорал", "кватч",
    "леявін", "скінград", "сіродзіл", "тамрыэль",
    # арганізацыі (уласныя часткі назвы, не агульныя словы кшталту "гільдыя"/"легіён")
    "клінк", "міфічн",
    # легендарны набор рэліквій "Крыжака" (Crusader) - заўсёды з вялікай
    # (пацверджана 25 ужо гатовымі custom: "Пальчаткі/Понажы/... Крыжака")
    "крыжак",
]


def is_proper(word_lower):
    return any(word_lower.startswith(stem) for stem in PROPER_STEMS)


def decide_case(word, freq):
    wl = word.lower()
    if is_proper(wl):
        return True
    info = freq.get(wl)
    if info and info['cap'] + info['low'] >= 2:
        return info['ratio'] > 0.5
    return False


def recase(bel, bel_alt, freq):
    words_bel = list(WORD_RE.finditer(bel))
    words_alt = list(WORD_RE.finditer(bel_alt))
    out = list(bel_alt)
    for i, (mb, ma) in enumerate(zip(words_bel, words_alt)):
        wb, wa = mb.group(0), ma.group(0)
        if wb == wa:
            # bel і bel_alt пагаджаюцца ў рэгістры гэтага слова (у тым ліку
            # абрэвіятуры/тэхнічныя ID кшталту "NPC", "XII", "FG") - не
            # чапаем, капіюем як ёсць.
            new_w = wa
        else:
            want_cap = True if i == 0 else decide_case(wa, freq)
            new_w = wa[0].upper() + wa[1:].lower() if want_cap else wa.lower()
        out[ma.start():ma.end()] = new_w
    return ''.join(out)


def main():
    freq = json.load(open(FREQ_PATH, encoding='utf-8'))
    data = json.load(open(DATA_PATH, encoding='utf-8'))
    results = {}
    identical = 0
    recased = 0
    for e in data:
        if e.get('custom'):
            continue
        bel, bel_alt = e['bel'], e['bel_alt']
        if bel == bel_alt:
            results[e['key']] = bel
            identical += 1
        else:
            results[e['key']] = recase(bel, bel_alt, freq)
            recased += 1
    json.dump(results, open(RESULTS_PATH, 'w', encoding='utf-8'), ensure_ascii=False)
    print(f"identical: {identical}, recased: {recased}, total: {len(results)}")


if __name__ == '__main__':
    main()
