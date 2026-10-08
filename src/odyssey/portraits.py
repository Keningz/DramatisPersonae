# -*- coding: utf-8 -*-
"""Vase-painting style profile portraits, drawn in a 100x100 box, facing right.
style red   = red-figure  (clay figure on black glaze)       -> gods & mortals
style black = black-figure (black figure on clay, incised)   -> monsters
style white = white-ground lekythos (outline on white slip)  -> shades in Hades
"""

PAL = {
    'red':   dict(bg='#1f1612', fig='#cf7442', ln='#1f1612', hair='#1f1612', hl='#cf7442',
                  wh='#f0e4c6', acc='#e9a766', skin='#cf7442', red='#8e2e22', obj='#cf7442'),
    'black': dict(bg='#d27a45', fig='#1f1612', ln='#d27a45', hair='#1f1612', hl='#d27a45',
                  wh='#f2e6c9', acc='#8e2e22', skin='#1f1612', red='#8e2e22', obj='#1f1612'),
    'white': dict(bg='#efe6d1', fig='#efe6d1', ln='#4d3829', hair='#9a6a45', hl='#4d3829',
                  wh='#fbf6ea', acc='#c79a6a', skin='#efe6d1', red='#a2553a', obj='#6b4f3a'),
}


def P(d, fill='none', stroke=None, sw=0.8, extra=''):
    s = f'<path d="{d}" fill="{fill}"'
    if stroke:
        s += f' stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"'
    return s + f'{extra}/>'


def C_(cx, cy, r, fill='none', stroke=None, sw=0.8):
    s = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"'
    if stroke:
        s += f' stroke="{stroke}" stroke-width="{sw}"'
    return s + '/>'


# ---------------------------------------------------------------- base pieces
HEAD = ("M57,28 C59.6,32 61.2,36.5 62.2,41 L68,50.6 C68.6,51.9 67.6,53.2 65.3,53.3 "
        "C64.7,54.2 64.9,55.2 64.9,55.7 C64.4,56.5 63.5,57 62.5,57.2 C63.4,57.6 64.1,58.3 63.9,59.1 "
        "C63.3,60 62.5,60.4 62.3,60.9 C63.3,62.6 63.5,64.9 61.6,66.4 C60.1,67.5 58.3,67.9 57.1,68 "
        "C57.6,73 58.2,78 59.2,86 L37.5,86 C39,78 39.6,72 38.8,66 C33,60 30,50 32,41 "
        "C34,31 44,25 52,26 C54.5,26.4 56,27 57,28 Z")

GARMENT = "M6,100 C9,88 22,80 37,78.6 C44,82.6 53,83 60,80.2 C74,80.8 88,88 94,100 Z"
GARMENT_FOLDS = ["M37,78.6 C44,83.6 53,84 60,80.2", "M40,84 C42.4,89 43,94 41.6,100",
                 "M57,85 C58.4,90 58.4,95 57,100", "M26,86 C29,90 30,95 29,100",
                 "M72,85 C71,90 71.4,95 73,100"]


def garment(C, folds=True, himation=False):
    s = P(GARMENT, C['fig'], C['ln'], 0.8)
    if folds:
        for d in GARMENT_FOLDS:
            s += P(d, 'none', C['ln'], 0.7)
    if himation:
        s += P("M14,92 C30,86 52,86 74,90 C82,92 88,95 92,99", 'none', C['ln'], 1.1)
        s += P("M18,96 C34,90 54,90 76,94", 'none', C['ln'], 0.6)
    return s


def head(C):
    return P(HEAD, C['skin'], C['ln'], 0.8)


def eye(C, kind='open', x=0, y=0):
    ln = C['ln']
    if kind == 'closed':
        return (P(f"M{54.6+x},{44+y} Q{57.5+x},{45.8+y} {60.3+x},{44.2+y}", 'none', ln, 0.9)
                + P(f"M{53.4+x},{40.8+y} Q{57.2+x},{39.2+y} {61.2+x},{40.5+y}", 'none', ln, 0.8))
    s = P(f"M{54.6+x},{43.9+y} Q{57.5+x},{41.8+y} {60.5+x},{43.2+y}", 'none', ln, 0.9)
    s += P(f"M{55.3+x},{44.3+y} Q{57.9+x},{45.6+y} {60.1+x},{44.5+y}", 'none', ln, 0.7)
    s += C_(58.8 + x, 43.8 + y, 1.05, ln)
    s += P(f"M{53.4+x},{40.6+y} Q{57.2+x},{38.8+y} {61.3+x},{40.3+y}", 'none', ln, 0.85)
    return s


def face_lines(C, old=False, smile=False):
    ln = C['ln']
    s = P("M65.3,52.4 Q64.4,52.1 63.9,52.9", 'none', ln, 0.7)       # nostril
    s += P("M62.5,57.2 L60.6,57.5", 'none', ln, 0.8)                 # mouth
    s += P("M50,67 C51.6,72 52.4,77 52.4,82", 'none', ln, 0.55)      # neck muscle
    if old:
        s += P("M53,35.5 Q56,34.5 59,35.2", 'none', ln, 0.5)
        s += P("M52.6,37.6 Q55.6,36.6 59.6,37.4", 'none', ln, 0.5)
        s += P("M61.5,46.5 Q60,49 60.8,51.5", 'none', ln, 0.5)       # cheek fold
        s += P("M52.8,44.6 L51.4,45.6 M52.9,43.2 L51.2,43.2", 'none', ln, 0.45)
    return s


def ear(C, x=0, y=0):
    return (P(f"M{46.4+x},{44.6+y} C{43.6+x},{43.4+y} {41.8+x},{45.8+y} {42.4+x},{48.6+y} "
              f"C{42.9+x},{51+y} {44.4+x},{52.6+y} {46.2+x},{52.3+y}", C['skin'], C['ln'], 0.8)
            + P(f"M{45.1+x},{46.3+y} C{43.9+x},{46.8+y} {43.9+x},{48.8+y} {45+x},{49.8+y}", 'none', C['ln'], 0.6))


# ---- hair
HAIR_SHORT = ("M57.4,29.2 C56,32.6 53.6,35.2 50.6,36.8 C48.6,39.6 48,43 47.6,46 L47,50 "
              "C44.4,53 42,57.5 40.5,63.5 L38.8,66.2 C33,60 30,50 32,41 C34,31 44,25 52,26 "
              "C54.5,26.4 56.3,27.5 57.4,29.2 Z")
HAIR_LONG = ("M57.4,29.2 C56,32.6 53.6,35.2 50.6,36.8 C48.6,39.6 48,43 47.6,46 L47,50 "
             "C45,55 44.5,60 45.5,66 C46.5,72 45,78 41,82 C37,84 32,83 28,80 "
             "C30,74 31,68 30,62 C28,54 28.5,46 31,39 C34,31 44,25 52,26 "
             "C54.5,26.4 56.3,27.5 57.4,29.2 Z")
