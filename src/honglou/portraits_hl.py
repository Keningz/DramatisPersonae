# -*- coding: utf-8 -*-
"""Dream of the Red Chamber portraits in the manner of Sun Wen's (孙温) gongbi paintings of the novel.

Frontal busts in a 100x100 box: fine even ink outlines, flat mineral colours (azurite, malachite, cinnabar, ochre,
gold) on a silk ground. Women wear Han-style jackets, some with cloud collars (云肩), and their hair dressed in buns
with pins and flowers; men wear Qing hats and robes, as in Sun Wen's album. People are told apart by age, hair,
headgear, colours and one object each (Daiyu's flower hoe, Baochai's gold locket, Qingwen's torn fan ...).
"""

INK = '#2a211c'
SILK = '#efe5cd'
SKIN = '#f8e9dc'
SKIN_M = '#f3dcc6'
SKIN_OLD = '#efd8c2'
HAIR = '#211b18'
GREY = '#a29d95'
WHITEH = '#ebe7df'
WHITE = '#fbf8f1'
LIP = '#c8443d'
BLUSH = '#f0a39c'
GOLD = '#d4a640'
LGOLD = '#ecd38a'
PEARL = '#fbf6ea'
C = dict(
    zhu='#c0392b', yanzhi='#c64a64', tao='#ef9fae', xing='#f1a77e', huang='#e8c35a', ehuang='#f3dc8f',
    shiqing='#2f5b8c', qing='#4a7fb0', yuebai='#dfe8ea', bilv='#3f8a6d', shilv='#5aa082', danlv='#a9cfae',
    zi='#7b4c8c', ouhe='#c7a6c3', zhe='#a5673d', mi='#ecd9a6', hui='#9a968e', mo='#3a3532', hong='#b8322e',
    jiang='#8c2f3b', cha='#7d6a4f', tuo='#c98b4d', song='#8fb178', lan='#3c5c86', fen='#f4c2c7', bai='#f6f2ea',
    jin='#d4a640', yin='#cfd2d4', zong='#6b4a33', qianlan='#9fbad0', qianhuang='#f2e2a8', molv='#2e5a48',
)


def P(d, fill='none', stroke=INK, w=0.7, extra=''):
    st = f' stroke="{stroke}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"' if stroke else ''
    return f'<path d="{d}" fill="{fill}"{st}{extra}/>'


def Cc(x, y, r, fill='none', stroke=INK, w=0.6, extra=''):
    st = f' stroke="{stroke}" stroke-width="{w}"' if stroke else ''
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"{st}{extra}/>'


def El(x, y, rx, ry, fill, op=1.0, rot=0, stroke=None, w=0.6):
    tr = f' transform="rotate({rot} {x} {y})"' if rot else ''
    st = f' stroke="{stroke}" stroke-width="{w}"' if stroke else ''
    return f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{fill}" opacity="{op}"{st}{tr}/>'


def G(s, tr):
    return f'<g transform="{tr}">{s}</g>'


def mir(s):
    return f'<g transform="matrix(-1 0 0 1 100 0)">{s}</g>'


def both(s):
    return s + mir(s)


# ================================================================== faces
FACES = {
    'f': "M50,33.5 C57.3,33.5 61.7,39.2 61.7,46.4 C61.7,53.6 57.6,60.6 50,61.9 C42.4,60.6 38.3,53.6 38.3,46.4 C38.3,39.2 42.7,33.5 50,33.5 Z",
    'm': "M50,32.6 C58.4,32.6 63.4,38.8 63.4,46.8 C63.4,54.8 58.8,62 50,63.4 C41.2,62 36.6,54.8 36.6,46.8 C36.6,38.8 41.6,32.6 50,32.6 Z",
    'c': "M50,37.4 C56.4,37.4 60.4,41.8 60.4,48.2 C60.4,54.4 56.4,59.4 50,60 C43.6,59.4 39.6,54.4 39.6,48.2 C39.6,41.8 43.6,37.4 50,37.4 Z",
    'p': "M50,32.8 C59.6,32.8 65,39 65,47.4 C65,55.6 60,62.4 50,63.4 C40,62.4 35,55.6 35,47.4 C35,39 40.4,32.8 50,32.8 Z",
}
NECK = "M45.8,58 L45.8,68 L54.2,68 L54.2,58 Z"
EAR = "M37,44.6 C34.8,44 33.8,46.2 34.3,48.8 C34.8,51.4 36,53 37.6,52.8"


def face(sp):
    kind = sp.get('face', 'f')
    sk = sp.get('skin') or (SKIN_OLD if sp.get('old') else SKIN_M if kind in ('m', 'p') else SKIN)
    s = P(NECK, sk, INK, 0.6)
    if sp.get('ears'):
        s += both(P(EAR, sk, INK, 0.6))
    s += P(FACES[kind], sk, INK, 0.75)
    dy = 1.6 if kind == 'c' else 0
    g = ''
    # blush
    if not sp.get('noblush'):
        g += both(El(42.6, 51.8, 3.4, 2.1, BLUSH, 0.32 if kind != 'm' else 0.16))
    # brows
    bcol = GREY if sp.get('old') else INK
    if kind in ('m', 'p') and not sp.get('fine'):
        g += both(P("M40,41.8 C42.4,40.2 45.6,40 47.9,41", 'none', bcol, 1.3))
    else:
        g += both(P("M39.9,42.5 C42.2,40.9 45.6,40.6 47.8,41.5", 'none', bcol, 0.7))
    # eyes
    eyes = sp.get('eyes', 'open')
    if eyes == 'down':
        g += both(P("M41.4,46.6 C43.4,47.8 45.6,47.8 47.3,46.6", 'none', INK, 0.85))
    elif eyes == 'side':     # glancing to the viewer's right
        g += both(P("M41.2,46.4 C42.8,45 45.4,44.8 47.3,46", 'none', INK, 0.9))
        g += Cc(45.6, 46.1, 1.0, INK, None) + Cc(56.9, 46.1, 1.0, INK, None)
    else:
        g += both(P("M41.3,46.5 C43.1,45.3 45.7,45.1 47.4,46.2 C45.8,47.1 43.2,47.3 41.3,46.5 Z", '#fffaf2', None)
                  + Cc(44.6, 46.15, 0.98, INK, None)
                  + P("M40.6,45.9 C41.2,46.2 41.6,46.4 41.3,46.5 C43.1,45.3 45.7,45.1 47.4,46.2", 'none', INK, 0.85)
                  + P("M42.2,46.95 C43.8,47.35 45.6,47.2 46.8,46.6", 'none', INK, 0.3))
    # nose and mouth
    g += P("M50.7,47.6 C50.3,50.2 49.5,52 48.9,52.8 C49.7,53.4 50.8,53.4 51.6,52.9", 'none', INK, 0.5)
    if sp.get('mouth') == 'frown':
        g += P("M47.4,57.6 C48.8,56.4 51.2,56.4 52.6,57.6", 'none', '#9a3b33', 0.9)
    elif sp.get('mouth') == 'smile':
        g += P("M47.2,56.4 C48.8,58 51.2,58 52.8,56.4", 'none', '#9a3b33', 0.9)
    elif kind in ('m', 'p') and not sp.get('fine'):
        g += P("M47.2,56.8 C49,57.4 51,57.4 52.8,56.8", 'none', '#9a3b33', 0.9)
    else:
        g += P("M47.7,56.5 C48.9,56 49.5,56.3 50,56.6 C50.5,56.3 51.1,56 52.3,56.5 C51.3,58.1 48.7,58.1 47.7,56.5 Z", LIP, None)
    if sp.get('old'):
        g += both(P("M42.2,49.6 C43.4,50.4 45,50.6 46.4,50.2", 'none', INK, 0.35)
                  + P("M46.2,53.4 C45.2,55.4 45.4,57.6 46.6,59", 'none', INK, 0.4))
        g += P("M44,37.6 C47,36.8 53,36.8 56,37.6", 'none', INK, 0.35)
    if sp.get('mole'):
        g += Cc(50, 43.4, 0.75, '#c8323a', None)
    if dy:
        g = G(g, f'translate(0 {dy})')
    return s + g


# ================================================================== hair (women)
HAIR_BASE = ("M37.4,48 C36,38 41.4,30.8 50,30.6 C58.6,30.8 64,38 62.6,48 C61.6,42.6 57.8,37.6 52,36.6 "
             "L50,38 L48,36.6 C42.2,37.6 38.4,42.6 37.4,48 Z")
LOCK = "M38.4,44 C37,49 37.2,54.6 39,58.8 C39.4,54.6 39.2,49.4 39.6,45"
BUNS = {
    'gao': "M43,32.4 C41.6,24.6 44.6,18.2 50,18 C55.4,18.2 58.4,24.6 57,32.4 Z",
    'yun': "M39.8,33.6 C34.6,28.6 38,20.2 44.8,22.4 C46.2,17.2 53.8,17.2 55.2,22.4 C62,20.2 65.4,28.6 60.2,33.6 C56,30.8 44,30.8 39.8,33.6 Z",
    'duo': "M43.6,32.4 C40,26 43.6,19.4 51,20.4 C58.6,21.4 64,27.4 61.8,34.8 C58.4,31.4 50,30.6 43.6,32.4 Z",
    'dan': "M44.2,32 C43.4,26.6 46.4,23.4 50,23.4 C53.6,23.4 56.6,26.6 55.8,32 Z",
    'pan': "M39.6,33.6 C40.6,27.4 44.8,25.2 50,25.2 C55.2,25.2 59.4,27.4 60.4,33.6 Z",
}


