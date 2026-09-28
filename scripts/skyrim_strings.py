#!/usr/bin/env python3
"""Утыліта для чытання бінарных .strings/.dlstrings/.ilstrings файлаў
Bethesda (Skyrim) і пабудовы слоўніка en -> bel для тэрміналогіі.
Не частка асноўнага TASK.md pipeline - дапаможны аднаразовы скрыпт для
стварэння glossary.md (Крок 1).
"""
import glob
import os
import struct
import sys


def read_strings(path):
    """.STRINGS: id -> null-terminated UTF-8 string."""
    with open(path, "rb") as f:
        data = f.read()
    count, _data_size = struct.unpack_from("<II", data, 0)
    off = 8
    entries = []
    for _ in range(count):
        sid, soff = struct.unpack_from("<II", data, off)
        off += 8
        entries.append((sid, soff))
    strings_start = off
    result = {}
    for sid, soff in entries:
        start = strings_start + soff
        end = data.index(b"\x00", start)
        result[sid] = data[start:end].decode("utf-8", errors="replace")
    return result


def read_lstrings(path):
    """.DLSTRINGS / .ILSTRINGS: id -> (length-prefixed) UTF-8 string."""
    with open(path, "rb") as f:
        data = f.read()
    count, _data_size = struct.unpack_from("<II", data, 0)
    off = 8
    entries = []
    for _ in range(count):
        sid, soff = struct.unpack_from("<II", data, off)
        off += 8
        entries.append((sid, soff))
    strings_start = off
    result = {}
    for sid, soff in entries:
        pos = strings_start + soff
        (length,) = struct.unpack_from("<I", data, pos)
        start = pos + 4
        result[sid] = data[start:start + length - 1].decode("utf-8", errors="replace")
    return result


def read_any(path):
    ext = path.rsplit(".", 1)[-1].lower()
    if ext == "strings":
        return read_strings(path)
    return read_lstrings(path)


def build_pairs(en_dir, bel_dir):
    """Вяртае спіс (en_text, bel_text) для ўсіх супадаючых id/файл."""
    en_files = {os.path.basename(p).lower(): p for p in glob.glob(os.path.join(en_dir, "**", "*"), recursive=True) if os.path.isfile(p)}
    bel_files = {os.path.basename(p).lower(): p for p in glob.glob(os.path.join(bel_dir, "**", "*"), recursive=True) if os.path.isfile(p)}
    pairs = []
    for name, en_path in en_files.items():
        bel_path = bel_files.get(name)
        if not bel_path:
            continue
        try:
            en_map = read_any(en_path)
            bel_map = read_any(bel_path)
        except Exception as e:
            print(f"skip {name}: {e}", file=sys.stderr)
            continue
        for sid, en_text in en_map.items():
            bel_text = bel_map.get(sid)
            if bel_text is not None and en_text.strip():
                pairs.append((en_text, bel_text))
    return pairs


if __name__ == "__main__":
    pairs = build_pairs(sys.argv[1], sys.argv[2])
    print(f"# пар: {len(pairs)}", file=sys.stderr)
    import json
    json.dump(pairs, sys.stdout, ensure_ascii=False)