HAIR_BUN = ("M57.2,29.4 C55.4,32.6 52.6,35 49.4,36.4 C47.6,39.4 47.2,42.6 47,45.4 "
            "C46,48.6 44.6,51.4 42.6,53.6 C40,52.6 37.6,50.4 36,47.6 "
            "C31,49 25.5,46.5 24.2,41.2 C23,35.6 27,31 32.4,31.4 "
            "C36.5,27.4 44,25 52,26 C54.5,26.4 56.3,27.5 57.2,29.4 Z")


def hair(C, kind='short', color=None, curls=True):
    col = color or C['hair']
    d = {'short': HAIR_SHORT, 'long': HAIR_LONG, 'bun': HAIR_BUN}[kind]
    s = P(d, col, C['hl'], 0.9)
    tex = C['hl'] if col == C['hair'] else C['ln']
    if kind == 'short':
        s += P("M36,38 C39,36 41,37 44,35.6 M35,46 C37.5,44 40,45 42.5,43 M37,54 C39,52 41,53 43,51",
               'none', tex, 0.5, ' opacity=".7"')
    elif kind == 'long':
        s += P("M34,44 C35,54 34,64 33,76 M38.5,46 C39.5,56 39,66 37,78 M42.5,52 C42.8,60 42.6,68 40.8,79",
               'none', tex, 0.5, ' opacity=".7"')
    elif kind == 'bun':
        s += P("M27,37 C29,41 30,43 34,44.5 M29,33.5 C33,36 34.5,40 34,43 M40,33 C43,34 45,35 47.5,36",
               'none', tex, 0.5, ' opacity=".7"')
    if curls and kind != 'bun':
        for (x, y) in [(56.4, 30.4), (54.6, 33.1), (52.2, 35.4), (49.8, 37.6)]:
            s += C_(x, y, 1.05, 'none', tex, 0.55)
    return s


def white_hair(C, kind='short'):
    """Old people: hair painted in added white."""
    return hair(C, kind, color=C['wh'], curls=False)


# ---- beards
BEARD_SHORT = ("M47.6,47 C48.5,52 51,56 55.2,58 C57.4,58.8 59.8,59.8 61.8,61 C63,62.8 63.6,64.8 63.2,66.8 "
               "C63.8,69.4 63.4,72.2 61.2,74.6 C58,76 54,75 50.5,72 C46.5,68.5 43,63.2 41,59 "
               "C42.5,55 44.5,50.5 47.6,47 Z")
BEARD_POINT = ("M47.6,47 C48.5,52 51,56 55.2,58 C57.4,58.8 59.8,59.8 61.8,61 C63,62.8 63.6,64.8 63.4,66.8 "
               "C64.8,70 66.5,74 68.5,77.5 C63,78 57,76 52,72.5 C47,69 43,63.4 41,59 "
               "C42.5,55 44.5,50.5 47.6,47 Z")
BEARD_LONG = ("M47.6,47 C48.5,52 51,56 55.2,58 C57.4,58.8 59.8,59.8 61.8,61 C63.2,63.4 64,66 63.8,69 "
              "C64.8,74 64.4,80 62,86.5 C57,87 52,84.5 48.5,79.5 C44.5,73.5 42,66.2 41,59 "
              "C42.5,55 44.5,50.5 47.6,47 Z")
MUSTACHE = ("M58.6,54.8 C60.6,54.4 63.2,54.9 65,55.9 C63.8,57 62.7,57.3 61.6,57.9 "
            "C60.3,57.3 59.2,56.4 58.6,54.8 Z")


def beard(C, kind='short', color=None):
    col = color or C['hair']
    d = {'short': BEARD_SHORT, 'long': BEARD_LONG, 'point': BEARD_POINT}[kind]
    tex = C['hl'] if col == C['hair'] else C['ln']
    s = P(d, col, C['hl'] if col == C['hair'] else C['ln'], 0.8)
    s += P(MUSTACHE, col, C['hl'] if col == C['hair'] else C['ln'], 0.6)
    if kind == 'long':
        s += P("M50,62 C52,70 55,77 57,84 M54,61 C56,68 58.5,75 60,82 M46.5,60 C48,67 50.5,74 52.5,79",
               'none', tex, 0.5, ' opacity=".75"')
    elif kind == 'point':
        s += P("M50,61 C54,66 58,70 63,74 M47,58 C50,63 53,67 57,71", 'none', tex, 0.5, ' opacity=".75"')
    else:
        s += P("M49,60 C51,65 54,69 57,72 M53,60.5 C55,64 57.5,67.5 60,70", 'none', tex, 0.5, ' opacity=".75"')
    return s


# ---- headgear & accessories
def fillet(C, color=None, sw=1.8):
    return P("M56.6,30.8 C50,33.4 42,37.4 33.2,44.6", 'none', color or C['fig'], sw)


def wreath(C, color=None):
    col = color or C['fig']
    lnc = C['ln']
    s = P("M57.4,30.2 C50,32.8 41.5,36.8 32.8,43.6", 'none', col, 0.8)
    import math
    for i in range(6):
        t = i / 5
        x = 56 - t * 21.4
        y = 30.6 + t * 11.4
        for side, a in ((-1, -62), (1, 28)):
            ax = x + side * 0.4
            s += (f'<ellipse cx="{ax:.1f}" cy="{y + side*1.6:.1f}" rx="2.9" ry="1.15" '
                  f'transform="rotate({a} {ax:.1f} {y + side*1.6:.1f})" fill="{col}" stroke="{lnc}" stroke-width="0.35"/>')
    return s


def stephane(C, color=None, points=False):
    col = color or C['fig']
    if points:
        d = ("M58.2,29.6 L56.5,20.5 L54.2,27.2 L51.4,18.8 L49.6,27.8 L46.2,19.6 L45.4,29.4 "
             "L41.2,22.6 L41.4,31.8 L37.2,26.8 L38.2,34.4 C44,31.8 51,30 58.2,29.6 Z")
        return P(d, col, C['ln'], 0.7) + P("M38.2,34.4 C44,31.8 51,30 58.2,29.6", 'none', C['ln'], 0.9)
    d = "M58,30 C57,25 54.5,22 51,21.4 C45,22.4 39.5,26.4 35.6,31.6 L37.2,35 C43,31.4 50.5,29.6 58,30 Z"
    s = P(d, col, C['ln'], 0.7)
    for x, y in [(54.5, 25.4), (50.4, 26.2), (46.4, 27.8), (42.6, 30)]:
        s += C_(x, y, 0.9, C['ln'])
    return s