def hair_f(sp):
    col = sp.get('haircol', HAIR)
    style = sp.get('hair', 'dan')
    s = ''
    if style == 'shuang':                       # twin buns of a young maid
        s += both(Cc(41.4, 29.4, 5.4, col, INK, 0.6) + P("M38.4,32.6 C36.6,35.4 36.4,38.6 37.4,41", 'none', sp.get('ribbon', C['zhu']), 1.3))
    elif style == 'child':
        s += both(Cc(42.4, 33.6, 3.8, col, INK, 0.6) + P("M40,35.6 C39,37.4 39,39 39.6,40.4", 'none', sp.get('ribbon', C['zhu']), 1.2))
    elif style in BUNS:
        s += P(BUNS[style], col, INK, 0.6)
        if style == 'yun':
            s += P("M44.6,23 C46.4,26 48,28.4 50,29.4 C52,28.4 53.6,26 55.4,23", 'none', '#3c3430', 0.5)
        if style == 'gao':
            s += P("M46,22 C48,24 52,24 54,22", 'none', '#3c3430', 0.5)
    s += P(HAIR_BASE, col, INK, 0.6)
    if col == HAIR:
        s += both(P("M40.2,44.6 C40.2,38.6 44,34.4 48.6,33.4 M43.6,32.8 C46,31.6 48,31.4 49.4,31.4", 'none', '#5d534c', 0.3))
    if sp.get('locks', True):
        s += both(P(LOCK, col, None))
    if sp.get('fringe'):
        s += P("M40,42.2 C42.6,37.6 57.4,37.6 60,42.2 C57.6,40.8 55.6,41.6 53.8,40.6 C52.4,41.6 50.6,40.8 50,41.4 "
               "C49.4,40.8 47.6,41.6 46.2,40.6 C44.4,41.6 42.4,40.8 40,42.2 Z", col, None)
    return s


def pin(x1, y1, x2, y2, col=GOLD, bead=None):
    return P(f"M{x1},{y1} L{x2},{y2}", 'none', col, 1.1) + Cc(x2, y2, 1.4, bead or col, INK, 0.4)


def buyao(x, y, col=GOLD):
    """A dangling hair ornament: a pin with a short string of beads."""
    return (P(f"M{x},{y} L{x + 6},{y - 4}", 'none', col, 1.1) + Cc(x + 6, y - 4, 1.5, col, INK, 0.4)
            + P(f"M{x + 1},{y + 0.4} L{x + 1.4},{y + 7}", 'none', col, 0.5)
            + Cc(x + 1.4, y + 3.6, 0.8, PEARL, INK, 0.3) + Cc(x + 1.4, y + 7.2, 1.0, C['zhu'], INK, 0.3))


def flower(x, y, r=2.4, col=None, center=None):
    col = col or C['tao']
    s = ''.join(Cc(x + r * 0.62 * dx, y + r * 0.62 * dy, r * 0.55, col, INK, 0.3)
                for dx, dy in ((0, -1), (0.95, -0.31), (0.59, 0.81), (-0.59, 0.81), (-0.95, -0.31)))
    return s + Cc(x, y, r * 0.3, center or LGOLD, None)


def headband(col, jewel=C['zhu']):
    return (P("M38.8,40.4 C42.2,36.6 57.8,36.6 61.2,40.4 L60.8,37.8 C57.4,34 42.6,34 39.2,37.8 Z", col, INK, 0.5)
            + El(50, 36.2, 1.9, 1.5, jewel, 1, 0, INK, 0.4))


def phoenix_crown():
    s = P("M36.6,40 C35.4,27.4 41.6,20.4 50,20.4 C58.4,20.4 64.6,27.4 63.4,40 C58.6,35.4 41.4,35.4 36.6,40 Z", GOLD, INK, 0.6)
    s += P("M39,34.6 C44,31.6 56,31.6 61,34.6", 'none', '#9c7426', 0.6)
    s += P("M44.6,26.4 C46.4,23 49,22.6 50,24.6 C51,22.6 53.6,23 55.4,26.4 C53,25.4 51.4,27 50,29.4 C48.6,27 47,25.4 44.6,26.4 Z", '#b8322e', INK, 0.4)
    s += Cc(50, 21.2, 2.1, C['zhu'], INK, 0.4) + both(Cc(42.4, 29.6, 1.3, C['bilv'], INK, 0.3) + Cc(39.6, 33.6, 1.1, PEARL, INK, 0.3))
    s += both(P("M37.4,39 L36.6,52", 'none', LGOLD, 0.5) + Cc(36.6, 44, 0.9, PEARL, INK, 0.3) + Cc(36.5, 48, 0.9, PEARL, INK, 0.3)
              + Cc(36.5, 52.2, 1.1, C['zhu'], INK, 0.3))
    return s


def fengjie_crown():
    """金丝八宝攒珠髻，朝阳五凤挂珠钗 (ch. 3)."""
    s = ''
    for a, (x2, y2) in enumerate(((36, 22), (41.6, 16.4), (50, 14.2), (58.4, 16.4), (64, 22))):
        s += P(f"M50,28 L{x2},{y2}", 'none', GOLD, 1.0)
        s += P(f"M{x2 - 2.2},{y2 + 1.2} C{x2 - 1},{y2 - 2.2} {x2 + 1.8},{y2 - 2.2} {x2 + 2.4},{y2 + 0.4} "
               f"C{x2 + 1},{y2 + 0.2} {x2},{y2 + 1.4} {x2 - 2.2},{y2 + 1.2} Z", GOLD, INK, 0.35)
    s += P(BUNS['yun'], HAIR, INK, 0.6)
    s += ''.join(Cc(x, y, 1.0, LGOLD, '#9c7426', 0.3) for x, y in ((44, 26), (47, 23.6), (50, 22.6), (53, 23.6), (56, 26),
                                                                      (45.6, 29), (50, 27), (54.4, 29)))
    s += Cc(50, 25, 1.4, C['zhu'], INK, 0.3) + both(Cc(42.6, 30.6, 1.1, C['bilv'], INK, 0.3))
    s += both(P("M37.6,30 L35.6,41", 'none', LGOLD, 0.5) + Cc(35.6, 36, 0.8, PEARL, INK, 0.3) + Cc(35.5, 41.4, 1.0, PEARL, INK, 0.3))
    return s


def nun_hood(col):
    return (P("M35.4,60 C33.4,44 36.4,28.8 50,28 C63.6,28.8 66.6,44 64.6,60 L61.4,60 C62.6,50 61.4,40.4 56.6,36.6 "
              "C53,34.4 47,34.4 43.4,36.6 C38.6,40.4 37.4,50 38.6,60 Z", col, INK, 0.6)
            + P("M43.6,36.4 C47.4,35 52.6,35 56.4,36.4", 'none', WHITE, 1.4))


def headscarf(col):
    return (P("M37,46 C35.6,34.4 41.6,29 50,29 C58.4,29 64.4,34.4 63,46 C60.6,40.4 56,37.4 50,37.4 C44,37.4 39.4,40.4 37,46 Z", col, INK, 0.6)
            + P("M58.6,33.6 C62.6,30.6 66.6,31.4 67.6,34.6 C64.6,34 62,35 60.4,37.4 Z", col, INK, 0.5)
            + P("M41,34.4 C46,32.8 54,32.8 59,34.4", 'none', '#ffffff', 0.4, ' opacity=".5"'))


# ================================================================== hats (men)
def hat_guapi(col=HAIR, knot=C['zhu']):        # skullcap
    return (P("M36.8,41 C36.4,30.4 42.6,25.6 50,25.6 C57.4,25.6 63.6,30.4 63.2,41 C58.4,38.4 41.6,38.4 36.8,41 Z", col, INK, 0.6)
            + P("M37,40.8 C41.8,38.4 58.2,38.4 63,40.8", 'none', '#4a403a', 1.6)
            + P("M50,25.8 L50,38.6", 'none', '#4a403a', 0.4) + P("M43.2,27.6 C42,31 41.6,35 41.8,39.2", 'none', '#4a403a', 0.4)
            + P("M56.8,27.6 C58,31 58.4,35 58.2,39.2", 'none', '#4a403a', 0.4)
            + Cc(50, 25, 1.9, knot, INK, 0.4))


def hat_nuan(brim='#4a3626', top=None, bead=C['zhu'], plume=False):   # Qing winter hat
    s = ''
    if plume:
        s += P("M54,24 C62,20 72,22 78,30 C72,27 64,27 56,28 Z", C['bilv'], INK, 0.4) + Cc(74.4, 27.2, 2.2, C['shiqing'], C['huang'], 0.6)
    s += P("M38.8,36.8 C38.8,28.4 44,24.4 50,24.4 C56,24.4 61.2,28.4 61.2,36.8 Z", top or C['zhu'], INK, 0.5)
    s += ''.join(P(f"M50,24.6 L{x},36.4", 'none', '#8e2a24', 0.35) for x in (41, 44.4, 47.6, 52.4, 55.6, 59))
    s += P("M34.6,41.4 C34,35.2 39,32.8 50,32.8 C61,32.8 66,35.2 65.4,41.4 C60,38.8 40,38.8 34.6,41.4 Z", brim, INK, 0.6)
    s += Cc(50, 22.8, 2.4, bead, INK, 0.5) + P("M50,25.2 L50,26.4", 'none', GOLD, 1.2)
    return s


