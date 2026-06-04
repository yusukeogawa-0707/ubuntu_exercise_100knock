#!/usr/bin/env python3
from pathlib import Path
import csv

p = Path(__file__).resolve().parents[1] / 'progress' / 'progress_3rounds.csv'
rows = list(csv.DictReader(p.open(encoding='utf-8')))
mods = {}
for r in rows:
    k = (r['topic_title'], r['level'], r['module_file'])
    d = mods.setdefault(k, [0, 0, 0, 0])
    d[0] += 1
    d[1] += bool(r['round1_done'].strip())
    d[2] += bool(r['round2_done'].strip())
    d[3] += bool(r['round3_done'].strip())

level_labels = {
    'intro': '入門編',
    'practice': '実践編',
}
for (title, level, path), (total, r1, r2, r3) in mods.items():
    level_label = level_labels.get(level, level)
    print(f'{level_label} {title}: R1 {r1}/{total}, R2 {r2}/{total}, R3 {r3}/{total}  {path}')