def veil(C, fill=None):
    f = fill or C['fig']
    d = ("M59.6,30.2 C58.6,22 50.6,16.6 41.6,18.2 C31.4,20.2 25.4,30.6 25.6,43.6 "
         "C25.8,54.6 29.2,62.6 27.4,72.6 C26.2,80 21.6,88 17,100 L46,100 "
         "C41.6,93 39.6,86 40.6,79.4 C41.4,73.8 40.6,69.4 38.8,66.2 "
         "C34.2,60 33.4,51.4 35.2,43.8 C37.2,36.2 43.2,30.6 51.4,29.4 "
         "C54.4,29 57.2,29.4 59.6,30.2 Z")
    s = P(d, f, C['ln'], 0.8)
    s += P("M33,24 C29.5,32 28.6,44 30.4,56 C31.6,64 31,74 26.6,86", 'none', C['ln'], 0.6)
    s += P("M40.6,19.4 C35,26 32.6,36 33.2,46", 'none', C['ln'], 0.6)
    s += P("M59.6,30.2 C57,29.2 53.4,28.8 51.4,29.4", 'none', C['ln'], 1.4)
    # dotted hem
    for i in range(7):
        t = i / 6
        x = 58.6 - t * 17.4 + (t * t) * 2
        y = 29.4 - 9 * (4 * t * (1 - t)) + 0.5
        s += C_(round(x, 2), round(y, 2), 0.55, C['ln'])
    return s


def front_hair_under(C):
    """A sliver of hair visible under a veil / cap at the forehead."""
    return P("M58.8,30.6 C57.2,32.4 55,33.6 52.2,34.2 C51.8,32.8 52,31.2 52.6,30 "
             "C54.8,29.6 57,29.8 58.8,30.6 Z", C['hair'], C['hl'], 0.5)


def pilos(C):
    s = P("M30.6,43.4 C30.2,31 36.6,16.6 46.8,6.2 C53.4,13.8 58.8,23.6 59.8,33 C51,36.6 40,40.6 30.6,43.4 Z",
          C['fig'], C['ln'], 0.9)
    s += P("M31.2,39.6 C40.4,37 50.6,33.4 59.6,29.4", 'none', C['ln'], 1.1)
    s += P("M40,24 C43,20 45,14 46.8,6.6", 'none', C['ln'], 0.5)
    return s


def petasos(C):
    s = P("M26,30.6 C36,24 54,22 70,27.6 C66,31.2 58,32 48.6,32.4 C40,32.6 31,32.6 26,30.6 Z",
          C['fig'], C['ln'], 0.8)
    s += P("M36.4,27 C37,19.6 42.6,15.4 49,15.2 C55.6,15.2 59.6,19.6 60.2,25.4", C['fig'], C['ln'], 0.8)
    s += P("M36.8,26 C44,23.4 52,23.2 60,24.8", 'none', C['ln'], 1.2)
    # wing
    s += P("M40.4,20 C35,15 29,12.4 22.6,12.6 C26,14.6 28,16 29.2,17.4 C26.6,17.2 24,17.6 21.6,18.6 "
           "C25.6,19.6 28.2,20.8 30,22 C28,22.4 26.2,23.2 24.6,24.4 C30.6,24.8 35.6,23.8 40.4,20 Z",
           C['fig'], C['ln'], 0.7)
    s += P("M39,20.4 C34,18.8 30,18.4 26,18.6 M38,21.8 C34,21.6 30.6,22.2 28,23.4", 'none', C['ln'], 0.45)
    return s


def attic_helmet(C, crest=True):
    s = ''
    if crest:
        s += P("M57.6,21.4 C56.4,10 44.6,3.2 32,7.2 C22.4,10.4 16.8,20 17.2,33.6 L22.4,35.4 "
               "C21.8,25.6 25.4,17.6 32.8,14 C41.2,10.2 50,13.8 52.6,22.8 Z",
               C['fig'], C['ln'], 0.8)
        for i in range(8):
            a = i / 7
            x1 = 55 - a * 33; y1 = 18 - 9 * (4 * a * (1 - a)) + a * 12
            x2 = 50.8 - a * 27; y2 = 21.8 - 7 * (4 * a * (1 - a)) + a * 12.5
            s += P(f"M{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f}", 'none', C['ln'], 0.5)
    s += P("M30.4,45.2 C28.8,33 36.2,23 47.6,21.4 C56,20.4 61.8,24.8 63,31.4 L66.4,34.8 "
           "C61,36.2 54.2,36.4 48,39 C41.8,41.6 36,44 30.4,45.2 Z", C['fig'], C['ln'], 0.9)
    s += P("M37.6,40.6 C44,36.8 53,33.6 62.8,32.6", 'none', C['ln'], 1.1)
    s += P("M48,39 C51,42.4 51.6,46.8 49.6,50.6 C45.8,49.4 43.2,45.8 42.8,41.4 Z", C['fig'], C['ln'], 0.8)
    s += P("M36,30 C40,27 45,25.6 50,25.6", 'none', C['ln'], 0.5)
    return s


def goat_cap(C):
    s = P("M31.2,44.4 C29.4,33 36.6,22.6 48.4,21.4 C56.4,20.8 60.6,25.4 61,31.6 "
          "C51.6,34.2 40.6,39 31.2,44.4 Z", C['fig'], C['ln'], 0.8)
    for (x, y) in [(38, 30), (43, 27), (48, 25.2), (53, 25.4), (57, 27.6), (35, 36.4), (40, 33.8),
                   (45, 31), (50, 29.2), (55, 29.6), (36.4, 41.2), (41.6, 38.4)]:
        s += P(f"M{x-1.2},{y-0.6} L{x},{y+0.8} L{x+1.2},{y-0.6}", 'none', C['ln'], 0.5)
    return s


def sakkos(C):
    d = ("M58.4,30 C56.4,24 49.6,20.6 42.6,21.6 C32.6,22.8 24.4,30.6 23.6,40.6 "
         "C23,48.6 27.6,54.6 34.6,55.6 C38.6,56.2 42.6,54.8 45.4,52.2 "
         "C46.6,46 47.8,40.4 50.4,37.2 C53.6,35.8 56.4,33.4 58.4,30 Z")
    s = P(d, C['fig'], C['ln'], 0.8)
    for dd in ["M28,31 C34,34 38,40 39,48", "M34,24.6 C40,28.6 44.6,34 46,42", "M25,40 C30,42 34,46 36,54"]:
        s += P(dd, 'none', C['ln'], 0.7)
    for (x, y) in [(31, 37), (36.6, 33), (41.6, 30.6), (30.6, 46), (38, 42), (44, 37.4), (35, 50)]:
        s += C_(x, y, 0.8, C['ln'])
    s += P("M58.4,30 C55.6,32 52.4,34.6 50.4,37.2", 'none', C['ln'], 1.3)
    return s


# ---- attributes
def spear(C, x0=74, y0=100, x1=86, y1=8, head=True):
    s = P(f"M{x0},{y0} L{x1},{y1+12}", 'none', C['obj'], 1.8)
    if head:
        s += P(f"M{x1},{y1} C{x1+2.8},{y1+5} {x1+2.6},{y1+10} {x1+0.6},{y1+14} L{x1-1.6},{y1+13.6} "
               f"C{x1-2.6},{y1+9.6} {x1-2},{y1+4.6} {x1},{y1} Z", C['fig'], C['ln'], 0.6)
        s += P(f"M{x1-0.1},{y1+3} L{x1-0.3},{y1+13}", 'none', C['ln'], 0.5)
    return s