def hat_liang(bead=C['zhu']):                   # Qing summer hat: a cone with red tassels
    return (P("M33.6,41.6 L50,21.6 L66.4,41.6 C60,39.4 40,39.4 33.6,41.6 Z", '#f0e3b6', INK, 0.6)
            + ''.join(P(f"M50,22.6 L{x},{39.6 - abs(x - 50) * 0.05}", 'none', C['zhu'], 0.9) for x in (40, 43.4, 46.8, 50, 53.2, 56.6, 60))
            + Cc(50, 21, 2.3, bead, INK, 0.5))


def hat_rujin(col=HAIR, tail=True):             # soft scholar's cap
    s = ''
    if tail:
        s += both(P("M41,33 C36,36 33.6,44 34.4,52 C36,46 38.4,39.6 42.6,35.4 Z", col, INK, 0.5))
    s += P("M37.4,41 C36.6,31 41,25 50,24.6 C59,25 63.4,31 62.6,41 C58,38.6 42,38.6 37.4,41 Z", col, INK, 0.6)
    s += P("M43,26.4 C45,30 46,35 46,39.2 M57,26.4 C55,30 54,35 54,39.2", 'none', '#4a403a', 0.4)
    return s


def hat_wang():                                 # prince's cap with silver wings (ch. 15)
    return (both(P("M38,33.6 C31,30 26,28.8 22.6,30.6 C25.4,33.4 31,35 38.6,36.6 Z", C['yin'], INK, 0.5))
            + P("M37.2,40.4 C36,28 42,22 50,22 C58,22 64,28 62.8,40.4 C58,37.6 42,37.6 37.2,40.4 Z", WHITE, INK, 0.6)
            + P("M38,37.6 C42.8,34.8 57.2,34.8 62,37.6", 'none', C['yin'], 1.8)
            + Cc(50, 27.6, 2.4, C['zhu'], INK, 0.5) + both(Cc(44, 30, 1.2, PEARL, INK, 0.3))
            + P("M50,21.8 C48.6,18 51.4,16 53.4,17.6", 'none', C['zhu'], 1.0))


def hat_xiongjin(col=C['mo'], ball=C['zhu']):   # a swordsman's soft headband
    return (P("M37,40.6 C36.6,31 42,26 50,26 C58,26 63.4,31 63,40.6 C58,38 42,38 37,40.6 Z", col, INK, 0.6)
            + Cc(50, 26.4, 2.8, ball, INK, 0.5)
            + P("M62.4,37.8 C67,40 70,46 69.4,53 C67.8,48 65.6,43.4 61.6,40.6 Z", col, INK, 0.5))


def topknot(col=HAIR, crown=None, pinc=GOLD):
    s = P("M37.4,42 C36.6,31.4 42.4,27 50,27 C57.6,27 63.4,31.4 62.6,42 C58,38.6 42,38.6 37.4,42 Z", col, INK, 0.6)
    s += P("M45,28.6 C44.4,23.4 46.6,20.6 50,20.6 C53.4,20.6 55.6,23.4 55,28.6 Z", col, INK, 0.6)
    if crown:
        s += P("M45.6,25.6 L46.4,19.6 L50,22 L53.6,19.6 L54.4,25.6 Z", crown, INK, 0.5)
    s += P("M41.6,23.4 L58.6,22.2", 'none', pinc, 1.1)
    return s


def baoyu_hair(crown=GOLD):
    """束发嵌宝紫金冠，齐眉勒着二龙抢珠金抹额 (ch. 3)."""
    s = P("M37.2,43 C36.4,31.6 42.4,27 50,27 C57.6,27 63.6,31.6 62.8,43 C58.4,39.4 41.6,39.4 37.2,43 Z", HAIR, INK, 0.6)
    s += P("M44,30 L44.8,21.6 L47.4,24.6 L50,19.8 L52.6,24.6 L55.2,21.6 L56,30 C53,28.6 47,28.6 44,30 Z", crown, INK, 0.5)
    s += Cc(50, 25.6, 1.5, C['zhu'], INK, 0.3) + both(Cc(46.4, 27.4, 0.9, C['bilv'], INK, 0.3))
    s += P("M38.6,40.6 C42.4,37.2 57.6,37.2 61.4,40.6 L61,38.4 C57.4,35 42.6,35 39,38.4 Z", GOLD, INK, 0.5)
    s += both(P("M41.4,38.6 C43,37.6 44.6,37.4 46.2,37.8", 'none', '#9c7426', 0.5)) + Cc(50, 37, 1.6, PEARL, INK, 0.4)
    return s


def bald(scabs=False, col='#ead6c4'):
    s = P("M37.4,44 C36.6,32.4 42.4,26.4 50,26.4 C57.6,26.4 63.4,32.4 62.6,44 C58,40 42,40 37.4,44 Z", col, INK, 0.6)
    if scabs:
        s += ''.join(Cc(x, y, r, '#b8664f', None, 0, ' opacity=".7"') for x, y, r in ((44, 32, 1.4), (53, 29.6, 1.1), (57.6, 35, 1.3), (47.6, 36.4, 0.9)))
    return s


def old_hair_m(col=GREY):
    return P("M37,44 C36.4,32 42.4,27.6 50,27.6 C57.6,27.6 63.6,32 63,44 C61.4,40 58,38 54,39 C52.6,37.4 47.4,37.4 46,39 C42,38 38.6,40 37,44 Z",
             col, INK, 0.6) + P("M46,27.8 C46.6,24.4 53.4,24.4 54,27.8 Z", col, INK, 0.5)


# ================================================================== beards
def beard(kind, col=HAIR):
    if kind == 'mous':        # 八字须
        return both(P("M49.4,55.2 C46.6,54.8 43.6,56 41.8,58.4 C44.4,57.4 47,57 49.6,56.6 Z", col, None))
    if kind == 'short':
        return both(P("M49.4,55.2 C47,55 44.6,56 43.4,57.6 C45.6,57 47.6,56.8 49.6,56.6 Z", col, None)) + P("M48.6,59.4 C49.4,61.4 50.6,61.4 51.4,59.4 L50,63 Z", col, None)
    if kind == 'san':         # three long strands
        s = both(P("M49.4,55.2 C46.6,54.8 43.6,56 41.8,58.4 C44.4,57.4 47,57 49.6,56.6 Z", col, None))
        s += P("M48.4,59.6 C47.6,66 48.4,73 50,78 C51.6,73 52.4,66 51.6,59.6 Z", col, None)
        s += both(P("M42.4,58.4 C41.6,63 42.2,68 43.6,72 C44.4,67.4 44.4,62.4 44,58.6 Z", col, None))
        return s
    if kind == 'full':
        return (both(P("M49.4,55.2 C46.6,54.8 43.6,56 41.8,58.4 C44.4,57.4 47,57 49.6,56.6 Z", col, None))
                + P("M40.8,56.6 C40.6,64 44,71.4 50,74 C56,71.4 59.4,64 59.2,56.6 C56.6,60.6 53.4,62.6 50,62.6 C46.6,62.6 43.4,60.6 40.8,56.6 Z", col, None))
    if kind == 'stubble':
        return P("M40.6,54 C41.4,61.6 45,64.6 50,65.2 C55,64.6 58.6,61.6 59.4,54 C57,59.4 54,61.6 50,61.8 C46,61.6 43,59.4 40.6,54 Z", col, None, 0, ' opacity=".45"')
    if kind == 'scraggly':
        return (both(P("M49.4,55.4 C47,55.2 44.6,56.4 43,58.4", 'none', col, 0.9))
                + ''.join(P(f"M{x},59.6 C{x - 0.6},63 {x + 0.4},66 {x - 0.4},69", 'none', col, 0.8) for x in (45.6, 48, 50.4, 52.8, 55)))
    return ''


# ================================================================== clothes
SH = {
    'f': "M15,101 C17,84.4 30,76.4 42.4,73 L57.6,73 C70,76.4 83,84.4 85,101 Z",
    'm': "M10,101 C12,82.4 27,74.2 41,71.6 L59,71.6 C73,74.2 88,82.4 90,101 Z",
    'c': "M22,101 C23,88 33,80.4 43.4,77 L56.6,77 C67,80.4 77,88 78,101 Z",
}


