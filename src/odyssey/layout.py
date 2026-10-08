# -*- coding: utf-8 -*-
"""Ring layout: Odysseus at centre, everyone else on an ellipse; chords bow inward."""
import math
from data import NODES, EDGES

ORDER = ['zeus', 'poseidon', 'polyphemus', 'alcinous', 'nausicaa', 'athena', 'mentor', 'argos',
         'eurycleia', 'menelaus', 'nestor', 'telemachus', 'eumaeus', 'melanthius', 'eurymachus',
         'antinous', 'penelope', 'laertes', 'anticleia', 'tiresias', 'scylla', 'sirens', 'circe',
         'eurylochus', 'helios', 'calypso', 'hermes']

W, H = 1240, 1120
CX, CY = 620, 560
A, B = 455, 470
R = 35          # portrait radius
RC = 64         # Odysseus radius

NODE = {n['id']: n for n in NODES}


def ellipse_arc_positions(n, a, b, start=-math.pi / 2):
    """n points evenly spaced by arc length on an ellipse, first at `start`."""
    M = 20000
    ts = [start + 2 * math.pi * k / M for k in range(M + 1)]
    pts = [(a * math.cos(t), b * math.sin(t)) for t in ts]
    cum = [0.0]
    for i in range(1, len(pts)):
        cum.append(cum[-1] + math.dist(pts[i], pts[i - 1]))
    total = cum[-1]
    out = []
    j = 0
    for k in range(n):
        target = total * k / n
        while cum[j] < target:
            j += 1
        out.append(pts[j])
    return out


def compute():
    pos = {'odysseus': (CX, CY)}
    pts = ellipse_arc_positions(len(ORDER), A, B)
    for v, (x, y) in zip(ORDER, pts):
        pos[v] = (CX + x, CY + y)
    return pos


def text_w(s, fs):
    w = 0
    for ch in s:
        if ch in ' ·':
            w += 0.34 * fs if ch == ' ' else 0.45 * fs
        elif ch in 'ilj.,\'':
            w += 0.3 * fs
        elif ch in 'mwMW':
            w += 0.85 * fs
        elif ord(ch) < 128 or ch in '–':
            w += (0.66 if ch.isupper() else 0.55) * fs
        else:
            w += 1.0 * fs
    return w