def scepter(C, x0=77, y0=100, x1=84, y1=12, lotus=False):
    s = P(f"M{x0},{y0} L{x1},{y1+6}", 'none', C['obj'], 2.2)
    for k in (0.25, 0.5):
        yy = y1 + 6 + (y0 - y1 - 6) * k
        xx = x1 + (x0 - x1) * ((yy - y1 - 6) / (y0 - y1 - 6))
        s += P(f"M{xx-2.2},{yy} L{xx+2.2},{yy}", 'none', C['obj'], 1.4)
    if lotus:
        s += P(f"M{x1},{y1+7} C{x1-4},{y1+5} {x1-4.4},{y1+1} {x1-3},{y1-2} C{x1-1.6},{y1+1} {x1-1},{y1+3} {x1},{y1+4} "
               f"C{x1+1},{y1+3} {x1+1.6},{y1+1} {x1+3},{y1-2} C{x1+4.4},{y1+1} {x1+4},{y1+5} {x1},{y1+7} Z",
               C['fig'], C['ln'], 0.5)
        s += P(f"M{x1},{y1+4} L{x1},{y1-3.4}", 'none', C['fig'], 1.4)
    else:
        s += C_(x1, y1 + 3, 3.2, C['acc'] if C['fig'] == C['bg'] else C['fig'], C['ln'], 0.6)
    return s


def trident(C):
    s = P("M73,100 L83.6,24", 'none', C['fig'], 2.2)
    s += P("M75.4,27.2 C77,29.4 81,30.2 84,30 C87.6,29.8 91,28.6 92.6,26", 'none', C['fig'], 2.2)
    for (bx, by, tx, ty) in [(75.4, 27.2, 76.6, 8), (84, 30, 85.6, 4), (92.6, 26, 94.6, 9)]:
        s += P(f"M{bx},{by} L{tx},{ty+5}", 'none', C['fig'], 1.8)
        s += P(f"M{tx},{ty} L{tx+2.4},{ty+6.4} L{tx+0.2},{ty+5.2} L{tx-2},{ty+6.6} Z", C['fig'], C['ln'], 0.4)
    return s


def thunderbolt(C):
    s = ''
    # central spindle
    s += P("M84,50 C87.6,42 87.6,34 85,24 C83.4,20 82.2,19 82.2,19 C82.4,26 80.6,34 80.4,42 C80.6,46 82,48.6 84,50 Z",
           C['fig'], C['ln'], 0.6)
    s += P("M84,50 C80.4,58 80.4,66 83,76 C84.6,80 85.8,81 85.8,81 C85.6,74 87.4,66 87.6,58 C87.4,54 86,51.4 84,50 Z",
           C['fig'], C['ln'], 0.6)
    s += P("M79.6,49.4 L88.4,50.6", 'none', C['fig'], 2.4)
    # zigzag prongs
    s += P("M81.6,22 L76,17 L79.2,15.4 L73.4,9", 'none', C['fig'], 1.3)
    s += P("M84.6,22 L90,16.4 L86.8,14.8 L92.4,8.6", 'none', C['fig'], 1.3)
    s += P("M86.4,78 L92,83 L88.8,84.6 L94.6,91", 'none', C['fig'], 1.3)
    s += P("M83.4,78 L78,83.6 L81.2,85.2 L75.6,91.4", 'none', C['fig'], 1.3)
    s += P("M82.2,19 L82.2,6 M85.8,81 L85.8,94", 'none', C['fig'], 1.2)
    return s


def caduceus(C):
    s = P("M74,100 L81.4,30", 'none', C['fig'], 1.9)
    s += C_(81.8, 26, 4.2, 'none', C['fig'], 1.6)
    s += P("M78.4,23.6 C76,19.6 76.8,15 80,13.4 M85.2,23.6 C87.8,19.8 87.6,15.2 84.4,13.2", 'none', C['fig'], 1.6)
    return s


def owl(C, x=80, y=78, s=1.0):
    g = f'<g transform="translate({x} {y}) scale({s})">'
    g += P("M-7,10 C-9,2 -8,-6 -5.6,-9.4 L-4.6,-13 L-2,-9.8 C-0.6,-10.2 0.6,-10.2 2,-9.8 L4.6,-13 L5.6,-9.4 "
           "C8,-6 9,2 7,10 Z", C['fig'], C['ln'], 0.6)
    g += C_(-2.6, -6, 2.4, C['bg'] if C['fig'] != C['bg'] else C['wh'], C['ln'], 0.5)
    g += C_(2.6, -6, 2.4, C['bg'] if C['fig'] != C['bg'] else C['wh'], C['ln'], 0.5)
    g += C_(-2.6, -6, 0.9, C['fig']) + C_(2.6, -6, 0.9, C['fig'])
    g += P("M0,-4.4 L-0.9,-2.6 L0,-1.4 L0.9,-2.6 Z", C['ln'])
    g += P("M-4.6,1 C-3,2.6 -1.6,2.6 0,1 C1.6,2.6 3,2.6 4.6,1 M-4.6,4.6 C-3,6.2 -1.6,6.2 0,4.6 C1.6,6.2 3,6.2 4.6,4.6",
           'none', C['ln'], 0.5)
    g += '</g>'
    return g


def bow(C):
    s = P("M81,8 C90,18 76,30 81.6,50 C76,70 90,82 81,92", 'none', C['fig'], 2.6)
    s += P("M81,8 L81,92", 'none', C['fig'], 0.6)
    s += P("M79.8,48 L83.4,48 M79.8,52 L83.4,52", 'none', C['ln'], 0.8)
    return s


def loom(C):
    s = P("M68,13 L98,13", 'none', C['fig'], 3)
    s += P("M68,13 L98,13 L98,26 L68,26 Z", C['fig'], C['ln'], 0.5)
    for y in (16, 19, 22):
        s += P(f"M68,{y} L98,{y}", 'none', C['ln'], 0.4)
    for i, x in enumerate(range(70, 98, 3)):
        s += P(f"M{x},26 L{x},{70 + (i % 2) * 5}", 'none', C['fig'], 0.7)
        yy = 70 + (i % 2) * 5
        s += P(f"M{x-1.3},{yy+5} L{x-0.5},{yy} L{x+0.5},{yy} L{x+1.3},{yy+5} Z", C['fig'], C['ln'], 0.4)
    s += P("M67,50 L99,50", 'none', C['fig'], 1.2)
    return s


def pear_branch(C):
    s = P("M98,70 C90,64 83,58 76,48", 'none', C['fig'], 1.3)
    for (x, y, a) in [(86, 60, -30), (80, 52, 20), (92, 66, 40), (79, 45, -50)]:
        s += f'<ellipse cx="{x}" cy="{y}" rx="4.2" ry="1.9" transform="rotate({a} {x} {y})" fill="{C["fig"]}" stroke="{C["ln"]}" stroke-width="0.4"/>'
    s += P("M86.4,62 L86.8,66 C83.6,67.4 82.4,71.6 84.4,74.6 C86.4,77.6 90.6,77.4 92.2,74.2 "
           "C93.6,71.2 91.6,67.6 88.4,66.4 L87.6,62 Z", C['fig'], C['ln'], 0.6)
    return s