def robe(sp):
    kind = sp.get('robe', 'f')
    col, trim = sp.get('col', C['tao']), sp.get('trim', C['shiqing'])
    sh = SH['c'] if sp.get('face') == 'c' else SH['m'] if kind in ('m', 'official', 'dao', 'jian', 'monk') else SH['f']
    s = P(sh, col, INK, 0.7)
    s += both(P("M15,101 C17,88 23,81 31,77.4 C27.4,83 25.6,91 26,101 Z", '#1a1210', None, 0, ' opacity=".13"'))
    if kind == 'f' and sp.get('motif', False):
        mc = sp.get('motifcol', LGOLD)
        s += ''.join(G(P("M0,-2.2 C1.2,-1 1.2,1 0,2.2 C-1.2,1 -1.2,-1 0,-2.2 Z M-2.2,0 C-1,-1.2 1,-1.2 2.2,0 C1,1.2 -1,1.2 -2.2,0 Z", mc, None, 0, ' opacity=".8"'),
                         f'translate({x} {y})') for x, y in ((22, 95), (30, 89), (70, 89), (78, 95), (35, 98), (65, 98)))
    # folds
    s += both(P("M24,96 C27,88.6 32.6,83.4 38.6,80.4", 'none', INK, 0.35, ' opacity=".6"'))
    if kind in ('f', 'maid'):
        s += P("M45.4,72.8 L50,81.2 L54.6,72.8 Z", WHITE, INK, 0.5)
        s += P("M43.8,72.6 L50,83.4 L56.2,72.6", 'none', trim, 3.2) + P("M42.6,72.6 L50,85.4 L57.4,72.6", 'none', INK, 0.4)
        if kind == 'f' and sp.get('yunjian', True):
            yc = sp.get('yjcol', trim)
            s += P("M29,84 C29,78.6 34.4,75.8 38.4,77 C39.6,73.8 43.6,72.8 45.6,74.4 L54.4,74.4 C56.4,72.8 60.4,73.8 61.6,77 "
                   "C65.6,75.8 71,78.6 71,84 C67,87.6 62.6,86.6 60.6,89.6 C57.6,92.8 53.4,91.6 50,94 C46.6,91.6 42.4,92.8 39.4,89.6 "
                   "C37.4,86.6 33,87.6 29,84 Z", yc, INK, 0.55)
            s += P("M33.6,83.4 C35.6,81 38.4,80.4 40.6,81.4 C42,79 45,78.4 47.4,79.4 M66.4,83.4 C64.4,81 61.6,80.4 59.4,81.4 "
                   "C58,79 55,78.4 52.6,79.4", 'none', LGOLD, 0.6)
            s += P("M45.4,74.6 L50,82 L54.6,74.6 Z", WHITE, INK, 0.5)
    elif kind in ('m', 'official', 'jian'):
        s += P("M42.8,71.6 C44.6,76.2 55.4,76.2 57.2,71.6", 'none', WHITE, 2.4) + P("M42,71.8 C44,77.6 56,77.6 58,71.8", 'none', INK, 0.4)
        s += P("M51,76.2 C55.4,78.4 60.8,81 66,80.2", 'none', INK, 0.6)
        if kind == 'official':
            s += P("M40.2,83 L59.8,83 L59.8,101 L40.2,101 Z", sp.get('badge', C['shiqing']), INK, 0.6)
            s += P("M42.2,85 L57.8,85 L57.8,101 L42.2,101 Z", 'none', GOLD, 0.6)
            s += Cc(50, 92, 3.4, LGOLD, INK, 0.4) + P("M46,95 C48,93.4 52,93.4 54,95", 'none', C['zhu'], 0.8)
        if kind == 'jian':      # Baoyu's red archer's robe with roundels
            s += both(Cc(33, 89, 5.6, LGOLD, INK, 0.5) + Cc(33, 89, 3.4, 'none', '#9c7426', 0.6))
    elif kind in ('dao', 'monk'):
        s += P("M41,71.8 L50,86 L59,71.8", 'none', trim, 4.2) + P("M39.4,71.8 L50,88.4 L60.6,71.8", 'none', INK, 0.4)
        s += P("M43,72 L50,83.4 L57,72 Z", WHITE, INK, 0.4)
        if kind == 'monk':
            s += P("M24,80 C34,86 46,92 64,101", 'none', C['zhu'], 4.6) + P("M24,80 C34,86 46,92 64,101", 'none', LGOLD, 0.6, ' stroke-dasharray="2 3"')
    if sp.get('ribbons'):    # a fairy's floating sash
        rc = sp['ribbons']
        s += P("M14,70 C22,64 30,68 34,76 C30,72 24,70 18,76 Z", rc, INK, 0.5) + P("M86,70 C78,64 70,68 66,76 C70,72 76,70 82,76 Z", rc, INK, 0.5)
    return s


