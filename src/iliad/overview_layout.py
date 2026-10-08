# -*- coding: utf-8 -*-
"""Overview ('battle lines') layout: gods on top by allegiance, Greeks left, Trojans right."""
import math, random, json, itertools
from data_il import NODES, EDGES

W, H = 1100, 1000
R = 28
NODE = {n['id']: n for n in NODES}


def box(n):
    if n['cat'] == 'god':
        if n['camp'] == 'neutral':
            return (520, 80, 580, 120)
        return (70, 80, 470, 250) if n['camp'] == 'ach' else (630, 80, 1030, 250)
    return (70, 350, 450, 930) if n['camp'] == 'ach' else (650, 350, 1030, 930)


def seg_cross(p1, p2, p3, p4):
    def ccw(a, b, c):
        return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])
    return ccw(p1, p3, p4) != ccw(p2, p3, p4) and ccw(p1, p2, p3) != ccw(p1, p2, p4)


def pdist(p, a, b):
    ax, ay = a; bx, by = b; px, py = p
    dx, dy = bx - ax, by - ay
    L = dx * dx + dy * dy or 1
    t = max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / L))
    return math.hypot(ax + t * dx - px, ay + t * dy - py)


ids = [n['id'] for n in NODES]
pairs = [(e[0], e[1]) for e in EDGES]


def cost(P):
    c = 0
    for a, b in pairs:
        c += math.dist(P[a], P[b]) * 1.0
    # spacing (label under node: treat as ellipse wider than tall)
    for a, b in itertools.combinations(ids, 2):
        dx = abs(P[a][0] - P[b][0]); dy = abs(P[a][1] - P[b][1])
        d = math.hypot(dx / 1.25, dy)
        if d < 92:
            c += (92 - d) ** 2 * 8
    # edges through nodes
    for a, b in pairs:
        for v in ids:
            if v in (a, b):
                continue
            d = pdist(P[v], P[a], P[b])
            if d < 40:
                c += (40 - d) * 40
    cr = 0
    for (a, b), (x, y) in itertools.combinations(pairs, 2):
        if len({a, b, x, y}) < 4:
            continue
        if seg_cross(P[a], P[b], P[x], P[y]):
            cr += 1
    return c + cr * 60, cr


def clamp(v, p):
    x0, y0, x1, y1 = box(NODE[v])
    return (min(max(p[0], x0), x1), min(max(p[1], y0), y1))


def run(seed):
    random.seed(seed)
    P = {}
    for v in ids:
        x0, y0, x1, y1 = box(NODE[v])
        P[v] = (random.uniform(x0, x1), random.uniform(y0, y1))
    cur = cost(P)[0]
    T = 400
    for it in range(14000):
        v = random.choice(ids)
        old = P[v]
        step = 60 * (T / 400) + 8
        P[v] = clamp(v, (old[0] + random.gauss(0, step), old[1] + random.gauss(0, step)))
        c2 = cost(P)[0]
        if c2 < cur or random.random() < math.exp((cur - c2) / max(T, 1e-3)):
            cur = c2
        else:
            P[v] = old
        T *= 0.9996
    return cur, P


if __name__ == '__main__':
    best = None
    for s in range(4):
        c, P = run(s)
        print(s, round(c), cost(P)[1], flush=True)
        if best is None or c < best[0]:
            best = (c, P)
    P = {k: (round(x, 1), round(y, 1)) for k, (x, y) in best[1].items()}
    json.dump(P, open('overview.json', 'w'), indent=0)