def basin(C):
    g = '<g transform="translate(-4 -8)">'
    g += P("M66,76 C66,85 73.6,90.4 82,90.4 C90.4,90.4 98,85 98,76 Z", C['fig'], C['ln'], 0.7)
    g += P("M64.6,76 L99.4,76", 'none', C['ln'], 1.6)
    g += P("M69,80.4 C75,82.4 89,82.4 95,80.4", 'none', C['ln'], 0.5)
    g += P("M76.6,90.2 L75.6,95 L88.4,95 L87.4,90.2", C['fig'], C['ln'], 0.6)
    g += P("M70,71.6 C72,70 74,70 76,71.6 M82,70.6 C84,69 86,69 88,70.6 M91,72 C92.4,70.8 94,70.8 95.4,72", 'none', C['fig'], 0.8)
    g += '</g>'
    return g


def pig(C):
    return '<g transform="translate(74 70) scale(1.25) translate(-83 -80)">' + _pig(C) + '</g>'


def _pig(C):
    s = P("M68,93 C66,84 70.6,75.6 79,73.2 C85,71.6 90.6,72.8 93.6,75.8 L97.6,76.8 "
          "C98.8,78.4 98.8,81.8 97.6,83.4 L94,84.2 C92,89 86,93.2 78,93.4 C74,93.4 70.6,93.8 68,93 Z",
          C['fig'], C['ln'], 0.7)
    s += P("M78.6,73.4 C79.6,68 83.2,65.2 86.8,64.6 C86,68.6 84.8,71.6 82.6,73.8 Z", C['fig'], C['ln'], 0.6)
    s += C_(88.4, 77.2, 0.9, C['ln'])
    s += P("M97.6,76.8 L97.6,83.4 M95.4,79.4 L95.8,80.6", 'none', C['ln'], 0.7)
    s += P("M91,86 C89,87.4 86.6,87.6 84.6,87", 'none', C['ln'], 0.5)
    s += P("M72,78 L73,76.6 M75,76.2 L76,74.8 M70,81 L71,79.6", 'none', C['ln'], 0.5)
    return s


def goat(C):
    return '<g transform="translate(75 68) scale(1.2) translate(-82 -82)">' + _goat(C) + '</g>'


def _goat(C):
    s = P("M70,96 C68,88 70,80 75,76 C78,73.6 82,72.6 85,73.4 L94,79 C96,80.2 96.6,82.6 95.4,84.2 "
          "L91,86 C89.4,86.8 88,88.4 87.4,90 C86,94 81,96.4 76,96.4 C73,96.4 71.6,96.4 70,96 Z",
          C['fig'], C['ln'], 0.7)
    s += P("M80.6,74.4 C79.4,66 74.4,59.6 65.6,57.6 C71.6,62 75,67.4 76.6,75.4 Z", C['fig'], C['ln'], 0.6)
    s += P("M78.4,62.6 L76.6,64.4 M80,66.4 L77.8,67.6 M80.8,70.4 L78.6,71.2", 'none', C['ln'], 0.5)
    s += P("M77.6,77.4 C73,77 70.2,78.8 69.2,81.2 C72.4,81.2 75,80.4 77.4,79.2 Z", C['fig'], C['ln'], 0.5)
    s += P("M87.8,89 C88.8,92.8 87.8,96.6 85.2,99.8 C83.8,96.4 84.6,92.4 86,89.6 Z", C['fig'], C['ln'], 0.5)
    s += C_(85.4, 77.8, 0.9, C['ln'])
    s += P("M93.2,80.4 L94,81.4", 'none', C['ln'], 0.6)
    return s


def bucranium(C):
    s = P("M74,74 C74,70 78,67.4 82,67.4 C86,67.4 90,70 90,74 C90,80 86.4,84 84.8,92 L79.2,92 "
          "C77.6,84 74,80 74,74 Z", C['fig'], C['ln'], 0.7)
    s += P("M74.6,71.6 C68.6,70.6 65.6,65 67,59 C69.8,63.2 72.4,65.4 76,66.4", C['fig'], C['ln'], 0.6)
    s += P("M89.4,71.6 C95.4,70.6 98.4,65 97,59 C94.2,63.2 91.6,65.4 88,66.4", C['fig'], C['ln'], 0.6)
    s += C_(78.6, 74.6, 1.2, C['ln']) + C_(85.4, 74.6, 1.2, C['ln'])
    s += P("M80.4,88 L80.8,90 M83.6,88 L83.2,90", 'none', C['ln'], 0.7)
    return s


def kantharos(C):
    s = P("M67,55.6 C67,63.6 71.4,68 77.6,68 C83.8,68 88.2,63.6 88.2,55.6 Z", C['fig'], C['ln'], 0.7)
    s += P("M67,55.6 C61.4,52.6 61.8,43.4 68.4,43.2 M88.2,55.6 C93.8,52.6 93.4,43.4 86.8,43.2",
           'none', C['fig'], 1.5)
    s += P("M75.6,68 L79.6,68 L80.6,74 L74.6,74 Z", C['fig'], C['ln'], 0.5)
    s += P("M71.6,76 C74,74.6 81.4,74.6 83.6,76 L83.6,77.4 L71.6,77.4 Z", C['fig'], C['ln'], 0.5)
    s += P("M69,59.6 C74,61.4 81,61.4 86.2,59.6", 'none', C['ln'], 0.6)
    return s


def kylix_wand(C):
    s = P("M64.6,62 L96,26", 'none', C['fig'], 1.3)
    s += P("M66,58 C66,62.6 72,65.4 80,65.4 C88,65.4 94,62.6 94,58 Z", C['fig'], C['ln'], 0.7)
    s += P("M66,58 C62,57 61.6,53.4 64.6,53.4 M94,58 C98,57 98.4,53.4 95.4,53.4", 'none', C['fig'], 1.3)
    s += P("M78.6,65.4 L78.6,71 L81.4,71 L81.4,65.4", C['fig'], C['ln'], 0.5)
    s += P("M74.6,73 C76,71.4 84,71.4 85.4,73 Z", C['fig'], C['ln'], 0.5)
    s += P("M70.6,56 C74,54 77,57.4 80,55.6 C83,54 86,56.6 89.6,55.4", 'none', C['fig'], 0.7, ' opacity=".8"')
    return s