# ================================================================== props
def prop(name):
    if name == 'hoe':          # 花锄 and 纱囊
        return (P("M84,100 L66,58", 'none', '#7a5434', 2.0) + P("M63.4,56 L70,53.6 L69.4,58.4 Z", '#8e8c88', INK, 0.5)
                + P("M70,74 C74,73 76,77 74.6,81 C72.6,84 68,83.6 67.4,80 C67,77 68,75 70,74 Z", C['danlv'], INK, 0.5)
                + P("M70.4,74 L72.4,68.4", 'none', INK, 0.5) + flower(71, 79, 1.6, C['tao']))
    if name == 'locket':       # 金锁
        return (P("M43.4,74 C45,79.4 55,79.4 56.6,74", 'none', GOLD, 0.8)
                + P("M45.4,80 C45.4,77.6 54.6,77.6 54.6,80 L53.6,85.4 C52,87.6 48,87.6 46.4,85.4 Z", GOLD, INK, 0.5)
                + P("M47.4,81.4 L52.6,81.4 M47.4,83.4 L52.6,83.4", 'none', '#9c7426', 0.5))
    if name == 'fan':          # 团扇
        return (P("M70,100 L66,86", 'none', '#7a5434', 1.4) + Cc(64, 81, 8.6, '#f7f1e2', INK, 0.6)
                + flower(62, 79, 2.2, C['tao']) + P("M60,85 C63,83.4 66,83.4 69,85", 'none', C['bilv'], 0.7))
    if name == 'tornfan':      # 撕扇
        return (P("M60,96 L56,82 L64,79 L66,84 L69,80 L72,85 L75,82 L77,88 Z", '#f4ebd6', INK, 0.5)
                + P("M60,96 L63,82 M60,96 L68,84 M60,96 L73,87", 'none', '#8a7a62', 0.4)
                + P("M77,88 L82,86 L80,91 Z M72,79 L74,74 L77,78 Z", '#f4ebd6', INK, 0.4))
    if name == 'unicorn':      # 金麒麟
        return (P("M57.6,90 C57.4,85.6 60.6,83.4 64.4,84 C66,81.8 68.4,81 70.4,82 L72.6,79.4 L72.2,82.8 C74,84 74,86.6 72.4,87.6 "
                  "L71.6,91.6 L69.8,91.6 L69.4,88.6 L62,88.8 L61.4,92 L59.6,92 L59.6,89.4 C58.6,89.8 57.8,90.4 57.6,90 Z", GOLD, INK, 0.5)
                + P("M57.8,86.6 C55.6,85 55.4,82.6 57.4,81.6 C57,83.4 58,84.6 59.4,85", 'none', '#9c7426', 0.7)
                + P("M64.6,84.2 C65.4,82.6 66.6,82 67.6,82.4 M62,86 C63,85.4 64,85.4 65,86", 'none', '#9c7426', 0.5)
                + Cc(71.2, 83.8, 0.55, INK, None) + Cc(66.4, 90.2, 1.4, C['zhu'], INK, 0.3))
    if name == 'sword':        # 鸳鸯剑
        return (P("M66,101 L85,58", 'none', '#cfd3d6', 2.6) + P("M66,101 L85,58", 'none', INK, 0.4)
                + P("M64.4,92 L71.6,95.2", 'none', GOLD, 2.0) + P("M60.6,100 L64.6,93", 'none', C['jiang'], 3.0))
    if name == 'kite':
        return (P("M78,52 L86,62 L78,74 L70,62 Z", '#f3ddb0', INK, 0.5) + P("M78,52 L78,74 M70,62 L86,62", 'none', INK, 0.4)
                + P("M78,74 C76,80 79,84 76,90 C74,94 70,96 66,99", 'none', INK, 0.4)
                + Cc(78, 62, 2.2, C['zhu'], None, 0, ' opacity=".7"'))
    if name == 'book':
        return (P("M38,86 L50,88.6 L62,86 L62,99 L50,101 L38,99 Z", '#e9dcb8', INK, 0.5) + P("M50,88.6 L50,101", 'none', INK, 0.5)
                + P("M41,90 L47,91.2 M41,93 L47,94.2 M53,91.2 L59,90 M53,94.2 L59,93", 'none', '#8a7a62', 0.4))
    if name == 'brush':
        return P("M62,100 L78,70", 'none', '#7a5434', 1.6) + P("M78,70 L81,63.6 L79.6,69.2 Z", INK, INK, 0.5)
    if name == 'rosary':
        return ''.join(Cc(50 + 10.6 * __import__('math').sin(a / 10), 76 + 8.4 * __import__('math').cos(a / 10), 1.15, '#7a3f2a', INK, 0.25)
                       for a in range(-15, 16, 2)) + Cc(50, 85.4, 1.8, C['zhu'], INK, 0.3)
    if name == 'spindle':
        return (P("M60,97 L74,74", 'none', '#7a5434', 1.0) + El(67, 85.6, 3.2, 5.2, '#e9dcb8', 1, 31, INK, 0.5)
                + P("M64.4,84 C66,87 69,88 70,86", 'none', '#8a7a62', 0.4))
    if name == 'bow':
        return P("M86,58 C74,68 72,86 80,100", 'none', '#7a5434', 1.6) + P("M86,58 L80,100", 'none', INK, 0.4)
    if name == 'mirror':       # 风月宝鉴, its back with a skull
        return (P("M66,101 L70,90", 'none', '#7a5434', 2.0) + Cc(73, 82, 8.6, '#cfc4a6', INK, 0.7) + Cc(73, 82, 6.8, 'none', '#9c7426', 0.6)
                + Cc(73, 80.6, 3.2, '#f4eee0', INK, 0.4) + Cc(71.8, 80.4, 0.7, INK, None) + Cc(74.2, 80.4, 0.7, INK, None)
                + P("M71.6,84.4 L74.4,84.4", 'none', INK, 0.5))
    if name == 'basket':
        return (P("M58,84 C58,95 76,95 76,84 Z", '#d4b680', INK, 0.5) + P("M58,84 C60,76 74,76 76,84", 'none', '#a88a52', 1.2)
                + P("M60,88 L74,88 M61,91 L73,91", 'none', '#a88a52', 0.5) + flower(63, 83, 1.8, C['huang']) + flower(70, 82.4, 1.8, C['tao']))
    if name == 'scissors':
        return (Cc(63, 92, 2.4, 'none', INK, 0.8) + Cc(68, 93, 2.4, 'none', INK, 0.8) + P("M64.4,90 L75,78 M66.4,90.6 L73,78", 'none', '#9a9da1', 1.0)
                + P("M76,84 C79,88 80,94 78,99", 'none', HAIR, 1.6) + P("M78,84 C81,89 82,94 80,99", 'none', HAIR, 1.2))
    if name == 'soup':
        return (P("M56,86 C56,94 72,94 72,86 Z", '#f4f1e8', INK, 0.6) + El(64, 86, 8, 2, '#a9cf8a', 1, 0, INK, 0.4)
                + P("M60,82 C59,79 61,77 60,74 M66,82 C65,79 67,77 66,74", 'none', '#bbb', 0.5))
    if name == 'medicine':
        return (P("M57,87 C57,94 71,94 71,87 Z", '#f4f1e8', INK, 0.6) + El(64, 87, 7, 1.8, '#5c3a22', 1, 0, INK, 0.4)
                + P("M62,83 C61,80 63,78 62,75", 'none', '#bbb', 0.5))
    if name == 'kerchief':
        return P("M58,82 C64,80 70,82 74,80 C72,86 74,92 70,98 C66,94 62,96 58,92 C60,88 57,86 58,82 Z", C['hong'], INK, 0.5)
    if name == 'keys':
        return (P("M66,80 L66,88", 'none', GOLD, 0.8) + Cc(66, 79, 1.8, 'none', GOLD, 0.8)
                + ''.join(P(f"M66,88 L{x},97", 'none', '#9c7426', 0.9) for x in (62, 65, 68.6, 71.6))
                + C_tassel(66, 87))
    if name == 'pouch':        # 绣春囊
        return (P("M60,84 C58,92 62,98 67,98 C72,98 76,92 74,84 C71,82 63,82 60,84 Z", C['tao'], INK, 0.5)
                + P("M60.6,84.6 C64,86.4 70,86.4 73.4,84.6", 'none', GOLD, 0.6) + flower(67, 91, 2.0, C['zhu']))
    if name == 'birdcage':
        return (P("M60,98 L60,82 C60,74 76,74 76,82 L76,98 Z", 'none', '#8a6a3a', 0.8)
                + ''.join(P(f"M{x},98 L{x},{82 - (8 - abs(x - 68)) * 0.45}", 'none', '#8a6a3a', 0.5) for x in (63, 66, 70, 73))
                + P("M68,75 L68,71", 'none', '#8a6a3a', 0.8) + El(68, 90, 2.6, 1.8, C['huang'], 1, 0, INK, 0.4))
    if name == 'furnace':      # 丹炉
        return (P("M58,86 C58,95 74,95 74,86 Z", '#b88a3a', INK, 0.6) + P("M57,86 L75,86", 'none', INK, 0.8)
                + P("M60,94 L59,99 M66,95 L66,100 M72,94 L73,99", 'none', INK, 0.8)
                + P("M62,82 C60,78 64,76 62,72 M68,82 C66,78 70,76 68,72", 'none', '#a7a4a0', 0.7))
    if name == 'whisk':
        return (P("M66,101 L80,72", 'none', '#7a5434', 1.4)
                + ''.join(P(f"M80,72 C{83 + d},{66 - d} {86 + d},{62 + d} {88 + d * 1.6},{58 + d}", 'none', '#f2efe8', 1.1) for d in (-2, 0, 2))
                + P("M80,72 C83,66 86,62 88,58", 'none', INK, 0.3))
    if name == 'paperdolls':
        return ''.join(G(P("M0,-6 C2,-6 2,-3 0,-3 C-2,-3 -2,-6 0,-6 Z M-3,-2 L3,-2 L4,5 L1,5 L0,9 L-1,5 L-4,5 Z", '#f4eee0', INK, 0.5)
                         + P("M-1,1 L1,1", 'none', C['zhu'], 0.6), f'translate({x} {y})') for x, y in ((62, 88), (71, 90)))
    if name == 'lantern':
        return (P("M68,72 L68,76", 'none', INK, 0.6) + El(68, 84, 6, 7.6, '#e2564a', 1, 0, INK, 0.5)
                + P("M62.4,80 C66,81.6 70,81.6 73.6,80 M62.4,88 C66,86.4 70,86.4 73.6,88", 'none', '#9e2e26', 0.5)
                + P("M64.6,76.6 L71.4,76.6 M64.6,91.4 L71.4,91.4", 'none', INK, 1.0))
    if name == 'giftbox':
        return (P("M57,84 L75,84 L75,97 L57,97 Z", C['zhu'], INK, 0.5) + P("M66,84 L66,97 M57,90.4 L75,90.4", 'none', GOLD, 1.2)
                + P("M63,84 C62,80 66,80 66,84 C66,80 70,80 69,84", 'none', GOLD, 0.8))
    if name == 'flowerbox':
        return (P("M56,88 L76,88 L76,98 L56,98 Z", '#7a4a2a', INK, 0.5) + flower(60, 85, 2.2, C['tao']) + flower(66, 84, 2.2, C['xing'])
                + flower(72, 85.4, 2.2, C['yanzhi']))
    if name == 'comb':
        return (P("M60,86 L76,86 L76,90 L60,90 Z", '#c99b5d', INK, 0.5)
                + ''.join(P(f"M{x},90 L{x},95", 'none', '#a37a42', 0.6) for x in (61.4, 63.2, 65, 66.8, 68.6, 70.4, 72.2, 74)))
    if name == 'warmer':       # 手炉
        return (El(65, 89, 8, 6, '#c08a3a', 1, 0, INK, 0.6) + El(65, 85.4, 6.4, 2.2, '#d9a957', 1, 0, INK, 0.5)
                + ''.join(Cc(x, 85.4, 0.6, INK, None) for x in (61, 63, 65, 67, 69)) + P("M57.6,86 C57,80 73,80 72.4,86", 'none', '#8a6a3a', 0.8))
    if name == 'armlet':
        return El(64, 90, 5, 2.4, 'none', 1, -12, GOLD, 1.6) + El(64, 90, 5, 2.4, 'none', 1, -12, INK, 0.3)
    if name == 'poem':
        return (P("M56,88 L74,82 L76,90 L58,96 Z", '#f6f0e0', INK, 0.5)
                + P("M60,89.6 L72,85.4 M61,92 L73,87.8", 'none', '#8a7a62', 0.4) + Cc(57, 92, 2.0, '#e6dcc0', INK, 0.4))
    if name == 'plum':
        return (P("M60,100 C64,90 70,84 82,72 M70,84 C74,84 78,82 82,80", 'none', '#5a3a2a', 1.2)
                + ''.join(flower(x, y, 1.8, C['hong'], LGOLD) for x, y in ((82, 72), (74, 80), (66, 90), (82, 80), (77, 76))))
    if name == 'sash_green':
        return P("M58,80 C64,82 66,90 64,99 L69,99 C71,90 69,82 63,79 Z", C['song'], INK, 0.5)
    if name == 'sash_red':
        return P("M58,80 C64,82 66,90 64,99 L69,99 C71,90 69,82 63,79 Z", C['hong'], INK, 0.5)
    if name == 'pin_hand':     # 龄官's gold hairpin
        return P("M58,96 L76,76", 'none', GOLD, 1.4) + Cc(76.6, 75.4, 1.8, GOLD, INK, 0.4) + flower(76.6, 75.4, 1.4, C['zhu'])
    if name == 'cup':
        return P("M60,86 L70,86 C70,93 60,93 60,86 Z", '#f6f2ea', INK, 0.5) + El(65, 93.6, 5.4, 1.4, '#f6f2ea', 1, 0, INK, 0.4) + P("M62,88 C64,89 66,89 68,88", 'none', C['qing'], 0.5)
    if name == 'bundle':
        return (P("M56,86 C56,80 76,80 76,86 L76,96 C76,99 56,99 56,96 Z", '#5c7aa0', INK, 0.5)
                + P("M62,81 C64,77 68,77 70,81", 'none', '#5c7aa0', 1.6) + P("M57,88 L75,92 M57,93 L75,88", 'none', '#3c5a80', 0.5))
    if name == 'scroll':       # registers
        return (P("M56,84 L76,84 L76,97 L56,97 Z", '#f1e6c8', INK, 0.5) + P("M56,84 L56,97 M76,84 L76,97", 'none', '#7a4a2a', 1.8)
                + P("M60,88 L72,88 M60,91 L72,91 M60,94 L68,94", 'none', '#8a7a62', 0.4))
    if name == 'bookbox':
        return (P("M56,84 L76,84 L76,98 L56,98 Z", '#6e4a2c', INK, 0.5) + P("M58,86 L74,86 L74,90 L58,90 Z", '#e9dcb8', INK, 0.4)
                + P("M66,80 L66,84", 'none', INK, 0.8))
    if name == 'cane':
        return P("M80,100 L76,58", 'none', '#7a4e2a', 2.0) + P("M75,58 C72,54 76,50 79,53 C81,55 79,58 76.4,58 Z", GOLD, INK, 0.5)
    if name == 'stick':
        return P("M78,100 L74,62", 'none', '#7a5434', 1.8)
    if name == 'farmbasket':
        return (P("M56,88 C56,98 76,98 76,88 Z", '#c6a066', INK, 0.5) + P("M56,88 C58,78 74,78 76,88", 'none', '#9a7a42', 1.4)
                + Cc(61, 86.4, 2.4, '#7aa04a', INK, 0.3) + Cc(66, 85.4, 2.6, '#d77a2c', INK, 0.3) + Cc(71, 86.4, 2.2, '#7aa04a', INK, 0.3))
    if name == 'jade':         # 通灵宝玉 on its cord
        return (P("M43.4,73.6 C45,79.4 55,79.4 56.6,73.6", 'none', C['zhu'], 0.8)
                + El(50, 82.6, 2.9, 3.8, '#e7efdc', 1, 0, INK, 0.5) + P("M48.8,81 L51.2,81 M48.8,83 L51.2,83", 'none', C['bilv'], 0.4))
    if name == 'oldfan':
        return (P("M58,96 L60,80 C64,77 72,77 76,80 L74,96 Z", '#efe0b8', INK, 0.5)
                + P("M66,96 L62,80 M66,96 L66.8,78.6 M66,96 L71.4,79.2", 'none', '#8a7a62', 0.4) + P("M60,82 C65,79.6 71,79.6 75.6,82", 'none', C['bilv'], 0.6))
    if name == 'whip':
        return P("M60,100 L70,80", 'none', '#5a3a2a', 1.6) + P("M70,80 C76,72 82,74 84,66", 'none', INK, 0.6)
    return ''


