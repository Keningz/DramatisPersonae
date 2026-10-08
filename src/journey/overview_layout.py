# -*- coding: utf-8 -*-
"""Overview layout for the Journey to the West map: Heaven top left, the Buddhist West top right, the pilgrims in
the middle, and the people met on the road placed by chapter from left (early) to right (late). Within each
region a simulated-annealing pass picks the slots that give the fewest crossings and the fewest lines running
through other people. Writes overview.json. Run: python3 overview_layout.py"""
import json, math, random, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from data_xy import NODES, EDGES  # noqa: E402

FIXED = {'wukong': (600, 505), 'tangseng': (600, 375), 'bajie': (478, 560), 'shaseng': (722, 560), 'horse': (600, 640)}
REGIONS = {
    'heaven': (['jade', 'queenmother', 'laojun', 'jinxing', 'erlang', 'lijing', 'nezha', 'change'],
               [(x, 100) for x in (80, 190, 300, 410, 520)] + [(x, 222) for x in (135, 245, 355, 465)]),
    'buddha': (['rulai', 'guanyin', 'maitreya', 'manjushri', 'samantabhadra', 'lingji'],
               [(x, 100) for x in (680, 790, 900, 1010, 1120)] + [(x, 222) for x in (735, 845, 955, 1065)]),
    'origin': (['subodhi', 'aoguang', 'taizong'],
               [(80, 392), (190, 392), (80, 484), (190, 484), (300, 440)]),
    'early': (['blackbear', 'cuilan', 'yellowwind', 'zhenyuan', 'whitebone', 'yellowrobe', 'baihuaxiu', 'goldhorn',
               'silverhorn', 'wujiking', 'redboy', 'aorun', 'tuolong'],
              [(x, y) for y in (632, 748, 864, 980) for x in (80, 190, 300, 410)] + [(330, 535)]),
    'middle': (['goldfish', 'greenox', 'womanking', 'sixear', 'ironfan', 'bull', 'jadeface', 'ninehead', 'yellowbrow'],
               [(x, y) for y in (770, 885, 1000) for x in (530, 640, 750)] + [(860, 1000)]),
    'late': (['saitaisui', 'spiders', 'whiteelephant', 'roc', 'greenlion', 'mouse', 'jaderabbit'],
             [(x, y) for y in (405, 530, 655, 780, 900) for x in (880, 1000, 1115)]),
}
ids = [n['id'] for n in NODES]
assert set(ids) == set(FIXED) | {v for r in REGIONS.values() for v in r[0]}, set(ids) ^ ({v for r in REGIONS.values() for v in r[0]} | set(FIXED))
E = [(e[0], e[1]) for e in EDGES]
inc = {v: [] for v in ids}
for i, (a, b) in enumerate(E):
    inc[a].append(i)
    inc[b].append(i)


def ccw(A, B, C):
    return (C[1] - A[1]) * (B[0] - A[0]) - (B[1] - A[1]) * (C[0] - A[0])


def cross(p1, p2, p3, p4):
    if p1 in (p3, p4) or p2 in (p3, p4):
        return False
    d1, d2 = ccw(p3, p4, p1), ccw(p3, p4, p2)
    d3, d4 = ccw(p1, p2, p3), ccw(p1, p2, p4)
    return (d1 * d2 < 0) and (d3 * d4 < 0)


def seg_dist(P, A, B):
    ax, ay = A; bx, by = B; px, py = P
    dx, dy = bx - ax, by - ay
    L = dx * dx + dy * dy
    t = max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / L)) if L else 0
    return math.hypot(px - ax - t * dx, py - ay - t * dy)


def edge_cost(i, pos):
    a, b = E[i]
    A, B = pos[a], pos[b]
    c = 0.0
    for j, (u, v) in enumerate(E):
        if j != i and cross(A, B, pos[u], pos[v]):
            c += 0.5          # each crossing is counted from both edges
    for w in ids:
        if w != a and w != b:
            d = seg_dist(pos[w], A, B)
            if d < 36:
                c += 4 * (36 - d) / 36 + 2
    c += math.hypot(A[0] - B[0], A[1] - B[1]) * 0.004
    return c


def total(pos):
    return sum(edge_cost(i, pos) for i in range(len(E)))


def run(seed=1, iters=9000):
    rnd = random.Random(seed)
    pos = dict(FIXED)
    slots = {}
    for k, (members, sl) in REGIONS.items():
        sl = sl[:]
        rnd.shuffle(sl)
        slots[k] = sl
        for v, p in zip(members, sl):
            pos[v] = p
    cur = total(pos)
    T0 = 6.0
    for it in range(iters):
        T = T0 * (1 - it / iters) + 0.02
        k = rnd.choice(list(REGIONS))
        members, _ = REGIONS[k]
        sl = slots[k]
        i = rnd.randrange(len(members))
        j = rnd.randrange(len(sl))
        vi = members[i]
        # target slot j: occupied by another member, or free
        other = next((m for m in members if pos[m] == sl[j]), None)
        if other == vi:
            continue
        touched = set(inc[vi]) | (set(inc[other]) if other else set())
        before = sum(edge_cost(e, pos) for e in touched)
        old_i = pos[vi]
        pos[vi] = sl[j]
        if other:
            pos[other] = old_i
        after = sum(edge_cost(e, pos) for e in touched)
        d = after - before
        if d < 0 or rnd.random() < math.exp(-d / T):
            cur += d
        else:
            pos[vi] = old_i
            if other:
                pos[other] = sl[j]
    return total(pos), pos


if __name__ == '__main__':
    best = None
    for seed in range(1, 4):
        c, pos = run(seed)
        print('seed', seed, round(c, 1))
        if not best or c < best[0]:
            best = (c, pos)
    c, pos = best
    ncross = sum(1 for i in range(len(E)) for j in range(i + 1, len(E))
                 if cross(pos[E[i][0]], pos[E[i][1]], pos[E[j][0]], pos[E[j][1]]))
    print('best', round(c, 1), 'crossings', ncross)
    json.dump({v: list(pos[v]) for v in ids}, open(os.path.join(HERE, 'overview.json'), 'w'), indent=0)