def qpoint(p0, c, p1, t):
    return ((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * c[0] + t * t * p1[0],
            (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * c[1] + t * t * p1[1])


FONT = {
    'zh': dict(name=18, sub=13, big_name=23, big_sub=14, edge=14, pad=14),
    'en': dict(name=18.5, sub=12.5, big_name=24, big_sub=13.5, edge=13.5, pad=14),
}


def overlap(b, others, pad=3):
    s = 0
    for o in others:
        ox = min(b[2] + pad, o[2]) - max(b[0] - pad, o[0])
        oy = min(b[3] + pad, o[3]) - max(b[1] - pad, o[1])
        if ox > 0 and oy > 0:
            s += ox * oy
    return s


def edge_paths():
    """Geometry of every edge (language independent)."""
    pos = compute()
    idx = {v: i for i, v in enumerate(ORDER)}
    n = len(ORDER)
    out = []
    for (s, t, *_rest) in EDGES:
        p0, p1 = pos[s], pos[t]
        if 'odysseus' in (s, t):
            other = t if s == 'odysseus' else s
            out.append(dict(curve=False, p_from=(CX, CY), p_to=pos[other],
                            d='M%.1f,%.1f L%.1f,%.1f' % (p0[0], p0[1], p1[0], p1[1]),
                            cands=[0.5, 0.58, 0.44, 0.64, 0.38, 0.7, 0.34, 0.76, 0.3, 0.8]))
        else:
            i, j = idx[s], idx[t]
            k = min((i - j) % n, (j - i) % n)
            mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
            dx, dy = CX - mx, CY - my
            L = math.hypot(dx, dy)
            depth = {1: 95, 2: 120, 3: 120, 4: 110}.get(k, 70 + 6 * k)
            depth = min(depth, L - 90)
            c = (mx + dx / L * depth * 2, my + dy / L * depth * 2)
            out.append(dict(curve=True, p_from=p0, p_to=p1, c=c,
                            d='M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f' % (p0[0], p0[1], c[0], c[1], p1[0], p1[1]),
                            cands=[0.5, 0.42, 0.58, 0.35, 0.65, 0.3, 0.7, 0.25, 0.75]))
    return pos, out


def build_geometry(lang='zh', name_of=None, sub_of=None, label_of=None):
    """Positions are shared; label placement depends on the language's text widths."""
    F = FONT[lang]
    pos, paths = edge_paths()
    name_of = name_of or (lambda v: NODE[v]['zh'])
    sub_of = sub_of or (lambda v: NODE[v]['sub'])
    label_of = label_of or (lambda i: EDGES[i][3])

    def lab_box(v, lab):
        big = v == 'odysseus'
        fs1, fs2 = (F['big_name'], F['big_sub']) if big else (F['name'], F['sub'])
        lw = max(text_w(name_of(v), fs1), text_w(sub_of(v), fs2)) + 4
        if lab['anchor'] == 'middle':
            x0 = lab['x'] - lw / 2
        elif lab['anchor'] == 'start':
            x0 = lab['x']
        else:
            x0 = lab['x'] - lw
        y0 = lab['y'] - fs1 + 2
        return (x0, y0, x0 + lw, y0 + fs1 + fs2 + 6)

    circles = []
    for v, (x, y) in pos.items():
        r = RC if v == 'odysseus' else R
        circles.append((v, x - r - 3, y - r - 3, x + r + 3, y + r + 3))
    nodes, boxes = [], []
    for v, (x, y) in pos.items():
        r = RC if v == 'odysseus' else R
        dx, dy = x - CX, y - CY
        L = math.hypot(dx, dy) or 1
        ux, uy = dx / L, dy / L
        face = 'left' if x > CX + 1 else 'right'
        if v == 'odysseus':
            lab = dict(x=x, y=y + r + 26, anchor='middle')
        else:
            cands = {
                'right': dict(x=x + r + 11, y=y - 1, anchor='start'),
                'left': dict(x=x - r - 11, y=y - 1, anchor='end'),
                'above': dict(x=x, y=y - r - 26, anchor='middle'),
                'below': dict(x=x, y=y + r + 22, anchor='middle'),
            }
            pref = ('right' if ux > 0 else 'left') if abs(ux) > 0.8 else ('above' if uy < 0 else 'below')
            side = 'right' if ux > 0 else 'left'
            best = None
            for k, lab0 in cands.items():
                b = lab_box(v, lab0)
                sc = overlap(b, [c[1:] for c in circles if c[0] != v], 2) * 3 + overlap(b, boxes, 2) * 3
                bx, by = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
                if math.hypot(bx - CX, by - CY) < L:
                    sc += 3000
                if b[0] < 4 or b[2] > W - 4 or b[1] < 4 or b[3] > H - 4:
                    sc += 5000
                sc += 0 if k == pref else (300 if k == side else 900)
                if best is None or sc < best[0]:
                    best = (sc, lab0)
            lab = best[1]
        boxes.append(lab_box(v, lab))
        nodes.append(dict(id=v, x=round(x, 1), y=round(y, 1), r=r, lab=lab, face=face))
    for c in circles:
        boxes.append(c[1:])

    labels = [None] * len(EDGES)
    order_e = sorted(range(len(EDGES)), key=lambda i: 0 if 'odysseus' in EDGES[i][:2] else 1)
    for ei in order_e:
        g = paths[ei]
        text = label_of(ei)
        lw = text_w(text, F['edge']) + F['pad']
        lh = 21
        best = None
        dx, dy = g['p_to'][0] - g['p_from'][0], g['p_to'][1] - g['p_from'][1]
        dl = math.hypot(dx, dy) or 1
        nx, ny = -dy / dl, dx / dl
        for tt in g['cands'] + [0.2, 0.8, 0.15, 0.85]:
            if g['curve']:
                q0 = qpoint(g['p_from'], g['c'], g['p_to'], tt)
            else:
                q0 = (g['p_from'][0] + dx * tt, g['p_from'][1] + dy * tt)
            for off in (0, 9, -9):
                q = (q0[0] + nx * off, q0[1] + ny * off)
                b = (q[0] - lw / 2, q[1] - lh / 2, q[0] + lw / 2, q[1] + lh / 2)
                sc = overlap(b, boxes) + abs(tt - 0.5) * 40 + abs(off) * 3
                if best is None or sc < best[0]:
                    best = (sc, q, b)
        boxes.append(best[2])
        labels[ei] = dict(text=text, lx=round(best[1][0], 1), ly=round(best[1][1], 1),
                          lw=round(lw, 1), lh=lh, ov=round(best[0]))
    edges = []
    for i, (s, t, typ, lab, text, bk) in enumerate(EDGES):
        edges.append(dict(s=s, t=t, type=typ, label=lab, text=text, bk=bk, d=paths[i]['d'], lab=labels[i]))
    return nodes, edges


if __name__ == '__main__':
    from data_en import NODE_EN, EDGE_EN
    for lang in ('zh', 'en'):
        if lang == 'en':
            nodes, edges = build_geometry('en', lambda v: NODE[v]['en'], lambda v: NODE_EN[v][0], lambda i: EDGE_EN[i][0])
        else:
            nodes, edges = build_geometry('zh')
        bad = [(e['s'], e['t'], e['lab']['text'], e['lab']['ov']) for e in edges if e['lab']['ov'] > 20]
        print(lang, 'label overlaps:', bad)