def C_tassel(x, y):
    return P(f"M{x},{y} L{x - 1},{y + 4} M{x},{y} L{x + 1},{y + 4}", 'none', C['zhu'], 0.6)


BEHIND = {'hoe', 'sword', 'bow', 'whisk', 'cane', 'stick', 'kite'}


# ================================================================== two small figures: the monk and the Taoist
def sengdao():
    monk = (P("M22,101 C24,90 31,84 39,82 L49,82 C57,84 64,90 66,101 Z", '#a2533a', INK, 0.6)
            + P("M30,88 C38,92 46,96 56,101", 'none', LGOLD, 2.0)
            + P("M41,72 L41,83 L47,83 L47,72 Z", SKIN_M, INK, 0.5)
            + Cc(44, 64, 10.4, SKIN_M, INK, 0.7)
            + ''.join(Cc(x, y, r, '#b8664f', None, 0, ' opacity=".7"') for x, y, r in ((39, 57, 1.3), (47, 55.4, 1.1), (50.4, 60, 1.2)))
            + P("M38.6,62.6 C39.8,61.6 41.6,61.4 42.8,62.2 M45.2,62.2 C46.4,61.4 48.2,61.6 49.4,62.6", 'none', INK, 0.7)
            + P("M40,66.6 C41,67.4 42.4,67.4 43,66.6 M45,66.6 C45.8,67.4 47.2,67.4 48,66.6", 'none', INK, 0.6)
            + P("M41,71 C43,72.6 45,72.6 47,71", 'none', '#9a3b33', 0.7))
    tao = (P("M44,101 C46,90 53,84 61,82 L71,82 C79,84 86,90 88,101 Z", '#4f6f8a', INK, 0.6)
           + P("M60,82 L66,94 L72,82", 'none', WHITE, 2.4)
           + P("M63,72 L63,83 L69,83 L69,72 Z", SKIN_OLD, INK, 0.5)
           + Cc(66, 64, 10, SKIN_OLD, INK, 0.7)
           + P("M56,62 C55,52 60,48 66,48 C72,48 77,52 76,62 C73,57 70,56 66,56.4 C62,56 59,57 56,62 Z", GREY, INK, 0.5)
           + P("M62.4,49.6 C62,45 64,43 66,43 C68,43 70,45 69.6,49.6 Z", GREY, INK, 0.5) + P("M61,45.6 L71,44.6", 'none', '#7a5434', 0.9)
           + P("M61,62.6 C62,61.6 63.8,61.6 65,62.4 M67,62.4 C68.2,61.6 70,61.6 71,62.6", 'none', INK, 0.6)
           + P("M62,66.4 L64.8,66.4 M67.2,66.4 L70,66.4", 'none', INK, 0.7)
           + P("M64,70.4 C64,76 65,80 66,82 C67,80 68,76 68,70.4 Z", GREY, None)
           + P("M58,74 C59,70 61,69 62,68 M74,74 C73,70 71,69 70,68", 'none', GREY, 0.8))
    return monk + tao


def jinghuan():
    return (P("M10,101 C14,82 30,74 42,72 L58,72 C70,74 86,82 90,101 Z", '#c9dbe3', INK, 0.6)
            + P("M43.8,72.6 L50,84 L56.2,72.6", 'none', '#e7b4c4', 3.2) + P("M45.4,72.8 L50,81.2 L54.6,72.8 Z", WHITE, INK, 0.5)
            + P("M8,74 C20,62 30,70 30,84 C26,76 18,74 12,82 Z", '#e7b4c4', INK, 0.5) + P("M92,74 C80,62 70,70 70,84 C74,76 82,74 88,82 Z", '#e7b4c4', INK, 0.5)
            + P("M14,92 C24,84 34,86 40,94", 'none', '#b9d3df', 2.0))


# ================================================================== specs
def S(**k):
    return k