def necklace(C):
    s = P("M70,34 C68,56 74,72 84,74 C92,75 97,62 97,40", 'none', C['fig'], 0.5)
    import math
    for i in range(13):
        t = i / 12
        x = (1 - t) ** 3 * 70 + 3 * (1 - t) ** 2 * t * 68 + 3 * (1 - t) * t * t * 74 + t ** 3 * 84
        y = (1 - t) ** 3 * 34 + 3 * (1 - t) ** 2 * t * 56 + 3 * (1 - t) * t * t * 72 + t ** 3 * 74
        s += C_(round(x, 2), round(y, 2), 1.9 if i % 2 else 1.4, C['acc'] if i % 2 else C['wh'], C['ln'], 0.4)
    for i in range(1, 9):
        t = i / 9
        x = (1 - t) ** 3 * 84 + 3 * (1 - t) ** 2 * t * 92 + 3 * (1 - t) * t * t * 97 + t ** 3 * 97
        y = (1 - t) ** 3 * 74 + 3 * (1 - t) ** 2 * t * 75 + 3 * (1 - t) * t * t * 62 + t ** 3 * 40
        s += C_(round(x, 2), round(y, 2), 1.9 if i % 2 else 1.4, C['acc'] if i % 2 else C['wh'], C['ln'], 0.4)
    s += P("M84,76 C82.6,79 83,82 84.6,84 C86.2,82 86.4,79 84.8,76 Z", C['acc'], C['ln'], 0.5)
    return s


def key(C):
    s = P("M74,98 L82.6,30", 'none', C['fig'], 2)
    s += P("M82.6,30 C83.2,25 86.8,21.6 91.4,22.4 C95,23 96,27 94,30.4 L91.6,34.4", 'none', C['fig'], 2)
    s += P("M91.6,34.4 L88.6,35.8 M91.6,34.4 L93.6,37.6", 'none', C['fig'], 1.4)
    s += P("M76.6,78 C73,80 71.6,84 72.4,88 M76,82.6 C74,86 74,90 75.4,93", 'none', C['fig'], 0.8)
    s += C_(77, 76.6, 1.8, C['fig'], C['ln'], 0.5)
    return s


def ball(C):
    s = C_(83, 66, 8.2, C['fig'], C['ln'], 0.7)
    s += P("M75.4,63 C79,66 87,66 90.6,63 M75.4,69.4 C79,66.4 87,66.4 90.6,69.4 M83,57.8 C80,62 80,70 83,74.2 M83,57.8 C86,62 86,70 83,74.2",
           'none', C['ln'], 0.5)
    s += P("M72,53 C73,51 75,50.4 76.6,51.4 M69.6,58 C70,56.4 71.2,55.6 72.6,55.8", 'none', C['fig'], 0.7, ' opacity=".7"')
    return s


def vine(C):
    s = P("M98,94 C90,86 88,74 91,62 C93,52 90,42 84,34 C80,29 78,24 79,18", 'none', C['fig'], 1.8)
    s += P("M91,62 C86,60 84,56 84.6,52", 'none', C['fig'], 0.8)
    for (x, y, a) in [(86, 45, -20), (93, 72, 30), (80, 24, -40)]:
        s += (f'<g transform="rotate({a} {x} {y})">'
              + P(f"M{x},{y+4} C{x-5},{y+3} {x-6},{y-2} {x-3},{y-3} C{x-3},{y-6} {x},{y-6.4} {x},{y-4} "
                  f"C{x},{y-6.4} {x+3},{y-6} {x+3},{y-3} C{x+6},{y-2} {x+5},{y+3} {x},{y+4} Z", C['fig'], C['ln'], 0.5)
              + '</g>')
    for (x, y) in [(80.6, 56), (83.4, 56.4), (78.8, 58.8), (81.8, 59.2), (84.6, 59.4), (80.2, 61.8), (83, 62.2),
                   (81.4, 64.8), (86.4, 56.6)]:
        s += C_(x, y, 1.6, C['fig'], C['ln'], 0.5)
    return s


def prow(C):
    return '<g transform="translate(-9 -17)">' + _prow(C) + '</g>'


def _prow(C):
    s = P("M58,98 C64,94 72,92 82,91 C88,90.4 92,88 94,84 C95.4,80.6 95,76.4 93.6,72.8 "
          "C96.6,73.6 98.6,76.4 99,80 C99.6,86 97,92.6 92,96 C88,98.6 84,100 80,100 L58,100 Z",
          C['fig'], C['ln'], 0.7)
    s += P("M60,98.4 C68,95.6 78,94.4 88,93.6", 'none', C['ln'], 0.8)
    s += P("M86.6,86.4 C88.2,84.4 91.2,84.4 92.4,86.6 C91,88.6 88.2,88.8 86.6,86.4 Z", C['wh'], C['ln'], 0.5)
    s += C_(89.6, 86.5, 0.8, C['ln'])
    s += P("M93.6,72.8 C93.6,70 95.2,68.4 97,68.6", 'none', C['fig'], 1.2)
    return s


def sun_disc(C):
    s = ''
    import math
    cx, cy = 46, 42
    for k in range(18):
        a = -math.pi + k * (2 * math.pi / 18)
        if 0.35 < a < 2.6:  # skip rays behind neck/shoulder
            continue
        x1, y1 = cx + 30 * math.cos(a), cy + 30 * math.sin(a)
        x2, y2 = cx + 47 * math.cos(a), cy + 47 * math.sin(a)
        xl, yl = cx + 30 * math.cos(a - 0.09), cy + 30 * math.sin(a - 0.09)
        xr, yr = cx + 30 * math.cos(a + 0.09), cy + 30 * math.sin(a + 0.09)
        s += P(f"M{xl:.1f},{yl:.1f} L{x2:.1f},{y2:.1f} L{xr:.1f},{yr:.1f} Z", C['acc'])
    s += C_(cx, cy, 30, C['acc'], C['ln'], 0.6)
    s += C_(cx, cy, 26.5, 'none', C['ln'], 0.4)
    return s


def stake(C):
    s = P("M99,82 L71,40 L74.6,37.6 L102,78 Z", C['wh'] if False else '#6b4a2e', C['ln'], 0.6)
    s += P("M71,40 L68.6,33.6 L74.6,37.6 Z", C['red'], C['ln'], 0.5)
    s += P("M66,31.4 C64.4,29 66,27 67.4,29 C68,26.4 70.2,26.6 69.6,29.6", 'none', C['wh'], 0.9)
    return s


# ---------------------------------------------------------------- characters
def std_person(C, hair_kind='short', beard_kind=None, old=False, eye_kind='open', hair_col=None,
               beard_col=None, himation=False, show_ear=True):
    s = garment(C, himation=himation)
    s += head(C)
    s += hair(C, hair_kind, color=hair_col)
    if beard_kind:
        s += beard(C, beard_kind, color=beard_col)
    if show_ear:
        s += ear(C)
    s += eye(C, eye_kind)
    s += face_lines(C, old=old)
    return s