F = dict(face='f')
SPEC = {
  # ---- 宁国府
  'jiajing':   S(face='m', ears=True, old=True, hair=None, head='topknot', headcol=GREY, crown=GOLD, beard=('san', GREY), robe='dao', col='#6c7f96', trim=WHITE, prop='furnace'),
  'jiazhen':   S(face='m', ears=True, head='nuan', beard=('short', HAIR), robe='official', col=C['shiqing'], badge='#2a4a72'),
  'youshi':    S(hair='pan', col='#3c5c86', trim=C['ouhe'], yjcol=C['qianlan'], orn=('pin', 'flower:fen'), robe='f'),
  'jiarong':   S(face='m', fine=True, ears=True, head='guapi', headcol=HAIR, robe='m', col='#8c5fa0'),
  'qinkeqing': S(hair='yun', col=C['jiang'], trim=C['huang'], yjcol=C['ehuang'], orn=('phoenixpin', 'buyao')),
  'jiaqiang':  S(face='m', fine=True, ears=True, head='guapi', headcol='#3a3d55', knot=C['bilv'], robe='m', col=C['qing'], prop='birdcage'),
  'youerjie':  S(hair='duo', col='#e9e2d0', trim=C['qianlan'], yjcol=C['yuebai'], orn=('flower:bai',), eyes='down'),
  'yousanjie': S(hair='gao', col=C['hong'], trim=C['mo'], yjcol=C['zhu'], orn=('pin',), prop='sword', mouth='frown'),
  'jiaoda':    S(face='m', ears=True, old=True, head='oldm', headcol=WHITEH, beard=('scraggly', WHITEH), robe='m', col='#8a7a62', mouth='frown'),
  'xichun':    S(hair='dan', col='#e6e3dc', trim=C['hui'], yjcol='#d8d4cc', orn=(), eyes='down', prop='brush'),
  # ---- 荣国府
  'jiamu':     S(old=True, hair='pan', haircol=WHITEH, band=('#5a3a5c', C['zhu']), col='#6b4a6e', trim=GOLD, yjcol='#8f6f90', prop='cane', mouth='smile'),
  'jiashe':    S(face='m', ears=True, old=True, head='nuan', bead=C['qianlan'], beard=('mous', GREY), robe='official', col=C['shiqing'], badge='#7a3a3a', prop='oldfan'),
  'xingfuren': S(hair='pan', band=('#4a3a2a', C['bilv']), col='#8a6a48', trim=C['zong'], yunjian=False),
  'jiazheng':  S(face='m', ears=True, head='liang', beard=('san', HAIR), robe='official', col=C['shiqing'], badge='#284466'),
  'wangfuren': S(hair='pan', band=('#2a3a52', C['bilv']), col='#3c5c86', trim=C['mi'], yunjian=False, prop='rosary', eyes='down'),
  'zhaoyiniang': S(hair='duo', col='#b04a7a', trim=C['huang'], yunjian=False, orn=('flower:hong',), mouth='frown'),
  'jialian':   S(face='m', fine=True, ears=True, head='guapi', headcol=HAIR, knot=C['zhu'], robe='m', col=C['mo'], mouth='smile'),
  'xifeng':    S(head='fengjie', col=C['hong'], trim=GOLD, yjcol=C['shiqing'], mouth='smile', butterflies=True),
  'liwan':     S(hair='dan', col='#9aa3a6', trim='#6f7a80', yunjian=False, prop='book'),
  'yuanchun':  S(head='phoenix', col=C['huang'], trim=C['hong'], yjcol=C['shiqing']),
  'yingchun':  S(hair='dan', col=C['ehuang'], trim=C['danlv'], yjcol='#f4ead0', orn=('pin',), eyes='down', prop='book'),
  'tanchun':   S(hair='gao', col=C['xing'], trim=C['shiqing'], yjcol=C['qianlan'], orn=('pin', 'flower:xing'), prop='kite'),
  'baoyu':     S(face='f', head='baoyu', robe='jian', col=C['hong'], prop='jade', blushm=True),
  'jiahuan':   S(face='m', fine=True, ears=True, head='guapi', headcol='#4a3a2a', knot=C['huang'], robe='m', col='#7a8a5a', eyes='side', mouth='frown'),
  'jialan':    S(face='c', ears=True, head='guapi', headcol=HAIR, knot=C['zhu'], robe='m', col=C['shilv'], prop='bow'),
  'qiaojie':   S(face='c', hair='child', col=C['tao'], trim=C['hong'], yunjian=False, prop='spindle'),
  'jiarui':    S(face='m', fine=True, ears=True, head='rujin', headcol=HAIR, robe='m', col='#a99a7a', prop='mirror', mouth='smile'),
  'jiayun':    S(face='m', fine=True, ears=True, head='rujin', headcol='#3a3d55', robe='m', col='#7a8aa0', prop='giftbox'),
  # ---- 林 史 王 薛
  'linruhai':  S(face='m', ears=True, head='liang', beard=('san', HAIR), robe='official', col='#3a4a6a', badge='#2a5a4a'),
  'daiyu':     S(hair='duo', col=C['danlv'], trim=C['bilv'], yjcol='#cfe3d2', orn=('pin', 'flower:bai'), prop='hoe'),
  'xiangyun':  S(hair='gao', fringe=True, col=C['shiqing'], trim=C['hong'], yjcol=C['qianlan'], orn=('flower:hong', 'flower2:huang'), prop='unicorn', mouth='smile'),
  'wangziteng': S(face='m', ears=True, head='nuan', beard=('full', HAIR), robe='official', col=C['shiqing'], badge='#7a2a2a'),
  'xueyima':   S(hair='pan', band=('#5a4a2a', C['zhu']), col='#8a7a4a', trim=C['mi'], yunjian=False, mouth='smile'),
  'xuepan':    S(face='p', ears=True, head='guapi', headcol=HAIR, knot=C['zhu'], robe='m', col=C['hong'], prop='whip', mouth='smile'),
  'baochai':   S(hair='yun', col=C['mi'], trim=C['huang'], yjcol=C['ehuang'], orn=('pin',), prop='locket'),
  'baoqin':    S(hair='gao', col='#c5544c', trim=GOLD, yjcol='#8a5a3a', orn=('pin', 'buyao'), prop='plum', cloak=True),
  'xueke':     S(face='m', fine=True, ears=True, head='rujin', headcol=HAIR, robe='m', col='#5a7a9a'),
  'xiajingui': S(hair='yun', col=C['yanzhi'], trim=GOLD, yjcol=C['huang'], orn=('buyao', 'flower:hong', 'flower2:huang'), mouth='frown'),
  # ---- servants
  'pinger':    S(hair='dan', col=C['ouhe'], trim=C['zi'], yunjian=False, orn=('pin',), robe='maid', prop='keys'),
  'xiren':     S(hair='dan', col=C['fen'], trim=C['qing'], robe='maid', orn=('flower:hong',), prop='sash_green'),
  'qingwen':   S(hair='duo', col=C['hong'], trim=C['shiqing'], robe='maid', orn=('pin',), prop='tornfan'),
  'sheyue':    S(hair='dan', col=C['danlv'], trim=C['bilv'], robe='maid', prop='comb'),
  'zijuan':    S(hair='dan', col='#a98ab8', trim=C['zi'], robe='maid', prop='medicine'),
  'xueyan':    S(face='c', hair='shuang', col='#f1efe8', trim=C['qianlan'], robe='maid', ribbon=C['qing'], prop='warmer'),
  'yinger':    S(hair='shuang', col=C['huang'], trim=C['bilv'], robe='maid', ribbon=C['bilv'], prop='basket'),
  'yuanyang':  S(hair='dan', col=C['shilv'], trim=C['shiqing'], robe='maid', prop='scissors'),
  'jinchuan':  S(hair='shuang', col=C['ehuang'], trim=C['zhu'], robe='maid', ribbon=C['zhu'], prop='armlet'),
  'yuchuan':   S(hair='shuang', col=C['danlv'], trim=C['zhu'], robe='maid', ribbon=C['qing'], prop='soup'),
  'siqi':      S(hair='dan', col='#7a5a8a', trim=C['mo'], robe='maid', mouth='frown', prop='sash_red'),
  'xiaohong':  S(hair='shuang', col=C['tao'], trim=C['hong'], robe='maid', ribbon=C['hong'], prop='kerchief'),
  'fangguan':  S(face='f', head='guapi', headcol=C['zhu'], knot=GOLD, robe='m', col=C['shilv'], fringe_m=True),
  'lingguan':  S(hair='duo', col=C['ouhe'], trim=C['jiang'], robe='maid', prop='pin_hand', eyes='down'),
  'zhouruijia': S(hair='pan', band=('#3a3a3a', C['bilv']), col='#6a7a8a', trim='#4a5a6a', robe='maid', prop='flowerbox'),
  'wangshanbao': S(old=True, hair='pan', haircol=GREY, band=('#3a2a2a', C['zhu']), col='#6a5a4a', trim='#3a2a1a', robe='maid', prop='lantern', mouth='frown'),
  'qiutong':   S(hair='duo', col=C['yanzhi'], trim=C['huang'], robe='maid', orn=('flower:huang', 'flower2:hong'), mouth='frown'),
  'shadajie':  S(face='p', hair='shuang', col='#d9a066', trim=C['hong'], robe='maid', ribbon=C['hong'], prop='pouch', mouth='smile'),
  'mingyan':   S(face='c', ears=True, head='guapi', headcol=HAIR, knot=C['zhu'], robe='m', col='#8aa0b0', prop='bookbox'),
  'limama':    S(old=True, hair='pan', haircol=GREY, band=('#3a2a2a', C['bilv']), col='#7a6a5a', trim='#4a3a2a', robe='maid', prop='stick', mouth='frown'),
  'caixia':    S(hair='dan', col=C['xing'], trim=C['shiqing'], robe='maid', prop='cup'),
  'baoer':     S(hair='duo', col='#b07a6a', trim='#5a3a3a', robe='maid', loose=True),
  'ruhua':     S(hair='shuang', col='#cfd6d8', trim=C['qing'], robe='maid', ribbon=C['qing'], prop='bundle', eyes='down'),
  'cuilv':     S(hair='shuang', col=C['shilv'], trim=C['hong'], robe='maid', ribbon=C['hong'], prop='unicorn'),
  'xiangling': S(hair='dan', col=C['fen'], trim=C['shilv'], robe='maid', mole=True, orn=('flower:huang',), prop='poem'),
  # ---- outside
  'jinghuan':  S(hair='gao', col='#c9dbe3', trim='#e7b4c4', orn=('buyao', 'flower:fen', 'flower2:bai'), body='jinghuan', prop='scroll'),
  'sengdao':   S(body='sengdao'),
  'shiyin':    S(face='m', ears=True, old=True, head='topknot', headcol=GREY, beard=('san', GREY), robe='dao', col='#7a8a9a', trim=WHITE, prop='whisk'),
  'jiaoxing':  S(hair='dan', col=C['xing'], trim=C['bilv'], robe='maid', eyes='side', orn=('flower:hong',)),
  'yucun':     S(face='m', ears=True, head='liang', beard=('mous', HAIR), robe='official', col=C['shiqing'], badge='#4a3a6a', eyes='side'),
  'fengyuan':  S(face='m', fine=True, ears=True, head='rujin', headcol='#3a3d55', robe='m', col='#a0b0c0'),
  'liulaolao': S(old=True, head='scarf', headcol='#4f6f9a', col='#8a7a5a', trim='#5a4a3a', robe='maid', prop='farmbasket', mouth='smile'),
  'qinzhong':  S(face='f', fine=True, ears=True, head='rujin', headcol=HAIR, robe='m', col=C['qianlan']),
  'zhineng':   S(face='f', head='baldnun', robe='dao', col='#8a8d8a', trim='#c9c6bf'),
  'beijingwang': S(face='m', fine=True, ears=True, head='wang', robe='m', col=WHITE, trim=C['yin'], dragon=True),
  'jiangyuhan': S(face='f', head='actor', col=C['tao'], trim=C['shiqing'], yjcol=C['qianlan'], prop='sash_red', opera=True),
  'liuxianglian': S(face='m', fine=True, ears=True, head='xiongjin', headcol=C['mo'], robe='m', col='#3a4a5a', prop='sword'),
  'miaoyu':    S(head='nunhood', headcol='#9a9690', robe='dao', col='#b9b6ae', trim='#e4e0d6', prop='whisk', eyes='down'),
  'madaopo':   S(old=True, head='daogu', headcol='#3a3a3a', robe='dao', col='#5a5a6a', trim='#d4d0c6', prop='paperdolls', eyes='side', mouth='frown'),
  'zhanghua':  S(face='m', fine=True, ears=True, head='guapi', headcol='#5a4a3a', knot='#8a7a62', robe='m', col='#9a8a6a', mouth='frown', patched=True),
  'sunshaozu': S(face='m', ears=True, head='nuanplume', beard=('stubble', HAIR), robe='official', col='#5a3a2a', badge='#3a2a1a', mouth='frown'),
  'zhenbaoyu': S(face='f', head='baoyu', crown=C['yin'], robe='jian', col=C['qing'], prop='jade', mirror=True),
}