def build(pid, style):
    C = PAL[style] if isinstance(style, str) else style   # a palette key, or a palette dict (other books)
    bg = f'<rect width="100" height="100" fill="{C["bg"]}"/>'
    s = ''
    if pid == 'odysseus':
        s = bow(C) + std_person(C, 'short', 'short') + pilos(C)
    elif pid == 'penelope':
        s = loom(C) + garment(C) + head(C) + front_hair_under(C) + veil(C) + eye(C) + face_lines(C)
    elif pid == 'telemachus':
        s = spear(C, 72, 100, 86, 6) + std_person(C, 'short') + fillet(C)
    elif pid == 'laertes':
        s = pear_branch(C) + std_person(C, 'short', 'short', old=True, hair_col=C['wh'], beard_col=C['wh']) + goat_cap(C)
    elif pid == 'anticleia':
        s = garment(C) + head(C) + front_hair_under(C) + veil(C) + eye(C) + face_lines(C, old=True)
    elif pid == 'eurycleia':
        s = basin(C) + garment(C) + head(C) + front_hair_under(C) + sakkos(C) + eye(C) + face_lines(C, old=True)
    elif pid == 'eumaeus':
        s = std_person(C, 'short', 'short', himation=True) + pig(C)
    elif pid == 'melanthius':
        s = std_person(C, 'short', 'point') + goat(C)
        s += P("M53.6,39.6 L61,41.6", 'none', C['ln'], 1.0)   # scowl
    elif pid == 'argos':
        s = dog(C)
    elif pid == 'antinous':
        s = std_person(C, 'long') + wreath(C, C['wh']) + kantharos(C)
    elif pid == 'eurymachus':
        s = necklace(C) + std_person(C, 'short') + wreath(C)
    elif pid == 'mentor':
        s = '<g transform="translate(-6 2)">' + key(C) + '</g>' + std_person(C, 'short', 'short', himation=True, old=True)
    elif pid == 'nestor':
        s = scepter(C) + std_person(C, 'long', 'long', old=True, hair_col=C['wh'], beard_col=C['wh']) + fillet(C, C['fig'])
    elif pid == 'menelaus':
        s = scepter(C, lotus=True) + std_person(C, 'short', 'short', hair_col=C['acc'], beard_col=C['acc']) + stephane(C, C['fig'])
    elif pid == 'alcinous':
        s = std_person(C, 'short', 'short') + stephane(C, C['acc'], points=True) + prow(C)
    elif pid == 'nausicaa':
        s = garment(C) + head(C) + hair(C, 'bun') + ear(C) + fillet(C, C['fig'], 1.6) + eye(C) + face_lines(C) + ball(C)
    elif pid == 'tiresias':
        s = scepter(C, 75, 100, 82, 10) + std_person(C, 'long', 'long', old=True, eye_kind='closed', hair_col=C['wh'], beard_col=C['wh'])
    elif pid == 'eurylochus':
        s = spear(C, 20, 100, 30, 4) + std_person(C, 'short', 'short', show_ear=False) + attic_helmet(C, crest=False) + bucranium(C)
    elif pid == 'zeus':
        s = '<g transform="translate(-4 0)">' + thunderbolt(C) + '</g>' + std_person(C, 'long', 'long') + wreath(C)
    elif pid == 'athena':
        s = garment(C) + head(C) + hair(C, 'long') + attic_helmet(C) + eye(C) + face_lines(C) + owl(C, 79, 75, 1.05)
    elif pid == 'poseidon':
        s = trident(C) + std_person(C, 'long', 'long') + fillet(C)
    elif pid == 'hermes':
        s = caduceus(C) + std_person(C, 'short') + petasos(C)
    elif pid == 'helios':
        s = sun_disc(C) + std_person(C, 'short')
    elif pid == 'calypso':
        s = '<g transform="translate(-6 2)">' + vine(C) + '</g>' + garment(C) + head(C) + hair(C, 'long') + stephane(C) + eye(C) + face_lines(C)
    elif pid == 'circe':
        s = garment(C) + head(C) + hair(C, 'bun') + ear(C) + stephane(C) + eye(C) + face_lines(C) + kylix_wand(C)
    elif pid == 'polyphemus':
        s = polyphemus(C)
    elif pid == 'sirens':
        s = siren(C)
    elif pid == 'scylla':
        s = scylla(C)
    if pid not in ('polyphemus', 'sirens', 'scylla', 'argos'):
        s = f'<g transform="translate(48 50) scale(1.1) translate(-48 -50)">{s}</g>'
    return bg + s


# ---------------------------------------------------------------- specials
def dog(C):
    s = P("M14,100 C18,86 26,74 34,64 C38,58 41,51 44,44 C46,38 50,33.4 56,32.6 "
          "C61.6,32 66,34.6 69.6,38.6 C73,42 77,44.4 82,46 L90.4,48.6 C92.8,49.4 93.4,52.4 91.6,54.2 "
          "C89.4,56 86,56.8 82,57.6 L72,60 C67,61.6 62.6,63.6 60,67 C57.4,71 57,77 58.4,84 "
          "C59.6,90 62,95.6 64,100 Z", C['fig'], C['ln'], 0.8)
    # ear laid back
    s += P("M52.6,36 C48,35.4 42.6,38.4 39,43.6 C38,45.2 38.4,46.6 40,46.4 C45,45.6 49.6,42.6 53.6,39.4 Z",
           C['fig'], C['ln'], 0.7)
    s += C_(90.4, 51, 2.2, C['ln'])                               # nose
    s += P("M91,55 C85,57 78,58.6 71,59.4", 'none', C['ln'], 0.7)   # mouth
    s += P("M60.8,40.8 Q63.4,39.2 66,40.8 Q63.4,42.6 60.8,40.8 Z", 'none', C['ln'], 0.7)
    s += C_(64.2, 40.8, 0.9, C['ln'])
    s += P("M58.6,38 Q62.6,36.4 66.4,38.4", 'none', C['ln'], 0.6)
    # grey muzzle
    s += P("M72,50 C75,51 78,51.6 82,52 M74,53.6 C77,54.4 80,54.6 84,54.6", 'none', C['wh'], 0.7, ' opacity=".9"')
    # collar
    s += P("M36.6,62.6 C44,69 52,71.6 60,70.4", 'none', C['ln'], 3.2)
    for (x, y) in [(41, 66.4), (46.4, 69.2), (52, 70.6), (57.2, 70.6)]:
        s += C_(x, y, 0.8, C['fig'])
    # ribs / old age
    s += P("M30,82 C34,80 38,80 42,82 M27,88 C31,86 35,86 39,88", 'none', C['ln'], 0.6)
    return s


def polyphemus(C):
    g = '<g transform="translate(50 52) scale(1.14) translate(-48 -50)">'
    g += garment(C, folds=False)
    g += head(C)
    # shaggy hair
    g += P("M57.4,29.2 C56,32.6 53.6,35.2 50.6,36.8 C48.6,39.6 48,43 47.6,46 L47,50 C44.4,53 42,57.5 40.5,63.5 "
           "L38.8,66.2 C32,62 27,54 26,45 C25,38 27,30 33,25 C38,21 45,20 52,22 C55,23 56.8,26 57.4,29.2 Z",
           C['hair'], C['hl'], 0.6)
    for d in ["M30,30 L27,28 M29,38 L25.6,37.6 M29,46 L25.6,47 M31,54 L27.6,56 M37,24 L35.6,20.6 M45,22 L45,18.4"]:
        g += P(d, 'none', C['hair'], 1.6)
    g += P("M34,34 C37,37 40,37 43,35 M32,44 C35,46 38,46 41,44 M34,54 C37,55 39,55 42,53", 'none', C['hl'], 0.5)
    g += beard(C, 'long', color=C['red'])
    g += ear(C)
    g += face_lines(C)
    # brow & single eye on the forehead
    g += P("M53.2,32.6 Q58.6,29.6 63.6,33", 'none', C['ln'], 1.0)
    g += P("M54.6,35.8 Q58.8,31.8 62.8,35.4 Q58.8,39.4 54.6,35.8 Z", C['wh'], C['ln'], 0.6)
    g += C_(59.8, 35.6, 1.6, C['fig'])
    g += '</g>'
    g += stake(C)
    return g


def small_female_head(C, tx, ty, sc, skin=None):
    """Female head reused at small scale (sirens, scylla); skin white per black-figure convention."""
    Cw = dict(C)
    Cw['skin'] = skin or C['wh']
    Cw['ln'] = '#1f1612'
    g = f'<g transform="translate({tx} {ty}) scale({sc}) translate(-48 -46)">'
    g += P("M57,28 C59.6,32 61.2,36.5 62.2,41 L68,50.6 C68.6,51.9 67.6,53.2 65.3,53.3 "
           "C64.7,54.2 64.9,55.2 64.9,55.7 C64.4,56.5 63.5,57 62.5,57.2 C63.4,57.6 64.1,58.3 63.9,59.1 "
           "C63.3,60 62.5,60.4 62.3,60.9 C63.3,62.6 63.5,64.9 61.6,66.4 C60.1,67.5 58.3,67.9 57.1,68 "
           "C57.6,73 58.2,78 59.2,84 L40,84 C40.4,78 40,72 38.8,66 C33,60 30,50 32,41 "
           "C34,31 44,25 52,26 C54.5,26.4 56,27 57,28 Z", Cw['skin'], '#1f1612', 1.0)
    g += P(HAIR_LONG, C['hair'], C['hl'], 0.9)
    g += fillet(C, C['red'], 2.2)
    g += eye(Cw)
    g += P("M62.5,57.2 L60.6,57.5", 'none', '#1f1612', 1.0)
    g += '</g>'
    return g


def siren(C):
    s = ''
    # tail feathers
    s += P("M36,66 C26,66 16,70 8,78 C16,77 22,76.6 28,77 C20,80 14,85 10,91 C20,87 30,82 38,76 Z",
           C['fig'], C['ln'], 0.6)
    # body
    s += P("M34,70 C34,58 44,50 56,50 C66,50 74,56 76,64 C78,74 72,84 60,86 C48,88 36,82 34,70 Z",
           C['fig'], C['ln'], 0.6)
    # wing
    s += P("M40,62 C48,54 60,54 70,60 C64,62 60,66 57,72 C52,70 46,68 40,62 Z", C['red'], C['ln'], 0.6)
    for d in ["M44,64 C50,62 56,64 60,68", "M46,67 C52,66 56,68 58,71", "M40,70 C46,72 52,74 56,78",
              "M36,74 C44,78 52,80 58,82"]:
        s += P(d, 'none', C['ln'], 0.6)
    # legs & talons
    s += P("M52,86 L50,94 M60,86 L62,94", 'none', C['fig'], 1.8)
    s += P("M46.6,95 L50,94 L52.6,96 M58.6,95.6 L62,94 L65,95.6", 'none', C['fig'], 1.1)
    s += P("M40,97 L72,97", 'none', C['fig'], 1.2)
    # neck & head
    s += P("M62,52 C62,46 63.4,42 65,38 L72,40 C71,45 71,49 72.6,55 Z", C['wh'], '#1f1612', 0.8)
    s += small_female_head(C, 66, 30, 0.56)
    # aulos
    s += P("M73.4,31 L96,24 M73.4,32 L95.4,31.6", 'none', C['fig'], 1.2)
    s += C_(96, 24, 1.2, C['fig']) + C_(95.4, 31.6, 1.2, C['fig'])
    return s


def scylla(C):
    s = ''
    # coiling fish tail
    s += P("M40,70 C30,76 22,86 26,94 C29,99 36,99 40,95 C36,95 32,93 32,89 C32,83 40,78 48,76 Z",
           C['fig'], C['ln'], 0.6)
    s += P("M26,94 C20,96 16,94 14,90 C18,90 22,90 24,88", C['fig'], C['ln'], 0.6)
    # torso
    s += P("M38,78 C38,66 42,56 50,52 C58,56 62,66 62,78 C56,80 44,80 38,78 Z", C['wh'], '#1f1612', 0.8)
    s += P("M36,78 C44,82 56,82 64,78 L66,84 C56,88 44,88 34,84 Z", C['fig'], C['ln'], 0.6)

    # dog-headed necks
    def doghead(x, y, ang, sc=1.0):
        g = f'<g transform="translate({x} {y}) rotate({ang}) scale({sc})">'
        g += P("M-8,-3 C-6,-7 0,-8 4,-6 L12,-3.6 C13.4,-3.2 13.4,-1.6 12,-1.2 L5,0 L12.4,2.4 "
               "C13.4,2.8 13.2,4.2 12,4.4 L3,4.6 C-2,6 -6,5 -8,3 Z", C['fig'], C['ln'], 0.5)
        g += P("M-4,-6 L-6,-11 L-1,-7.4 Z", C['fig'], C['ln'], 0.5)
        g += C_(1.6, -3.6, 0.8, C['ln'])
        g += P("M6,0.4 L7,1.8 L8,0.6 L9,2 L10,0.8", 'none', C['wh'], 0.6)
        g += '</g>'
        return g
    necks = [("M44,76 C34,74 24,66 16,56", 14, 54, 200), ("M56,76 C66,74 76,68 84,58", 86, 56, -20),
             ("M58,80 C70,84 80,86 88,82", 90, 80, 10)]
    for d, x, y, a in necks:
        s += P(d, 'none', C['ln'], 5.4) + P(d, 'none', C['fig'], 4)
    s += doghead(14, 54, 200, 1.05) + doghead(86, 56, -20, 1.05) + doghead(90, 80, 10, 0.95)
    s += small_female_head(C, 50, 34, 0.62)
    return s


IDS = ['odysseus', 'penelope', 'telemachus', 'laertes', 'anticleia', 'eurycleia', 'eumaeus', 'melanthius',
       'argos', 'antinous', 'eurymachus', 'mentor', 'nestor', 'menelaus', 'alcinous', 'nausicaa', 'tiresias',
       'eurylochus', 'zeus', 'athena', 'poseidon', 'hermes', 'helios', 'calypso', 'circe', 'polyphemus',
       'sirens', 'scylla']


def symbols(styles):
    out = ['<clipPath id="pclip" clipPathUnits="objectBoundingBox"><circle cx=".5" cy=".5" r=".5"/></clipPath>']
    for pid in IDS:
        out.append(f'<symbol id="pt-{pid}" viewBox="0 0 100 100">'
                   f'<clipPath id="pc-{pid}"><circle cx="50" cy="50" r="50"/></clipPath>'
                   f'<g clip-path="url(#pc-{pid})">{build(pid, styles[pid])}</g></symbol>')
    return '\n'.join(out)