def head(sp):
    h = sp.get('head')
    if h is None:
        return hair_f(sp) + ornaments(sp)
    if h == 'topknot':
        return topknot(sp.get('headcol', HAIR), sp.get('crown'))
    if h == 'nuan':
        return hat_nuan(bead=sp.get('bead', C['zhu']))
    if h == 'nuanplume':
        return hat_nuan(brim='#3a2a1a', bead=C['qianlan'], plume=True)
    if h == 'liang':
        return hat_liang()
    if h == 'guapi':
        s = ''
        if sp.get('fringe_m'):
            s += P("M40,42.6 C42.4,39 57.6,39 60,42.6 C57,41.6 54.4,42.4 52,41.4 C50,42.4 48,41.6 46,42.4 C44,41.6 42,42.2 40,42.6 Z", HAIR, None)
        return s + hat_guapi(sp.get('headcol', HAIR), sp.get('knot', C['zhu']))
    if h == 'rujin':
        return hat_rujin(sp.get('headcol', HAIR))
    if h == 'xiongjin':
        return hat_xiongjin(sp.get('headcol', C['mo']))
    if h == 'oldm':
        return old_hair_m(sp.get('headcol', GREY))
    if h == 'baoyu':
        return baoyu_hair(sp.get('crown', GOLD))
    if h == 'fengjie':
        return fengjie_crown() + P(HAIR_BASE, HAIR, INK, 0.6) + both(P(LOCK, HAIR, None))
    if h == 'phoenix':
        return P(HAIR_BASE, HAIR, INK, 0.6) + both(P(LOCK, HAIR, None)) + phoenix_crown()
    if h == 'wang':
        return hat_wang()
    if h == 'nunhood':
        return nun_hood(sp.get('headcol', '#9a9690'))
    if h == 'baldnun':
        return bald(False, '#dfe0de')
    if h == 'scarf':
        return P(HAIR_BASE, GREY, INK, 0.6) + headscarf(sp.get('headcol', '#4f6f9a'))
    if h == 'daogu':
        return (P(HAIR_BASE, GREY, INK, 0.6)
                + P("M39.6,38 C39,30 43.6,25.6 50,25.6 C56.4,25.6 61,30 60.4,38 C56,36 44,36 39.6,38 Z", sp.get('headcol', '#3a3a3a'), INK, 0.6)
                + P("M44,27.4 L56,27.4", 'none', GOLD, 0.8))
    if h == 'actor':           # a young actor of female roles: hair ornaments and stage rouge
        return (hair_f(dict(hair='dan')) + pin(55, 28, 64, 23) + flower(42, 29, 2.4, C['tao']) + flower(58, 29.6, 2.0, C['zhu']))
    return ''


def ornaments(sp):
    s = ''
    style = sp.get('hair', 'dan')
    top = {'gao': 22, 'yun': 24, 'duo': 24, 'dan': 27, 'pan': 29, 'shuang': 27, 'child': 31}.get(style, 28)
    for o in sp.get('orn', ()):
        if o == 'pin':
            s += pin(55, top + 4, 64, top)
        elif o == 'buyao':
            s += buyao(38, top + 6)
        elif o == 'phoenixpin':
            s += pin(56, top + 3, 65.4, top - 2.4, GOLD, C['zhu']) + P(f"M63,{top - 3.6} C65.4,{top - 6.6} 68.6,{top - 5.4} 68.6,{top - 2.6} C66.8,{top - 3.2} 65.4,{top - 2.2} 64.6,{top - 0.6} Z", GOLD, INK, 0.4)
        elif o.startswith('flower:'):
            s += flower(41.6, top + 6, 2.6, C[o.split(':')[1]])
        elif o.startswith('flower2:'):
            s += flower(46.4, top + 4.6, 1.9, C[o.split(':')[1]])
    if sp.get('band'):
        s += headband(*sp['band'])
    return s


def build(pid, shared=None):
    """The portrait's SVG content. With a `shared` dict, repeated parts are stored there once and used by reference."""
    def part(svg):
        if shared is None or len(svg) < 300:
            return svg
        key = shared.setdefault(svg, f'hp{len(shared)}')
        return f'<use href="#{key}"/>'

    sp = SPEC[pid]
    s = ''
    if sp.get('body') == 'sengdao':
        s = G(sengdao(), 'translate(50 70) scale(1.25) translate(-50 -70)')
        return f'<rect width="100" height="100" fill="{SILK}"/>' + s + Cc(50, 50, 47, 'none', INK, 0.8, ' opacity=".3"')
    if sp.get('prop') in BEHIND:
        s += part(G(prop(sp['prop']), 'translate(-3 -8)'))
    if sp.get('body') == 'jinghuan':
        s += part(jinghuan())
    else:
        rsp = dict(sp)
        if rsp.get('robe') is None:
            rsp['robe'] = 'f'
        s += part(G(robe(rsp), 'translate(0 -7)'))
        if sp.get('butterflies'):
            s += ''.join(G(P("M0,0 C-3,-3 -4,1 -1,1 C-4,2 -2,5 0,1.4 C2,5 4,2 1,1 C4,1 3,-3 0,0 Z", GOLD, INK, 0.3), f'translate({x} {y})')
                         for x, y in ((22, 94), (31, 88), (69, 88), (78, 94), (36, 98)))
        if sp.get('dragon'):
            s += P("M24,92 C30,86 36,90 40,86 C44,82 40,78 44,76", 'none', C['yin'], 1.2) + P("M76,92 C70,86 64,90 60,86 C56,82 60,78 56,76", 'none', C['yin'], 1.2)
        if sp.get('cloak'):
            s += P("M10,101 C12,84 24,74 36,72 L40,76 C30,80 24,90 22,101 Z", '#8a5a3a', INK, 0.5) + P("M90,101 C88,84 76,74 64,72 L60,76 C70,80 76,90 78,101 Z", '#8a5a3a', INK, 0.5)
        if sp.get('patched'):
            s += P("M28,90 L36,88 L37,95 L29,96 Z", '#b6a27e', INK, 0.4) + P("M68,86 L75,87 L74,93 L67,92 Z", '#b6a27e', INK, 0.4)
    s += part(face(sp))
    if sp.get('opera'):
        s += both(El(43, 48.6, 3.6, 4.8, '#ea7b8a', 0.45))
    if sp.get('beard'):
        s += part(beard(*sp['beard']))
    s += part(head(sp))
    if sp.get('prop') and sp['prop'] not in BEHIND:
        dx = 0 if sp['prop'] in ('locket', 'jade', 'rosary') else -3
        dy = -7.5 if sp['prop'] in ('locket', 'jade', 'rosary') else -14
        s += part(G(prop(sp['prop']), f'translate({dx} {dy})'))
    if sp.get('mirror'):
        inner = s
        s = f'<g transform="matrix(-1 0 0 1 100 0)">{inner}</g>'
        s += Cc(50, 50, 44, 'none', C['yin'], 1.6, ' opacity=".7"')
    return (f'<rect width="100" height="100" fill="{SILK}"/>'
            f'<g transform="translate(50 51) scale(1.3) translate(-50 -47)">{s}</g>'
            + Cc(50, 50, 47, 'none', INK, 0.8, ' opacity=".3"'))


def symbols(ids):
    shared = {}
    out = []
    for pid in ids:
        out.append(f'<symbol id="pt-{pid}" viewBox="0 0 100 100">'
                   f'<clipPath id="pc-{pid}"><circle cx="50" cy="50" r="50"/></clipPath>'
                   f'<g clip-path="url(#pc-{pid})">{build(pid, shared)}</g></symbol>')
    parts = [f'<symbol id="{k}" overflow="visible">{svg}</symbol>' for svg, k in shared.items()]
    return '\n'.join(parts + out)
