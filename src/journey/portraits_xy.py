# -*- coding: utf-8 -*-
"""Journey to the West portraits in the manner of Ming woodblock illustrations (明刊本绣像):
bold ink outlines on aged paper with light hand-colored washes. Profile busts facing right, drawn in a
100x100 box like the other books; gods get a round halo (头光) behind the head.
"""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'odyssey'))
from portraits import P, C_, GARMENT, BEARD_SHORT, BEARD_LONG, BEARD_POINT, MUSTACHE, HAIR_SHORT, HAIR_LONG, HAIR_BUN  # noqa: E402

INK = '#231d17'
PAPER = '#efe2c2'
PAPER_D = '#e3cfa2'          # a shade darker for demons
SKIN = '#f8edd6'
W = dict(ink=INK, paper=PAPER, skin=SKIN, white='#fbf6ea', red='#c2472f', vermil='#d0573a', blue='#5f7f8e',
         indigo='#3f5566', green='#7f9868', jade='#8fb3a2', ochre='#c99b55', gold='#dcaa42', yellow='#dfbd4c',
         grey='#9a958a', brown='#8a6444', pink='#dc9a86', purple='#8a6a8e', dark='#4a4540', bone='#efe9d6')
LW = 1.15   # outline weight


def base(bg=PAPER):
    return f'<rect width="100" height="100" fill="{bg}"/>'


def ink(d, w=LW, extra=''):
    return P(d, 'none', INK, w, extra)


def fill(d, col, w=LW):
    return P(d, col, INK, w)


def dot(x, y, r=0.9, col=INK):
    return C_(x, y, r, col)


def big(s, k, cx, cy, dx=0, dy=0):
    return f'<g transform="translate({dx} {dy}) translate({cx} {cy}) scale({k}) translate({-cx} {-cy})">{s}</g>'


def zoom(s, k=1.08, cx=48, cy=52):
    return f'<g transform="translate({cx} {cy}) scale({k}) translate({-cx} {-cy})">{s}</g>'


# ------------------------------------------------------------------ halo, frame, robe
def halo(x=47, y=42, r=26, col='#f2d488'):
    return (C_(x, y, r, col, INK, 0.7).replace('/>', ' fill-opacity=".55"/>')
            + C_(x, y, r - 3.2, 'none', INK, 0.4).replace('/>', ' opacity=".6"/>'))


def mandorla(x=47, y=44, r=30):
    """Larger double halo for buddhas, with little flame points."""
    s = halo(x, y, r, '#f0cd7a')
    for k in range(16):
        a = math.pi * (0.9 + k * 1.2 / 15)
        px, py = x + r * math.cos(a), y + r * math.sin(a)
        s += P(f"M{px:.1f},{py:.1f} l{2.4*math.cos(a):.1f},{2.4*math.sin(a):.1f}", 'none', INK, 0.5)
    return s


def frame():
    return C_(50, 50, 46.8, 'none', INK, 0.8).replace('/>', ' opacity=".45"/>')


def robe(col, collar=None, folds=True):
    s = fill(GARMENT, col)
    band = collar or W['white']
    # crossed collar, left over right (交领右衽)
    s += fill("M40.4,79.2 C45,85.6 49.4,92 52,100 L57.6,100 C55,92 50.6,85 46.4,79.8 Z", band, 0.9)
    s += fill("M58.8,80.4 C55.6,86.4 52.6,93 51.2,100 L55.6,100 C57.2,93.4 60.2,87.4 63.6,82 Z", band, 0.9)
    if folds:
        for d in ["M26,88 C28.6,92 29.6,96 29,100", "M72,86 C71,91 71.4,96 73,100", "M34,84 C36.4,89 37,94 36,100"]:
            s += ink(d, 0.7)
    return s


def cassock(col=None, grid=None):
    """Monk's patched robe (袈裟): red with a gold grid."""
    col = col or W['red']
    grid = grid or W['gold']
    s = robe(col, W['gold'], folds=False)
    for d in ["M14,92 L90,92", "M20,84 L80,84", "M30,80 L30,100", "M44,86 L42,100", "M66,82 L68,100", "M80,86 L82,100"]:
        s += P(d, 'none', grid, 1.4)
    s += C_(66, 88, 2.2, grid, INK, 0.6)
    return s


# ------------------------------------------------------------------ human head
HEAD_CN = ("M57,28 C59.8,32 61.4,36 61.8,39.6 C62,41.2 61.8,42.4 62.4,43.8 L66.8,50.2 C67.6,51.6 66.8,52.9 65,53.1 "
           "C64.6,54.1 64.8,55 64.7,55.6 C64.2,56.4 63.4,56.8 62.5,57 C63.4,57.6 64,58.3 63.8,59.1 "
           "C63.3,60 62.5,60.4 62.3,60.9 C63.2,62.6 63,64.8 61.2,66.2 C59.6,67.4 57.8,67.8 56.6,67.8 "
           "C57.2,73 57.8,78 58.8,86 L37.5,86 C39,78 39.6,72 38.8,66 C33,60 30,50 32,41 "
           "C34,31 44,25 52,26 C53.6,26.2 55.4,26.8 57,28 Z")


def head(skin=SKIN):
    return fill(HEAD_CN, skin)


def eye(kind='open', col=None):
    if kind == 'closed':      # downcast, meditative
        return ink("M54.6,43.6 Q57.6,45.2 60.6,43.4", 1.0) + ink("M53.2,39.6 Q57.2,37.8 61,39.4", 1.0)
    if kind == 'laugh':
        return ink("M54.8,44.2 Q57.8,41.6 60.8,44", 1.1) + ink("M53.4,39.2 Q57.4,37.4 61.2,39.2", 1.0)
    s = ink("M54.4,43.4 Q57.6,41.6 61,43", 1.0) + ink("M55.4,44.2 Q58,45.2 60.4,44.2", 0.6)
    s += dot(58.6, 43.5, 1.05, col or INK)
    s += ink("M53.2,39.6 Q57.2,37.6 61.2,39.2", 1.3)            # brow
    return s


def face(old=False, smile=False):
    s = ink("M64.8,52.4 Q64,52.1 63.5,52.8", 0.7)                    # nostril
    s += ink("M62.5,57 L60.4,57.3", 0.8) if not smile else ink("M62.6,56.6 Q60.8,58.6 58.8,57.2", 0.9)
    if old:
        s += ink("M53,35.4 Q56,34.4 59,35.1 M52.8,37.3 Q55.8,36.4 59.6,37.2", 0.5)
        s += ink("M61,46.6 Q59.6,49.2 60.4,51.6", 0.5)
    return s


def ear(lobe=False, skin=SKIN):
    if lobe:   # long Buddha earlobe
        return fill("M46.4,42.4 C43.4,41.4 41.4,44 42,47.6 C42.4,51.4 42.2,56.4 44,59.4 C45.4,61.6 47.6,61 47.6,58.6 "
                    "C47.4,55 47,51.4 46.4,48", skin, 0.9) + ink("M45,45.4 C43.8,46.4 43.8,49 44.8,50.4", 0.6)
    return (fill("M46.4,44.6 C43.6,43.4 41.8,45.8 42.4,48.6 C42.9,51 44.4,52.6 46.2,52.3", skin, 0.9)
            + ink("M45.1,46.3 C43.9,46.8 43.9,48.8 45,49.8", 0.6))


def hair(kind='short', col=INK):
    d = {'short': HAIR_SHORT, 'long': HAIR_LONG, 'bun': HAIR_BUN}[kind]
    s = P(d, col, INK, LW)
    if col == INK:
        tex = {'short': "M36,40 C39,38 41,38.6 44,37.4 M35,48 C37.4,46 40,46.8 42.6,45 M37,56 C39,54 41,55 43,53",
               'long': "M34,46 C35,56 34,66 33,76 M38.4,48 C39.4,58 39,68 37,78",
               'bun': "M27,37 C29,41 30,43 34,44.5 M29,33.5 C33,36 34.5,40 34,43"}[kind]
        s += P(tex, 'none', PAPER, 0.5, ' opacity=".55"')
    return s


def topknot(col=INK, pin=True, y=20):
    s = P(f"M40,{y+7} C38.4,{y+1} 42,{y-4} 47,{y-4} C52,{y-4} 55,{y} 53.6,{y+6} C50,{y+6.6} 44,{y+6.8} 40,{y+7} Z", col, INK, LW)
    if pin:
        s += P(f"M34,{y+3.4} L60,{y-1}", 'none', W['gold'], 1.6) + ink(f"M34,{y+3.4} L60,{y-1}", 0.4)
    return s


def beard(kind='long', col=INK):
    d = {'short': BEARD_SHORT, 'long': BEARD_LONG, 'point': BEARD_POINT}[kind]
    s = P(d, col, INK, 1.0) + P(MUSTACHE, col, INK, 0.8)
    if col == INK:
        s += P("M50,62 C52,70 55,77 57,84 M54,61 C56,68 58.5,75 60,82", 'none', PAPER, 0.5, ' opacity=".5"')
    else:
        s += ink("M50,62 C52,70 55,77 57,84 M54,61 C56,68 58.5,75 60,82", 0.45)
    return s


def thin_beard(col=INK):
    """Three long thin strands (三绺长髯) of a scholar or official."""
    s = P(MUSTACHE, col, INK, 0.7)
    s += P("M60.4,61.6 C61,68 60,76 57.6,86 C57,80 57.6,70 58.2,62 Z", col, INK, 0.7)
    s += P("M50,58 C49,66 47,74 43,82 C45,74 46.4,66 47.6,58 Z", col, INK, 0.6)
    return s


def person(skin=SKIN, hair_kind='short', beard_kind=None, beard_col=INK, old=False, eye_kind='open', hair_col=INK, show_ear=True):
    s = head(skin)
    if hair_kind:
        s += hair(hair_kind, hair_col)
    if beard_kind == 'thin':
        s += thin_beard(beard_col)
    elif beard_kind:
        s += beard(beard_kind, beard_col)
    if show_ear:
        s += ear(skin=skin)
    s += eye(eye_kind) + face(old)
    return s


# ------------------------------------------------------------------ headgear
def mian():
    """Emperor's crown: a flat board hung with strings of beads (冕旒)."""
    s = fill("M34,34 C33,26 38,21 46,20 C53,19.4 58,22 58.6,28.6 C50,29.6 41,31.6 34,34 Z", INK)
    s += fill("M22,19.2 L71,12.4 L71.6,15.8 L22.6,22.6 Z", INK)
    s += P("M24,19.8 L70,13.4", 'none', W['red'], 0.9)
    for x0, y0 in [(66, 15.2), (69, 14.8), (24.4, 22), (27.4, 21.6)]:
        for i in range(6):
            s += C_(x0 - i * 0.12, y0 + 2.2 + i * 2.6, 0.9, W['gold'], INK, 0.3)
    s += P("M46,22 L45.4,31", 'none', W['gold'], 1.4)
    return s


def futou():
    """Tang emperor's black gauze cap (幞头) with two soft tails hanging behind."""
    s = fill("M31.4,32 C28.6,40 27,50 25,60 C28,58 30,52 32,46 C31.6,54 30.4,62 28,70 C32,64 34.4,54 35,44 Z", INK, 0.8)
    s += fill("M32.8,44 C30.4,32 35,23.4 45,21.4 C53,20 58.6,23.6 59.6,30.6 C50,32.6 41,37.4 32.8,44 Z", INK)
    s += fill("M38.6,26.6 C37.6,19 41.4,14 47,13.6 C52.6,13.4 55.6,17.6 54.6,23.4 C50,23.2 44,24.4 38.6,26.6 Z", INK)
    s += P("M34.4,40.6 C42,35.4 50,32.4 59.4,30.8", 'none', '#5a524a', 1)
    return s


def king_crown():
    s = fill("M33.6,42.6 C31.6,33.6 36,26.6 44,24.6 C51.4,22.8 57.8,25.4 59.6,31.4 C50.4,33.4 41.6,37.4 33.6,42.6 Z", W['gold'])
    s += fill("M46,25.2 C45,18 48,13 52,11.6 C55,14 56.4,19 55,24.6 Z", W['gold'], 0.9)
    s += C_(51, 19, 1.6, W['red'], INK, 0.4)
    s += P("M34.6,40 C43,35.4 51,32.6 59.6,31.4", 'none', INK, 1.1)
    return s


def pilu_crown():
    """Tang Sanzang's five-panel crown (毗卢帽)."""
    s = fill("M33.6,42.6 C31.6,33.6 36,26.6 44,24.6 C51.4,22.8 57.8,25.4 59.6,31.4 C50.4,33.4 41.6,37.4 33.6,42.6 Z", W['yellow'])
    for (x, y, h) in [(56.6, 27.4, 12), (49.4, 25.4, 13.6), (41.8, 27.4, 13), (35.4, 32.6, 11)]:
        s += fill(f"M{x-4.2},{y+2.4} C{x-4.4},{y-h*0.4} {x-1.6},{y-h*0.8} {x},{y-h} C{x+1.6},{y-h*0.8} {x+4.4},{y-h*0.4} {x+4.2},{y+2.4} Z", W['red'], 1.0)
        s += C_(x, y - h * 0.42, 1.5, W['gold'], INK, 0.5)
    s += P("M34.6,40 C43,35.4 51,32.6 59.6,31.4", 'none', INK, 1.1)
    s += fill("M32,40.4 C27,46 24,56 22,68 C25.4,64 27.6,56 30.4,50 C30.6,58 29.6,66 27.4,74 C31,68 33,58 33.6,48 Z", W['red'], 0.8)
    return s


def bodhi_crown(col=None):
    """Bodhisattva's jeweled crown with ribbons (宝冠)."""
    col = col or W['gold']
    s = hair('long')
    s += fill("M34,38.6 C33,33 36,28.6 41,27 L43.6,17.4 L47,25.8 L50.4,15.6 L53,25.4 L57.2,19 L57.6,28.4 C50,30 41.4,33.6 34,38.6 Z", col)
    for x, y in [(43.8, 23), (50.4, 21.6), (56.4, 24.4)]:
        s += C_(x, y, 1.2, W['red'], INK, 0.4)
    s += P("M34,38.6 C42,34 50,30.6 57.8,28.4", 'none', INK, 1.0)
    s += fill("M33.6,36.4 C28,40 24,48 22.4,58 C25,54 27,50 29.4,47 C28.6,54 28,60 26.4,66 C30,60 32,52 33.8,44 Z", W['vermil'], 0.7)
    return s


def dao_crown(col=None):
    """Small lotus crown on a Daoist topknot."""
    col = col or W['gold']
    s = topknot(pin=False, y=21)
    s += fill("M39.6,23.4 C39,18 42,14.6 46,14.4 C50,14.2 53.4,17 53.4,22 C49,23.2 44,23.4 39.6,23.4 Z", col)
    s += ink("M43,15.6 L43.6,22.8 M46.6,14.4 L46.6,22.8 M50.2,15.4 L49.8,22.6", 0.5)
    s += P("M34,20 L60,15.4", 'none', INK, 1.4)
    return s


def phoenix_crown():
    s = fill("M36.6,34 C35.6,26 40,20.6 46.6,19.6 C53.4,18.6 58.4,21.6 59.6,28 C52,28.6 44,30.8 36.6,34 Z", W['gold'])
    s += fill("M44,20.4 C44,14 48,10 52,11.4 C50,13 49.4,15 50.6,17 C53,15.4 56,15.6 57.6,17.4 C54.6,18 52.4,19.6 51,21 Z", W['gold'], 0.8)
    s += C_(52.6, 13.6, 0.7, INK)
    for x0 in (60.4, 36):
        for i in range(4):
            s += C_(x0, 29 + i * 2.8, 0.85, W['red'], INK, 0.3)
    s += ink("M38,31 C45,28.6 52,27.4 59,27.4", 0.6)
    return s


def helmet_cn(col=None, tassel=True):
    col = col or W['gold']
    s = fill("M31.6,46 C28.6,33 35,22.4 46.4,21 C55.6,20 61.4,24.8 62.4,32.6 C52.6,33.8 42.6,38.6 36,45.6 Z", col)
    s += fill("M31.4,44.6 C26,46 22.6,51 22,57 C26.6,55 30.4,53.4 34,53.6 Z", col, 0.9)            # neck flap
    s += fill("M35.6,33 C31,29 26,28 21,30.4 C25,32.4 28.6,35.6 31.4,39 Z", col, 0.8)             # phoenix wing
    s += ink("M37.4,41 C45,35.8 53,33 62,32.4", 1.0)
    if tassel:
        s += P("M46.4,21 L46,14", 'none', INK, 1.4)
        s += fill("M46,14.6 C42,12 40,7 42,3 C44.6,6 46.4,6 48,3 C50.4,7 49.6,12 46,14.6 Z", W['red'], 0.8)
    return s


def three_peak_cap(col=None):
    col = col or W['gold']
    s = fill("M33.2,42.6 C31,33 35.6,24.6 44.6,22.8 C52.6,21.4 58.4,24.6 59.6,31 C50.6,32.6 41.4,36.6 33.2,42.6 Z", col)
    for (x, h) in [(38, 10), (46.4, 14), (54.6, 10.6)]:
        s += fill(f"M{x-3.4},{27 if x < 50 else 25} L{x},{24-h} L{x+3.4},{26 if x < 50 else 24.4} Z", col, 0.9)
    s += ink("M34.6,39.6 C42.6,35 50.6,32.4 59.6,31", 1.0)
    return s


def third_eye():
    return (fill("M58.2,31.6 C56.8,33.6 56.8,36.4 58.2,38.6 C59.8,36.4 59.8,33.6 58.2,31.6 Z", W['white'], 0.9)
            + dot(58.2, 35.1, 1.0) + P("M58.2,30.4 L58.2,31.4 M58.2,38.8 L58.2,39.8", 'none', W['red'], 0.9))


def curls():
    """Buddha's snail-shell curls and ushnisha (螺发肉髻)."""
    s = fill("M33,44 C30.6,33 36,24.6 46,23.4 C54,22.6 59.8,26.6 60.4,33 C52,33.2 42,37.6 33,44 Z", W['indigo'])
    s += fill("M40.4,25.8 C40,19 44,15 48.6,15.2 C53.4,15.4 56,19.4 55,25.4 C50,24 45,24.2 40.4,25.8 Z", W['indigo'])
    for (x, y) in [(37, 38), (40.6, 34), (44.6, 30.6), (48.8, 28), (53, 27.4), (56.8, 29.4), (41.4, 39.4), (45.4, 35.6),
                   (49.6, 32.6), (53.6, 31.4), (36.6, 32.4), (40.4, 29), (44.6, 26), (44.2, 20), (48.4, 18.4), (52.2, 20.4), (48, 22.6)]:
        s += C_(x, y, 1.15, 'none', W['white'], 0.5)
    s += C_(58.8, 34.8, 1.1, W['red'], INK, 0.3)    # urna
    return s


def hood():
    """Guanyin's white hood falling to the shoulders."""
    d = ("M60,31 C59,22 51,16.6 42,18.2 C31.6,20.2 25.4,30.6 25.6,43.6 C25.8,54.6 29.2,62.6 27.4,72.6 "
         "C26.2,80 21.6,88 17,100 L46,100 C41.6,93 39.6,86 40.6,79.4 C41.4,73.8 40.6,69.4 38.8,66.2 "
         "C34.2,60 33.4,51.4 35.2,43.8 C37.2,36.2 43.2,31 51.4,29.8 C54.4,29.4 57.4,29.8 60,31 Z")
    s = fill(d, W['white'])
    s += ink("M33,24 C29.5,32 28.6,44 30.4,56 C31.6,64 31,74 26.6,86 M40.6,19.4 C35,26 32.6,36 33.2,46", 0.6)
    # small crown with a seated buddha
    s += fill("M47,22.6 C46.6,18 49.4,15.2 52.6,15.4 C55.6,15.6 57.4,18.4 57,22 C54,22.4 50,22.6 47,22.6 Z", W['gold'], 0.8)
    s += C_(52.2, 18.6, 1.3, W['red'], INK, 0.3)
    return s


def high_bun(col=INK, ornament=True):
    s = hair('bun', col)
    s += P("M40,27 C37,19 41,11 48,10 C54,9.6 58,14 56.6,20 C54,22 50,24 45,26 Z", col, INK, LW)
    if ornament:
        s += P("M36,20 L58,12", 'none', W['gold'], 1.6) + ink("M36,20 L58,12", 0.4)
        s += C_(57.6, 12.4, 1.8, W['red'], INK, 0.5)
    return s


def flower(x, y, col=None, r=2.2):
    col = col or W['red']
    s = ''
    for k in range(5):
        a = k * 2 * math.pi / 5
        s += C_(round(x + r * 0.9 * math.cos(a), 2), round(y + r * 0.9 * math.sin(a), 2), r * 0.62, col, INK, 0.35)
    return s + C_(x, y, r * 0.4, W['gold'], INK, 0.3)


# ------------------------------------------------------------------ attributes
def staff_rings(x0=80, y0=100, x1=86, y1=8):
    """Monk's ringed staff (锡杖)."""
    s = P(f"M{x0},{y0} L{x1},{y1+10}", 'none', W['brown'], 2.2) + ink(f"M{x0},{y0} L{x1},{y1+10}", 0.4)
    s += fill(f"M{x1},{y1+11} C{x1-7},{y1+9} {x1-7},{y1-1} {x1},{y1-3} C{x1+7},{y1-1} {x1+7},{y1+9} {x1},{y1+11} Z", 'none', 1.3)
    s += P(f"M{x1},{y1+11} C{x1-7},{y1+9} {x1-7},{y1-1} {x1},{y1-3} C{x1+7},{y1-1} {x1+7},{y1+9} {x1},{y1+11} Z", 'none', W['gold'], 0.8)
    for dx, dy in [(-5.4, 2), (-5.6, 7), (5.4, 2), (5.6, 7)]:
        s += C_(x1 + dx, y1 + dy, 1.6, 'none', INK, 0.7)
    return s


def iron_staff(x0=78, y0=100, x1=88, y1=0):
    s = P(f"M{x0},{y0} L{x1},{y1}", 'none', INK, 4.2) + P(f"M{x0},{y0} L{x1},{y1}", 'none', W['red'], 2.8)
    for t0, t1 in [(0.0, 0.1), (0.9, 1.0)]:
        ax, ay = x0 + (x1 - x0) * t0, y0 + (y1 - y0) * t0
        bx, by = x0 + (x1 - x0) * t1, y0 + (y1 - y0) * t1
        s += P(f"M{ax:.1f},{ay:.1f} L{bx:.1f},{by:.1f}", 'none', W['gold'], 2.8)
    return s


def rake():
    s = P("M72,100 L88,22", 'none', W['brown'], 2.2) + ink("M72,100 L88,22", 0.4)
    s += fill("M74,22.6 L100,17.4 L100.6,21.6 L75,26.6 Z", W['grey'], 0.9)
    for i in range(9):
        x = 75.4 + i * 2.9
        y = 26.2 - i * 0.58
        s += P(f"M{x:.1f},{y:.1f} L{x+0.8:.1f},{y+6:.1f}", 'none', INK, 1.1)
    return s


def moon_spade():
    """Sha Wujing's demon-quelling staff with a crescent blade."""
    s = P("M74,100 L88,14", 'none', W['brown'], 2.2) + ink("M74,100 L88,14", 0.4)
    s += fill("M80,8 C84,14 92,16 97,12 C94,17 90,20 86,19 L89.6,13 Z", W['grey'], 0.9)
    s += fill("M86.4,19 L90.8,19.8 L90.2,23.6 L85.6,22.6 Z", W['gold'], 0.6)
    return s


def skulls():
    s = ''
    for i in range(7):
        t = i / 6
        x = 42 + t * 22
        y = 81 + 9 * math.sin(t * math.pi)
        s += C_(round(x, 1), round(y, 1), 2.3, W['bone'], INK, 0.6)
        s += dot(round(x + 0.8, 1), round(y - 0.2, 1), 0.45)
    return s


def palm(x=84, y=42):
    """The Buddha's raised palm (五行山)."""
    g = f'<g transform="translate({x} {y})">'
    g += fill("M-7,40 L-7,14 C-8,10 -8,6 -6,4 L-6,-10 C-6,-12.6 -2.6,-12.6 -2.6,-10 L-2.6,1 L-2.2,-15 C-2.2,-17.6 1.4,-17.6 1.4,-15 "
              "L1.6,0.6 L2.2,-13 C2.2,-15.6 5.8,-15.6 5.8,-13 L5.8,1.6 L6.4,-8.4 C6.4,-11 9.8,-11 9.8,-8.4 L9.6,8 "
              "C9.6,14 7.6,18 6,22 L6,40 Z", SKIN, 1.0)
    g += fill("M-6,6 C-10,2 -13,-2 -12.6,-5.6 C-11,-7.2 -8.4,-5.6 -6.4,-1.6", SKIN, 0.9)
    g += ink("M-3,10 C0,12 3,12 6,10", 0.5)
    g += '</g>'
    return g


def vase_willow():
    s = fill("M80,90 C74,86 73,76 77,70 C78.6,67.4 79,64 78.6,60 L85.4,60 C85,64 85.4,67.4 87,70 C91,76 90,86 84,90 Z", W['white'])
    s += fill("M78,58 L86,58 L85.4,61 L78.6,61 Z", W['gold'], 0.7)
    s += ink("M82,58 C81,48 84,38 90,28", 1.0)
    for (x, y, a) in [(83.2, 46, -40), (85, 40, 30), (87.2, 34.4, -40), (88.6, 30, 30), (82.4, 51, 40)]:
        s += f'<ellipse cx="{x}" cy="{y}" rx="3.6" ry="1.2" transform="rotate({a} {x} {y})" fill="{W["green"]}" stroke="{INK}" stroke-width="0.5"/>'
    return s


def sack():
    s = fill("M70,100 C66,86 68,72 78,66 C84,62.6 92,64 96,70 C100,78 99,90 96,100 Z", W['ochre'])
    s += fill("M80,66 C79,62 81,58 84,57 C86,58 87.4,61.4 86,65.6 Z", W['ochre'], 0.9)
    s += ink("M78,70 C82,72 88,72 92,69 M74,82 C80,84 88,84 96,82", 0.6)
    return s


def sword(x0=74, y0=100, x1=90, y1=14, col=None):
    col = col or W['white']
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    px, py = -uy, ux
    hx, hy = x0 + ux * 22, y0 + uy * 22
    s = P(f"M{x0},{y0} L{hx:.1f},{hy:.1f}", 'none', W['brown'], 2.6)
    s += P(f"M{hx + px*4.4:.1f},{hy + py*4.4:.1f} L{hx - px*4.4:.1f},{hy - py*4.4:.1f}", 'none', W['gold'], 2.2)
    s += fill(f"M{hx + px*1.6:.1f},{hy + py*1.6:.1f} L{x1 + px*1.2:.1f},{y1 + py*1.2:.1f} L{x1 + ux*3:.1f},{y1 + uy*3:.1f} "
              f"L{x1 - px*1.2:.1f},{y1 - py*1.2:.1f} L{hx - px*1.6:.1f},{hy - py*1.6:.1f} Z", col, 0.8)
    return s


def ruyi(x=80, y=60):
    s = P(f"M{x-6},{y+34} C{x-2},{y+20} {x+2},{y+8} {x+4},{y}", 'none', W['gold'], 2.4) + ink(f"M{x-6},{y+34} C{x-2},{y+20} {x+2},{y+8} {x+4},{y}", 0.4)
    s += fill(f"M{x+4},{y+2} C{x-4},{y-2} {x-2},{y-12} {x+5},{y-11} C{x+8},{y-15} {x+14},{y-12} {x+12},{y-6} C{x+14},{y-2} {x+8},{y+2} {x+4},{y+2} Z", W['jade'], 0.9)
    s += ink(f"M{x+2},{y-6} C{x+4},{y-9} {x+8},{y-9} {x+9},{y-6}", 0.5)
    return s


def dragon_staff():
    s = P("M74,100 L86,22", 'none', W['brown'], 2.2) + ink("M74,100 L86,22", 0.4)
    s += fill("M86,22 C82,18 82,11 87,8 C91,6 96,8 97,12 L94,13 C95,16 93,19 90,19 L89,24 Z", W['gold'], 0.9)
    s += dot(91, 11.4, 0.7) + ink("M96,12.4 C98,14 99,17 98,20 M94,8 C96,5 99,4 100,5", 0.6)
    return s


def whisk(x0=76, y0=96, x1=84, y1=40):
    s = P(f"M{x0},{y0} L{x1},{y1}", 'none', W['brown'], 2.2) + ink(f"M{x0},{y0} L{x1},{y1}", 0.4)
    for k in range(7):
        dx = -6 + k * 2
        s += P(f"M{x1},{y1} C{x1+dx*0.4},{y1-8} {x1+dx},{y1-16} {x1+dx*1.4},{y1-26}", 'none', W['white'], 1.4)
        s += ink(f"M{x1},{y1} C{x1+dx*0.4},{y1-8} {x1+dx},{y1-16} {x1+dx*1.4},{y1-26}", 0.3)
    return s


def ring(x=84, y=62, r=9, col=None):
    col = col or W['white']
    return (C_(x, y, r, 'none', INK, 4.6) + C_(x, y, r, 'none', col, 3.2)
            + C_(x, y, r, 'none', INK, 0.4).replace('/>', ' stroke-dasharray="1 2.4"/>'))


def hu_tablet():
    return fill("M76,100 L84,50 C85,47 88,47 88.4,50 L82,100 Z", W['jade'], 0.9)


def pearl(x=84, y=64):
    s = C_(x, y, 7, W['white'], INK, 1.0)
    s += P(f"M{x-3},{y-3} C{x-1},{y-5} {x+2},{y-5} {x+3},{y-3}", 'none', W['gold'], 0.9)
    for k in range(6):
        a = k * math.pi / 3
        s += ink(f"M{x + 9*math.cos(a):.1f},{y + 9*math.sin(a):.1f} L{x + 12*math.cos(a):.1f},{y + 12*math.sin(a):.1f}", 0.7)
    return s


def pagoda(x=84, y=40):
    g = f'<g transform="translate({x} {y})">'
    for i, (w, h) in enumerate([(14, 7), (12, 6.4), (10, 5.8), (8.4, 5.2), (6.8, 4.6)]):
        yy = 36 - sum(v[1] for v in [(14, 7), (12, 6.4), (10, 5.8), (8.4, 5.2), (6.8, 4.6)][:i + 1])
        g += fill(f"M{-w/2},{yy+h} L{-w/2+1},{yy+1.6} L{-w/2-1.4},{yy+1.6} L0,{yy-1.2} L{w/2+1.4},{yy+1.6} L{w/2-1},{yy+1.6} L{w/2},{yy+h} Z",
                  W['gold'], 0.8)
        g += C_(0, yy + h * 0.6, 0.8, INK)
    g += ink("M0,6.4 L0,0 M-1.6,2 L1.6,2", 0.9)
    g += fill("M-8,36 L8,36 L7,40 L-7,40 Z", W['gold'], 0.8)
    g += '</g>'
    return g


def peach(x=84, y=66):
    s = fill(f"M{x},{y+8} C{x-9},{y+6} {x-10},{y-4} {x-3},{y-7} C{x-1},{y-8} {x},{y-6} {x},{y-6} C{x+1},{y-8} {x+4},{y-8} {x+6},{y-6} C{x+11},{y-1} {x+8},{y+7} {x},{y+8} Z", W['pink'])
    s += ink(f"M{x},{y-6} C{x-1},{y-1} {x-1},{y+4} {x},{y+8}", 0.6)
    s += f'<ellipse cx="{x+5}" cy="{y-9}" rx="4" ry="1.6" transform="rotate(-25 {x+5} {y-9})" fill="{W["green"]}" stroke="{INK}" stroke-width="0.5"/>'
    return s


def blade_three():
    """Erlang's three-pointed double-edged blade (三尖两刃刀)."""
    s = P("M74,100 L86,26", 'none', W['brown'], 2.2) + ink("M74,100 L86,26", 0.4)
    s += fill("M80.4,28 L82,14 L85,20 L87.6,4 L90.2,20 L93.4,15 L92.6,29 Z", W['white'], 0.9)
    s += fill("M80,28 L93,29.4 L92.4,32 L80.4,31 Z", W['gold'], 0.7)
    return s


def crescent(x=80, y=24, r=12):
    return fill(f"M{x},{y-r} C{x+r*1.2},{y-r*0.6} {x+r*1.2},{y+r*0.9} {x},{y+r} C{x+r*0.5},{y+r*0.3} {x+r*0.5},{y-r*0.4} {x},{y-r} Z", '#f6e7a6', 0.9)


def ribbons():
    return (fill("M44,24 C36,24 30,30 24,32 C28,34 34,32 38,30 C34,36 30,44 22,48 C30,48 38,40 42,30 Z", W['blue'], 0.7))


def ginseng_fruit(x=84, y=64):
    g = f'<g transform="translate({x} {y})">'
    g += fill("M0,-12 C4,-12 6,-9 5.6,-6 C8,-4 9,1 7,6 C9,9 8,13 5,13 L3,10 L1,14 L-1,14 L-3,10 L-5,13 C-8,13 -9,9 -7,6 C-9,1 -8,-4 -5.6,-6 C-6,-9 -4,-12 0,-12 Z", '#e8d7a8', 0.9)
    g += ink("M-2.4,-7.6 L-1.4,-7.2 M1.4,-7.2 L2.4,-7.6 M-1,-4.4 Q0,-3.6 1,-4.4", 0.6)
    g += ink("M-5,0 C-3,2 3,2 5,0", 0.5)
    g += f'<ellipse cx="3" cy="-15" rx="3.4" ry="1.4" transform="rotate(-30 3 -15)" fill="{W["green"]}" stroke="{INK}" stroke-width="0.5"/>'
    g += '</g>'
    return g


def ruler():
    return fill("M76,100 L90,34 L94,35 L80,100 Z", W['brown'], 0.9) + ink("M80.6,80 L84.6,80.8 M82.8,70 L86.8,70.8 M85,60 L89,60.8 M87,50 L91,50.8", 0.5)


def seal(x=84, y=66):
    s = fill(f"M{x-8},{y} L{x+8},{y} L{x+8},{y+12} L{x-8},{y+12} Z", W['jade'])
    s += fill(f"M{x-4},{y} C{x-4},{y-6} {x+4},{y-6} {x+4},{y} Z", W['jade'], 0.9)
    s += fill(f"M{x-6},{y+14} L{x+6},{y+14} L{x+6},{y+22} L{x-6},{y+22} Z", W['vermil'], 0.8)
    s += P(f"M{x-4},{y+16} L{x+4},{y+16} M{x},{y+16} L{x},{y+21} M{x-4},{y+20} L{x+4},{y+20}", 'none', W['white'], 0.9)
    return s


def letter():
    s = fill("M72,66 L94,58 L99,80 L77,88 Z", W['white'])
    for i in range(4):
        s += ink(f"M{77+i*4.4},{65.4-i*1.6} L{81+i*4.4},{84.4-i*1.6}", 0.5, ' stroke-dasharray="2 1.4"')
    return s


def water_drops():
    s = ''
    for (x, y) in [(63, 64), (66.6, 70), (58, 74), (70, 60), (61.4, 80)]:
        s += fill(f"M{x},{y-3} C{x+1.6},{y} {x+1.8},{y+1.6} {x},{y+2.4} C{x-1.8},{y+1.6} {x-1.6},{y} {x},{y-3} Z", '#a9c7d2', 0.5)
    return s


def banana_fan():
    s = P("M68,100 L80,74", 'none', W['brown'], 2.4) + ink("M68,100 L80,74", 0.4)
    s += fill("M79,76 C72,62 74,40 86,26 C94,18 102,22 100,34 C98,48 92,66 81,76 Z", W['green'])
    s += ink("M80,74 C84,58 88,42 95,26", 0.8)
    for t in range(1, 7):
        y = 74 - t * 7.6
        x = 80 + t * 2.3
        s += ink(f"M{x:.1f},{y:.1f} C{x-4:.1f},{y-3:.1f} {x-7:.1f},{y-4:.1f} {x-9:.1f},{y-4:.1f} M{x:.1f},{y:.1f} C{x+3:.1f},{y-2:.1f} {x+6:.1f},{y-4:.1f} {x+7:.1f},{y-7:.1f}", 0.45)
    return s


def fire_spear():
    s = P("M72,100 L88,20", 'none', W['brown'], 2.2) + ink("M72,100 L88,20", 0.4)
    s += fill("M88,20 L86.4,10 L89,4 L91.2,10 Z", W['white'], 0.8)
    s += flames_at(89, 22, 1.0)
    return s


def flames_at(x, y, k=1.0):
    g = f'<g transform="translate({x} {y}) scale({k})">'
    g += fill("M-6,4 C-8,-2 -4,-6 -3,-12 C-1,-8 0,-8 1,-14 C4,-9 6,-4 5,2 C7,0 8,-2 8,-5 C11,0 9,6 4,8 C0,9 -4,8 -6,4 Z", W['vermil'], 0.7)
    g += fill("M-3,4 C-4,0 -2,-3 -1,-6 C1,-3 3,-1 2,3 C1,5 -1,5 -3,4 Z", W['yellow'], 0.4)
    g += '</g>'
    return g


def gourd(x=84, y=70, col=None):
    col = col or W['vermil']
    s = fill(f"M{x},{y-18} C{x+4},{y-18} {x+5},{y-13} {x+3},{y-9} C{x+10},{y-6} {x+11},{y+6} {x},{y+9} "
             f"C{x-11},{y+6} {x-10},{y-6} {x-3},{y-9} C{x-5},{y-13} {x-4},{y-18} {x},{y-18} Z", col)
    s += ink(f"M{x-4},{y-9} C{x-1},{y-8} {x+1},{y-8} {x+4},{y-9}", 0.7)
    s += fill(f"M{x-1},{y-18} L{x+1},{y-18} L{x+1.4},{y-22} L{x-1.2},{y-22} Z", W['brown'], 0.6)
    return s


def cymbal(x=84, y=64):
    s = f'<ellipse cx="{x}" cy="{y}" rx="12" ry="6" fill="{W["gold"]}" stroke="{INK}" stroke-width="1"/>'
    s += f'<ellipse cx="{x}" cy="{y+7}" rx="12" ry="6" fill="{W["gold"]}" stroke="{INK}" stroke-width="1"/>'
    s += f'<ellipse cx="{x}" cy="{y-1}" rx="4" ry="2" fill="{W["yellow"]}" stroke="{INK}" stroke-width="0.7"/>'
    s += ink(f"M{x},{y-3} L{x},{y-8} M{x-2},{y-9} L{x+2},{y-9}", 0.9)
    return s


def bells():
    s = ink("M70,40 C78,44 86,44 96,40", 0.8)
    for (x, y) in [(74, 44), (83, 46), (92, 44)]:
        s += fill(f"M{x-4},{y+8} C{x-4},{y+2} {x-2.6},{y} {x},{y} C{x+2.6},{y} {x+4},{y+2} {x+4},{y+8} Z", W['gold'], 0.8)
        s += C_(x, y + 9, 1.2, INK)
    return s


def lotus_mace():
    s = P("M72,100 L86,40", 'none', W['brown'], 2.2) + ink("M72,100 L86,40", 0.4)
    s += fill("M86,40 C80,36 79,26 84,18 C86,16 88,16 90,18 C95,26 94,36 88,40 Z", '#e6a6a0')
    s += ink("M86,40 C84,32 84,24 87,17 M88,40 C90,32 90,24 87,17", 0.6)
    return s


def pestle():
    return (P("M74,100 L88,36", 'none', W['white'], 4) + ink("M74,100 L88,36", 0.5)
            + fill("M85,38 L86,26 C86,23 92,23 92,26 L91.4,39 Z", W['white'], 0.9))


def twin_swords():
    return sword(70, 100, 84, 18) + sword(80, 100, 96, 22)


def web(x=80, y=26, r=20):
    s = ''
    for k in range(8):
        a = k * math.pi / 4
        s += ink(f"M{x},{y} L{x + r*math.cos(a):.1f},{y + r*math.sin(a):.1f}", 0.5)
    for rr in (5, 10, 15, 20):
        pts = [(x + rr * math.cos(k * math.pi / 4), y + rr * math.sin(k * math.pi / 4)) for k in range(9)]
        d = 'M' + ' L'.join(f'{px:.1f},{py:.1f}' for px, py in pts)
        s += ink(d, 0.45)
    # spider
    s += C_(x + 6, y + 8, 2.4, INK) + C_(x + 6, y + 4.6, 1.4, INK)
    for sgn in (-1, 1):
        for k in range(4):
            s += ink(f"M{x+6},{y+7.6} l{sgn*4:.1f},{-3 + k*2.4:.1f} l{sgn*1.6:.1f},{2:.1f}", 0.5)
    return s


def halberd():
    s = P("M72,100 L88,14", 'none', W['brown'], 2.2) + ink("M72,100 L88,14", 0.4)
    s += fill("M86,20 L89,4 L92,20 Z", W['white'], 0.8)
    s += fill("M88,22 C94,20 98,24 98,30 C94,28 91,28 87.4,28 Z", W['white'], 0.8)
    s += fill("M86.6,24 C81,22 78,26 78,31 C81,29 84,29 87,29.4 Z", W['white'], 0.8)
    s += P("M86.6,30 C84,34 84,38 86,42", 'none', W['red'], 1.8)
    return s


def whip():
    s = P("M72,100 L86,24", 'none', W['dark'], 3)
    for i in range(7):
        t = i / 6
        x = 72 + 14 * t
        y = 100 - 76 * t
        s += ink(f"M{x-2.4:.1f},{y-0.5:.1f} L{x+2.4:.1f},{y+0.5:.1f}", 1.1)
    return s


def trident_cn():
    s = P("M72,100 L86,22", 'none', W['brown'], 2.2) + ink("M72,100 L86,22", 0.4)
    s += ink("M80,24 L92,26 M80,24 C79,18 80,12 82,8 M92,26 C94,20 95,14 94,8 M86,25 L88,6", 1.6)
    return s


def iron_club():
    s = P("M72,100 L90,6", 'none', INK, 4.6) + P("M72,100 L90,6", 'none', W['dark'], 3.2)
    for i in range(1, 6):
        t = i / 6
        x, y = 72 + 18 * t, 100 - 94 * t
        s += P(f"M{x-2.6:.1f},{y-0.4:.1f} L{x+2.6:.1f},{y+0.4:.1f}", 'none', W['grey'], 1)
    return s


def wind_lines():
    s = ''
    for (x, y, l) in [(72, 50, 22), (74, 56, 18), (71, 62, 24)]:
        s += P(f"M{x},{y} c{l*0.3},-3 {l*0.6},3 {l},0", 'none', W['yellow'], 2.2) + ink(f"M{x},{y} c{l*0.3},-3 {l*0.6},3 {l},0", 0.45)
    s += P("M92,46 c3,-2 5,1 3,3 c-2,2 -4,0 -3,-1", 'none', INK, 0.7)
    return s


def tiger_skirt():
    s = fill("M18,100 C22,92 30,88 40,88 L62,88 C72,88 80,92 84,100 Z", W['yellow'])
    for x in (26, 34, 44, 54, 64, 74):
        s += ink(f"M{x},{90} C{x+2},{93} {x},{96} {x+2},{100}", 1.3)
    return s


# ------------------------------------------------------------------ animal heads
def monkey(fur=None, face_col=None, ears=1, band=True):
    fur = fur or W['ochre']
    face_col = face_col or '#ecc0a6'
    s = ''
    # extra ears behind (for the six-eared macaque)
    s += fill("M57,24 C46,19 34.6,24 31.2,36 C28.6,45 30.4,55.6 35.4,62.4 C39.4,68 46,72 53,71.6 C56.4,71.4 59,70 60.4,68 "
              "L60,60 C62,50 61,38 57,24 Z", fur)
    for (x, y, a) in [(33, 34, 200), (30.6, 44, 180), (31.4, 54, 160), (35.4, 62, 140), (42, 68.6, 120), (50, 71.6, 100),
                      (40, 25, 230), (48, 21.4, 260)]:
        r = math.radians(a)
        s += ink(f"M{x:.1f},{y:.1f} l{3*math.cos(r):.1f},{3*math.sin(r):.1f}", 0.8)
    s += fill("M57.4,30 C61,31.6 63.4,35 63.8,39.2 C66,40.4 68.6,43.4 70.4,47.6 C71.4,50 71,52.4 69.6,53.6 C70.4,55.4 70.4,57.6 69,59.4 "
              "C66.8,62.4 62.4,64 58.4,63.6 C55,63.2 52.4,61.4 51.4,58.6 C50.8,56.2 51.8,53.6 53.6,52 C52,49 51.8,45.6 53.4,42.6 "
              "C54.4,40.6 55.2,39 55.2,36.8 C55.2,34 56,31.6 57.4,30 Z", face_col)
    s += ink("M55.2,37.6 C58.6,35.2 62.4,35.6 64.4,38.8", 1.6)                      # brow ridge
    s += P("M56.8,42.6 Q60,40.2 63.2,42.4 Q60,44.6 56.8,42.6 Z", W['gold'], INK, 0.8)  # fiery golden eye
    s += dot(60.2, 42.5, 1.1) + dot(60.7, 42.1, 0.35, W['red'])
    s += ink("M66,47 C67.4,48.6 68.4,50 69.4,50.4", 0.6) + dot(69.6, 51.2, 0.7)
    s += ink("M69.6,56 C67,57.4 64,57.6 61.4,57", 0.9)
    s += ink("M58,48 C60,50.4 61,53 60.6,56", 0.5)
    s += fill("M42.6,40.6 C38.4,39.8 36,43.4 37,47.6 C38,51.4 41.6,52.6 44,50.6 C42.4,48.6 42.2,45 42.6,40.6 Z", face_col, 0.9)
    if ears > 1:   # the six-eared macaque: three ears a side
        for (x, y) in [(40.6, 30.6), (40.6, 58)]:
            s += fill(f"M{x+2},{y-4.4} C{x-3},{y-5.6} {x-5.4},{y-1} {x-4.4},{y+2.6} C{x-3.4},{y+6} {x+1},{y+6} {x+2.6},{y+3.4} C{x+1},{y+1.6} {x+0.6},{y-1.6} {x+2},{y-4.4} Z", face_col, 0.9)
    if band:
        s += P("M59,31.2 C51,33 42,36.4 33,42.6", 'none', INK, 4.4) + P("M59,31.2 C51,33 42,36.4 33,42.6", 'none', W['gold'], 3.0)
    return s


def pig():
    skin = '#cdbdb1'
    s = fill("M54,25.6 C44,22 33.6,28 31.2,40 C29.4,50 33,60 40,66.4 C45,70.6 52,71.8 58,70 "
             "C61,69 63.6,66.6 65.6,64.4 L73.6,59 C75.6,58 76.6,55.6 76,53 C75.4,50.2 74,47.8 72,46.4 "
             "L63.6,36 C61.6,31.4 58.6,27.4 54,25.6 Z", skin)
    s += f'<ellipse cx="75.4" cy="52.6" rx="3.2" ry="6.4" fill="#c9bfb2" stroke="{INK}" stroke-width="1"/>'
    s += dot(75, 50.4, 0.8) + dot(75.6, 55, 0.8)
    s += ink("M72.4,58.6 C68,60.6 63.6,61 60,60.4", 0.9)
    s += ink("M63,58.8 L64.6,54.6 L66,58.6", 0.8)                                       # little tusk
    s += dot(58.8, 42.6, 1.1) + ink("M56,40.4 Q58.6,39 61.4,40.4", 0.9)
    s += ink("M62,46 C64,48 66,52 66,56", 0.5)
    for (x, y) in [(40, 32), (36, 40), (35, 50), (38, 58), (44, 64)]:
        s += ink(f"M{x},{y} l-2.4,-1.4", 0.6)
    # the big flopping ear
    s += fill("M44,30.4 C48,26.4 55,26 58.6,29.4 C61.6,32.6 62,38.6 59,44.6 C57,48.4 53,49.6 51,47 C49,44 47,38 44,30.4 Z", '#dccdc2')
    s += ink("M47,32 C50.4,34 53,38.6 53.6,44", 0.6)
    return s


def horse_head(col=None):
    col = col or W['white']
    s = fill("M30,100 C30,86 33,74 38,62 C40,54 43,46 47,40 L45.6,31 L50.4,36.4 L52.6,30 L54.2,38.4 "
             "C60,42 66,48 70.6,55 C72.6,58 72.4,62.4 69.6,64 C66.6,65.6 62.6,64.2 59.6,62 "
             "C56.6,70 56,84 60,100 Z", col)
    for (x, y) in [(46, 44), (42.6, 50), (40, 56), (37.6, 62), (35.6, 68), (34, 74)]:
        s += P(f"M{x},{y} C{x-5},{y+0.4} {x-8},{y+3} {x-9},{y+6} C{x-6},{y+4.6} {x-3},{y+4} {x-1},{y+4}", W['jade'], INK, 0.6)
    s += dot(56, 45.4, 1.2) + ink("M53.6,43.6 Q56,42.4 58.6,43.8", 0.8)
    s += ink("M66.6,58.4 C68.6,59 69.6,60 70,61.4", 0.6) + dot(68.4, 58.6, 0.6)
    s += ink("M52,46 C56,50 58,56 59.6,62 M62,52 L70.4,56.6", 0.9)                     # bridle
    s += P("M52.6,47.6 C51,52 50,56 51,60", 'none', W['red'], 2) + C_(51, 61, 1.8, W['red'], INK, 0.4)
    s += ink("M71,63 C75,64 78,62 80,58 M69,64.6 C72,68 76,69 80,68", 0.6)            # dragon whiskers
    return s


def bull_head(col=None, horns=2, horn_col=None):
    col = col or W['white']
    horn_col = horn_col or W['ochre']
    s = ''
    if horns == 2:
        s += fill("M40,34 C33,29 29,21 31,12 C32,10 34.4,10 35,12.4 C35.4,19 39,25 45,29.6 Z", horn_col, 0.9)   # far horn
    s += fill("M34,66 C30,58 30,46 34,38 C38,30 46,26 54,27 C61,28 66,32 69,38 C72,43 74,48 75,53 "
              "C76,59 74,64 70,66 C66,68 62,67 59,65 C55,69 48,71 42,70 C38,69 36,68 34,66 Z", col)
    s += f'<ellipse cx="69" cy="58" rx="6.6" ry="7.4" fill="{W["pink"]}" stroke="{INK}" stroke-width="0.9"/>'
    s += fill("M70.4,54.6 C72,54.4 73,55.6 72.4,57 C71.2,57.4 70.2,56.4 70.4,54.6 Z", INK, 0.4)
    s += C_(70, 65.4, 3, 'none', INK, 1.6) + C_(70, 65.4, 3, 'none', W['gold'], 0.9)          # nose ring
    s += fill("M38,42 C32,40 26,42 23,46.6 C27.4,48.6 33,47.6 38,45.4 Z", col, 0.9)            # ear
    if horns == 2:
        s += fill("M47,29 C45,20 49,12 57,8.4 C61,7 64.6,7.6 66,9.6 C60,10.6 55.6,14 54,19.6 C53.2,23 53.4,26 54.4,28.4 Z", horn_col)
    else:
        s += fill("M53,29.4 C53,20 57,12 63,6.6 C62.6,14 61.6,22 59.6,29.6 Z", horn_col)
    s += dot(56, 40.6, 1.4) + ink("M52.4,37.6 Q56,35.6 59.6,37.8", 1.2)
    s += ink("M44,52 C46,56 50,58 54,58", 0.5)
    return s


def bear_head():
    s = fill("M34,64 C29,56 28,44 32,36 C36,28 44,24 52,25 C58,26 63,30 66,36 C69,40 72,44 74,48 "
             "C75.6,52 74.4,56 71,57 C67,58 63,58 60,58 C57,64 50,68 44,68 C40,68 36,66 34,64 Z", INK)
    s += fill("M36,30 C33,24 36,19 41,19 C44,20 45,23 44,26 Z", INK) + fill("M38.6,27 C37,24 38.6,21.6 41,21.8", '#6a625a', 0.5)
    s += fill("M60,44 C64,43 70,45 73.6,48.4 C74.8,52 73.4,55.4 70.4,56 C66,57 62,56 60,54 Z", '#6a625a', 0.7)
    s += C_(73.4, 49.4, 1.8, INK)
    s += C_(55.6, 38.6, 1.4, PAPER) + dot(55.8, 38.6, 0.7)
    for (x, y) in [(36, 40), (38, 50), (44, 34), (48, 60)]:
        s += P(f"M{x},{y} l3,1.6", 'none', '#7a7068', 0.8)
    return s


def marten_head():
    col = W['yellow']
    s = fill("M34,64 C29,56 29,44 33,37 C37,30 45,27 53,28 C59,29 63,33 66,38 L77,47 C79,49 78.6,51.6 76,52.4 "
             "L66,55 C61,60 54,64 47,66 C42,67 37,66 34,64 Z", col)
    s += fill("M42,32 C38,26 40,20 45,20 C48,21 49,25 47,29 Z", col, 0.9)
    s += dot(77, 49.2, 1.1)
    s += dot(58.6, 39.6, 1.1) + ink("M55.4,37.4 Q58.6,35.8 61.8,37.6", 0.9)
    for dy in (-1.6, 0.4, 2.4):
        s += ink(f"M72,{50+dy} L86,{47+dy*2.2}", 0.45)
    s += ink("M66,55 C62,55.4 58,55 55,54", 0.7)
    return s


def lion_head(mane=None, face_col=None, long_snout=False):
    mane = mane or W['jade']
    face_col = face_col or W['ochre']
    s = fill("M52,20 C40,16 28,24 25,36 C22,48 25,60 32,68 C38,74 46,76 52,74 C56,72 58,68 58,64 L58,30 Z", mane)
    for (x, y) in [(30, 32), (27, 42), (27.4, 52), (30.6, 61), (37, 68.4), (45, 72), (36, 24), (44, 20), (34, 44), (36, 56), (42, 64), (40, 34), (46, 28)]:
        s += f'<path d="M{x-2.6},{y} a2.6,2.6 0 1,1 2.6,2.6" fill="none" stroke="{INK}" stroke-width="0.7"/>'
    snout = 8 if long_snout else 0
    s += fill(f"M52,28 C58,27 63,30 66,35 C70,36 {74+snout},40 {76+snout},46 C{77+snout},50 {76+snout},53 {73+snout},54 "
              f"C{75+snout},56 {75+snout},59 {72+snout},61 C{66+snout},64 58,64 54,62 C50,58 49,50 50,42 C50,36 50,31 52,28 Z", face_col)
    s += C_(62, 40, 2.8, W['white'], INK, 0.9) + dot(63, 40, 1.3)
    s += ink("M57,35.4 C60,33 65,33 68,36", 1.4)
    s += dot(74 + snout, 47, 1.4)
    s += fill(f"M{56+snout*0.5},57 C{62+snout*0.6},58 {68+snout},57.6 {72+snout},55.6 C{70+snout},60 {64+snout*0.6},61.6 {58+snout*0.5},60 Z", W['red'], 0.7)
    s += P(f"M{60+snout*0.5},57.6 L{61+snout*0.5},59.6 L{62.4+snout*0.5},57.8 M{66+snout*0.8},57.4 L{67+snout*0.8},59.4 L{68.2+snout*0.8},57.2", 'none', W['white'], 0.8)
    return s


def elephant_head():
    col = '#f1ebdc'
    s = fill("M36,70 C30,60 29,46 34,36 C39,26 50,21 60,24 C68,26 72,32 73,40 C74,48 72,54 70,58 "
             "C71,66 74,74 78,80 C81,85 82,90 78,93 C75,95 72,92 72,88 C71,84 70,80 67,74 C64,70 60,66 56,64 C50,70 42,72 36,70 Z", col)
    s += fill("M40,32 C30,30 22,38 22,50 C22,60 28,66 36,66 C42,64 44,56 44,48 C44,40 43,35 40,32 Z", '#e6ddca', 1.0)
    s += ink("M28,42 C30,50 30,56 32,60 M34,38 C35,46 36,52 38,58", 0.5)
    s += fill("M62,62 C68,66 74,66 80,62 C76,68 70,70 64,68 Z", W['bone'], 0.9)   # tusk
    s += dot(58.4, 40, 1.1) + ink("M55.6,38 Q58.4,36.6 61.2,38.2", 0.9)
    for y in (70, 76, 82):
        s += ink(f"M{68 + (y-70)*0.5},{y} l5,-1.6", 0.45)
    return s


def bird_head(col=None, crest=True):
    col = col or W['gold']
    s = ''
    if crest:
        for (x, y, a) in [(40, 22, 220), (35, 26, 200), (44, 20, 240)]:
            r = math.radians(a)
            s += fill(f"M{x},{y} L{x + 12*math.cos(r):.1f},{y + 12*math.sin(r):.1f} L{x + 4:.1f},{y + 3:.1f} Z", W['red'], 0.7)
    s += fill("M34,66 C29,56 29,42 35,32 C40,24 50,21 58,24 C63,26 66,30 67,35 L72,38 C78,40 82,44 82,50 "
              "C81,54 78,55 76,52 C75,50 73,48 70,48 L66,50 C63,56 57,62 50,66 C45,69 38,69 34,66 Z", col)
    s += fill("M67,35 L72,38 C78,40 82,44 82,50 C81,54 78,55 76,52 C75,50 73,48 70,48 L66,50 C66,45 66.4,40 67,35 Z", W['white'], 0.9)
    s += C_(59, 36.6, 2.4, W['white'], INK, 0.8) + dot(59.6, 36.6, 1.2)
    s += ink("M54,33 C58,31 63,32 66,34.4", 1.4)
    for (x, y) in [(40, 40), (44, 48), (38, 54), (46, 58), (52, 52)]:
        s += ink(f"M{x},{y} c2,2 4,2 6,0", 0.6)
    return s


def wings_back(col=None):
    col = col or W['gold']
    s = fill("M30,66 C16,60 6,44 4,24 C10,30 14,32 18,33 C12,26 10,18 11,10 C17,18 22,22 27,24 C24,16 25,8 28,3 "
             "C33,16 38,28 42,38 C42,50 38,60 30,66 Z", col, 0.9)
    for d in ["M32,58 C22,52 14,42 9,30", "M35,48 C28,42 21,34 16,20", "M38,40 C33,32 29,22 28,8"]:
        s += ink(d, 0.5)
    return s


def fish_head():
    col = '#e0703a'
    s = fill("M30,70 C26,58 28,42 36,32 C44,24 56,22 66,28 C74,33 78,42 78,50 C78,56 75,60 72,62 "
             "C66,66 58,68 50,70 C44,72 36,72 30,70 Z", col)
    s += fill("M36,34 C30,24 32,14 38,8 C40,16 44,22 50,26 Z", col, 0.9)              # dorsal fin
    s += ink("M40,28 C38,22 38,16 39,12 M44,26 C43,20 43,16 44,12", 0.5)
    s += C_(64, 38, 5.6, W['gold'], INK, 1.0) + C_(65, 38, 2.6, INK)                  # bulging eye
    s += fill("M72,52 C76,52 79,54 79,57 C76,58 73,57 71,55 Z", '#c85530', 0.8)        # mouth
    s += ink("M54,32 C50,40 50,52 56,62", 1.0)                                         # gill
    for (x, y) in [(44, 44), (40, 52), (46, 58), (38, 60), (48, 50), (42, 36)]:
        s += f'<path d="M{x},{y} a3,3 0 0,1 3,-3" fill="none" stroke="{INK}" stroke-width="0.6"/>'
    s += fill("M52,64 C50,72 44,76 38,78 C42,72 44,68 46,64 Z", '#f0a070', 0.7)          # pectoral fin
    return s


def rabbit_head():
    col = W['white']
    s = fill("M44,34 C38,22 36,8 40,2 C44,4 48,16 50,30 Z", col) + fill("M42.6,30 C40,20 39.6,10 41,6", '#f0c4c0', 0.4)
    s += fill("M50,32 C48,20 50,8 55,4 C58,8 57,20 55,32 Z", col) + fill("M52,28 C51,20 52,12 54.6,8", '#f0c4c0', 0.4)
    s += fill("M34,66 C30,58 30,46 35,38 C40,31 48,29 55,31 C62,33 66,38 69,44 C71,48 71.6,52 70,55 "
              "C68,58 64,60 60,60 C56,66 48,70 42,70 C38,70 36,68 34,66 Z", col)
    s += C_(58, 43, 1.6, W['red'], INK, 0.6)
    s += fill("M68.6,49 C70,49 71,50.4 70.4,51.6 C69.4,52 68.4,51 68.6,49 Z", W['pink'], 0.5)
    s += ink("M70,53 C68,56 65,56.6 62.6,56 M66,50 L80,46 M66,52 L80,52 M66,54 L79,57", 0.45)
    s += flower(50, 31, W['pink'], 2.6)
    return s


def mouse_head():
    col = W['white']
    s = fill("M34,66 C30,58 30,46 35,39 C40,32 48,30 55,32 C61,34 65,38 68,43 L79,50 C81,52 80.6,54.6 78,55 "
              "L68,57 C63,62 55,66 48,68 C42,69 37,68 34,66 Z", col)
    s += C_(46, 32, 9, '#f4e6e0', INK, 1.0) + C_(46, 32, 5.4, '#eec1bb', INK, 0.5)       # big round ear
    s += C_(79, 52, 2.2, W['gold'], INK, 0.7)                                          # golden nose
    s += dot(62, 43, 1.3)
    s += ink("M72,52 L88,48 M72,54 L88,55 M71,56 L86,61", 0.45)
    s += ink("M68,57 C64,58 60,57.6 57,56.6", 0.7)
    s += P("M40,24 L52,20", 'none', W['gold'], 1.4) + C_(52.4, 20, 1.6, W['red'], INK, 0.4)
    return s


def alligator_head():
    col = '#8a9a78'
    s = fill("M32,68 C28,58 29,46 35,38 C40,32 48,30 56,31 L82,40 C87,42 88,46 85,48 L66,49 L86,52 C88,54 87,57 83,57 "
             "L60,58 C56,64 48,68 42,69 C38,70 34,70 32,68 Z", col)
    for x in range(64, 86, 4):
        s += fill(f"M{x},48.6 L{x+1.2},51.6 L{x+2.4},48.8 Z", W['white'], 0.4)
    s += C_(56, 36.6, 2.6, W['yellow'], INK, 0.8) + ink("M56,35 L56,38.4", 1.1)
    s += ink("M50,32 C54,29 58,30 61,33", 1.2)
    for (x, y) in [(40, 42), (46, 40), (38, 50), (44, 48), (50, 46), (40, 58), (46, 56), (52, 54)]:
        s += P(f"M{x},{y} l3,-1.6 l3,1.6 l-3,1.6 Z", 'none', INK, 0.5)
    for x in (36, 42, 48):
        s += fill(f"M{x},34 L{x+2},28 L{x+4},34 Z", col, 0.6)
    return s


def dragon_head(col=None):
    col = col or W['jade']
    s = ''
    s += fill("M44,30 C42,20 38,14 32,12 C36,10 40,12 42,16 C42,10 40,6 36,4 C42,4 46,10 47,18 L49,28 Z", W['ochre'], 0.8)  # antler
    s += fill("M34,68 C29,58 29,46 35,38 C40,31 48,28 56,30 C62,32 66,36 70,40 L82,44 C86,46 86,50 83,51 L72,52 "
              "L80,56 C82,58 80,61 77,60 L64,58 C60,64 52,68 45,69 C40,70 36,70 34,68 Z", col)
    s += C_(80, 45.8, 1.2, INK)
    s += C_(58, 38.4, 2.8, W['white'], INK, 0.8) + dot(59, 38.4, 1.3)
    s += ink("M52,34 C56,31 61,32 65,35", 1.4)
    s += ink("M72,52 L66,53", 0.8)
    s += P("M80,48 C88,50 94,56 96,64 C97,70 94,74 90,74", 'none', INK, 0.9)      # whiskers
    s += P("M78,50 C84,54 88,60 88,66", 'none', INK, 0.7)
    for (x, y) in [(40, 38), (36, 46), (35, 54), (38, 62), (44, 66)]:
        s += P(f"M{x},{y} C{x-5},{y-1} {x-8},{y+1} {x-10},{y+4} C{x-6},{y+3} {x-3},{y+3} {x-1},{y+4}", W['blue'], INK, 0.6)
    return s


def skull_face():
    """Lady White Bone: a woman's hair and hairpin around a skull."""
    s = hair('long')
    s += fill("M57,28 C62,33 64,39 64,44 L68,50 C68.6,52 67.6,53 65.6,53.4 C66,56 65,58 63,59 C63.6,62 62,65 58.6,66 "
              "C54,67 48,66 45,62 C40,62 36,58 34.6,52 C33,44 35,34 42,29 C47,26 53,26 57,28 Z", W['bone'])
    s += fill("M52.6,38 C56,36.6 60,37.4 61.6,40.6 C61,44 57.6,45.6 54,44.4 C52,43 51.6,40 52.6,38 Z", INK, 0.6)
    s += fill("M64,48 L66.4,52 L63,52 Z", INK, 0.5)
    s += ink("M58,59 L66,58.4", 0.8)
    for x in (58.6, 60.8, 63):
        s += ink(f"M{x},57 L{x},61", 0.6)
    s += ink("M44,48 C46,52 48,54 52,55", 0.6)
    s += P("M34,34 L58,24", 'none', W['gold'], 1.6) + flower(58, 24, W['red'], 2)
    return s


def nine_heads():
    s = ''
    s += fill("M26,100 C20,86 24,74 34,68 C44,62 58,64 66,72 C72,78 74,90 72,100 Z", INK)
    s += fill("M30,82 C20,78 10,82 4,90 C14,88 22,88 30,90 Z", INK, 0.8)
    s += P("M36,80 C44,76 54,76 62,82 M34,88 C44,84 56,84 66,90", 'none', '#5a524a', 0.9)

    def bhead(x, y, a, sc=1.0):
        g = f'<g transform="translate({x} {y}) rotate({a}) scale({sc})">'
        g += fill("M-6,-4 C-2,-7 4,-6 7,-3 L13,-1 L7,1.4 C4,4 -2,5 -6,3 Z", INK, 0.6)
        g += fill("M-5,-4 L-8,-9 L-2,-6 Z", W['red'], 0.5)
        g += C_(2, -2, 1.1, W['yellow'])
        g += '</g>'
        return g
    necks = [("M50,68 C46,56 40,46 30,40", 30, 40, 200), ("M54,66 C54,52 52,38 46,26", 46, 26, -110),
             ("M58,68 C62,54 66,42 66,28", 66, 28, -80), ("M62,70 C70,60 78,52 86,46", 86, 46, -30),
             ("M64,74 C74,72 82,70 92,66", 92, 66, -10), ("M48,70 C40,64 30,60 20,58", 20, 58, 190),
             ("M56,66 C58,56 58,46 56,36", 56, 36, -95)]
    for d, x, y, a in necks:
        s += P(d, 'none', INK, 4)
    for d, x, y, a in necks:
        s += bhead(x, y, a, 0.85)
    return s


# ------------------------------------------------------------------ characters
GODS = {'rulai', 'guanyin', 'maitreya', 'manjushri', 'samantabhadra', 'lingji', 'jade', 'queenmother', 'laojun',
        'jinxing', 'erlang', 'lijing', 'nezha', 'change', 'zhenyuan', 'subodhi', 'aoguang', 'aorun'}
DEMON_GROUND = {'bull', 'ironfan', 'redboy', 'jadeface', 'whitebone', 'yellowrobe', 'goldhorn', 'silverhorn', 'blackbear',
                'yellowwind', 'greenox', 'greenlion', 'whiteelephant', 'roc', 'yellowbrow', 'saitaisui', 'goldfish',
                'jaderabbit', 'mouse', 'spiders', 'sixear', 'ninehead', 'tuolong'}


def draw(pid):
    s = ''
    if pid == 'tangseng':
        s = staff_rings() + cassock() + person(hair_kind=None) + pilu_crown()
    elif pid == 'wukong':
        s = iron_staff() + robe(W['yellow'], W['red']) + tiger_skirt() + big(monkey(), 1.2, 50, 50, -2, -5)
    elif pid == 'bajie':
        s = f'<g transform="translate(-6 10)">{rake()}</g>' + robe(W['indigo'], W['white']) + big(pig(), 1.14, 50, 50, -2, -4)
    elif pid == 'shaseng':
        s = moon_spade() + robe(W['ochre'], W['white']) + person('#b9c4c4', hair_kind=None, beard_kind='short', beard_col='#b8452e') + skulls()
        s += ''.join(dot(x, y, 0.4, INK) for x, y in [(40, 34), (44, 31), (48, 29.6), (38, 39), (42, 36.4)])
    elif pid == 'horse':
        s = big(horse_head(), 1.16, 50, 60, 2, -2)
    elif pid == 'rulai':
        s = palm(84, 42) + cassock(W['vermil']) + person(hair_kind=None, eye_kind='closed', show_ear=False) + ear(lobe=True) + curls()
    elif pid == 'guanyin':
        s = vase_willow() + robe(W['white'], W['jade']) + person(hair_kind=None, eye_kind='closed', show_ear=False) + hood()
    elif pid == 'maitreya':
        s = sack() + robe(W['ochre'], W['vermil']) + head() + ear(lobe=True) + eye('laugh') + face(smile=True)
        s += ink("M60,58 C58,60 55,61 52,60", 0.6)
    elif pid == 'manjushri':
        s = sword() + robe(W['green'], W['gold']) + person(hair_kind=None, show_ear=False) + bodhi_crown() + ear(lobe=True)
    elif pid == 'samantabhadra':
        s = ruyi(80, 58) + robe(W['white'], W['gold']) + person(hair_kind=None, show_ear=False) + bodhi_crown(W['jade']) + ear(lobe=True)
    elif pid == 'lingji':
        s = dragon_staff() + robe(W['blue'], W['gold']) + person(hair_kind=None, show_ear=False) + bodhi_crown() + ear(lobe=True)
    elif pid == 'jade':
        s = robe(W['yellow'], W['red']) + person(hair_kind='short', beard_kind='thin') + mian()
    elif pid == 'queenmother':
        s = peach() + robe(W['vermil'], W['gold']) + person(hair_kind='bun', show_ear=True) + phoenix_crown()
    elif pid == 'laojun':
        s = ring(84, 62, 8.6) + robe(W['white'], W['indigo']) + person(hair_kind='short', hair_col=W['white'], beard_kind='long', beard_col=W['white'], old=True) + dao_crown()
    elif pid == 'jinxing':
        s = whisk() + robe(W['jade'], W['white']) + person(hair_kind='short', hair_col=W['white'], beard_kind='long', beard_col=W['white'], old=True) + topknot(W['white'])
    elif pid == 'erlang':
        s = blade_three() + robe(W['gold'], W['red']) + person(hair_kind='short', show_ear=False) + three_peak_cap() + third_eye()
    elif pid == 'lijing':
        s = pagoda(84, 40) + robe(W['gold'], W['red']) + person(hair_kind='short', beard_kind='thin', show_ear=False) + helmet_cn()
    elif pid == 'nezha':
        s = robe(W['vermil'], W['gold'])
        s += fill("M16,94 C30,84 46,86 58,92 C66,96 76,94 86,86 C80,96 70,100 60,100 L20,100 Z", W['red'], 0.8)   # sash
        s += head() + ear() + eye() + face()
        s += fill("M34,44 C31,36 34,29 42,26 C50,24 56,26 58.4,30 C50,31 41,36 34,44 Z", INK)
        for (x, y) in [(38, 24), (52, 22)]:
            s += C_(x, y, 5.4, INK) + P(f"M{x-4},{y} C{x-2},{y-2} {x+2},{y-2} {x+4},{y}", 'none', W['red'], 1.2)
        s += ring(80, 70, 9, W['gold'])
    elif pid == 'change':
        s = crescent(80, 24, 13) + robe(W['white'], W['pink']) + person(hair_kind='bun') + high_bun() + ribbons()
    elif pid == 'zhenyuan':
        s = ginseng_fruit(84, 66) + robe(W['ochre'], W['white']) + person(hair_kind='short', beard_kind='thin') + dao_crown()
    elif pid == 'subodhi':
        s = ruler() + robe(W['grey'], W['white']) + person(hair_kind='short', hair_col=W['white'], beard_kind='long', beard_col=W['white'], old=True) + dao_crown(W['jade'])
    elif pid == 'aoguang':
        s = hu_tablet() + robe(W['blue'], W['gold']) + dragon_head(W['jade'])
        s += fill("M47,24 C47,19 50,16 54,16 C58,16 60,19 60,23 C56,25 51,25 47,24 Z", W['gold'], 0.8)
    elif pid == 'aorun':
        s = pearl(84, 70) + robe(W['white'], W['gold']) + dragon_head('#c9d6d0')
        s += fill("M47,24 C47,19 50,16 54,16 C58,16 60,19 60,23 C56,25 51,25 47,24 Z", W['gold'], 0.8)
    elif pid == 'taizong':
        s = robe(W['yellow'], W['red']) + person(hair_kind='short', beard_kind='thin') + futou()
        s += P("M22,92 C30,88 36,90 40,94 M56,96 C62,90 70,90 76,94", 'none', W['red'], 1.2)
    elif pid == 'cuilan':
        s = robe(W['pink'], W['white']) + person(hair_kind='bun') + flower(40, 30, W['red'], 2.6)
    elif pid == 'baihuaxiu':
        s = letter() + robe(W['jade'], W['gold']) + person(hair_kind='bun') + high_bun()
    elif pid == 'wujiking':
        s = robe(W['yellow'], W['red']) + person('#e8e6dc', hair_kind='short', beard_kind='short') + king_crown() + water_drops()
    elif pid == 'womanking':
        s = seal(84, 58) + robe(W['vermil'], W['gold']) + person(hair_kind='bun') + phoenix_crown()
    elif pid == 'bull':
        s = iron_club() + robe(W['dark'], W['gold']) + bull_head()
    elif pid == 'ironfan':
        s = banana_fan() + robe(W['vermil'], W['gold']) + person(hair_kind='bun') + high_bun()
    elif pid == 'redboy':
        s = flames_at(24, 70, 1.6) + fire_spear() + robe(W['red'], W['gold']) + head(SKIN) + ear() + eye() + face()
        for (x, y) in [(36, 30), (47, 24), (57.4, 26.8)]:
            s += P(f"M{x-3.6},{y+3} C{x-4.4},{y-2} {x-1},{y-5} {x+1.6},{y-4.4} C{x+1},{y-6.6} {x+3},{y-8} {x+4.6},{y-7} C{x+3.6},{y-5} {x+4.8},{y-1} {x+3.6},{y+3} Z", INK, INK, 0.6)
        s += fill("M52,62 C54,64 56,64 58,62", '#f2b7a8', 0.4)
    elif pid == 'jadeface':
        s = robe(W['pink'], W['white']) + person(W['white'], hair_kind='bun') + high_bun() + flower(56, 16, W['pink'], 2.6)
    elif pid == 'whitebone':
        s = robe(W['bone'], W['grey']) + skull_face()
    elif pid == 'yellowrobe':
        s = sword(72, 100, 88, 12) + robe(W['yellow'], W['red']) + person(W['blue'], hair_kind='short', hair_col='#b0452e', beard_kind='point', beard_col='#b0452e')
        s += fill("M62.6,57.4 L63.8,62 L61.4,57.8 Z", W['white'], 0.5)
    elif pid == 'goldhorn':
        s = sword(72, 100, 88, 10) + robe(W['ochre'], W['red']) + person('#e2c07a', hair_kind='short', beard_kind='short')
        s += fill("M54,30 C54,22 58,16 64,14 C62,20 61,26 60,31 Z", W['gold'], 0.9)
    elif pid == 'silverhorn':
        s = gourd(84, 70) + robe(W['blue'], W['white']) + person('#d9dcd2', hair_kind='short')
        s += fill("M54,30 C54,22 58,16 64,14 C62,20 61,26 60,31 Z", '#d8dbe0', 0.9)
    elif pid == 'blackbear':
        s = cassock(W['red'], W['gold']) + bear_head()
    elif pid == 'yellowwind':
        s = trident_cn() + robe(W['ochre'], W['white']) + marten_head() + wind_lines()
    elif pid == 'greenox':
        s = ring(84, 72, 9) + robe(W['dark'], W['gold']) + bull_head('#9fb0a6', horns=1, horn_col=W['bone'])
    elif pid == 'greenlion':
        s = robe(W['gold'], W['red']) + lion_head()
    elif pid == 'whiteelephant':
        s = robe(W['vermil'], W['gold']) + elephant_head()
    elif pid == 'roc':
        s = wings_back() + halberd() + robe(W['red'], W['gold']) + bird_head()
    elif pid == 'yellowbrow':
        s = cymbal(84, 60) + robe(W['ochre'], W['red']) + person(hair_kind=None, show_ear=True)
        s += P("M52.4,39.4 Q57.2,36.4 62,38.6", 'none', W['yellow'], 3.4) + ink("M52.4,39.4 Q57.2,36.4 62,38.6", 0.5)
        s += P("M52.4,40 C50,42 49,44 49.6,48", 'none', W['yellow'], 2)
    elif pid == 'saitaisui':
        s = bells() + robe(W['vermil'], W['gold']) + lion_head(W['gold'], W['yellow'], long_snout=True)
    elif pid == 'goldfish':
        s = lotus_mace() + robe(W['blue'], W['gold']) + fish_head()
    elif pid == 'jaderabbit':
        s = pestle() + robe(W['pink'], W['gold']) + rabbit_head()
    elif pid == 'mouse':
        s = twin_swords() + robe(W['jade'], W['pink']) + mouse_head()
    elif pid == 'spiders':
        s = web(78, 28, 22) + robe(W['purple'], W['white']) + person(hair_kind='bun') + high_bun(ornament=False)
        s += P("M50,88 C60,80 70,74 84,68", 'none', W['white'], 1.2) + ink("M50,88 C60,80 70,74 84,68", 0.3)
    elif pid == 'sixear':
        s = iron_staff() + robe(W['dark'], W['red']) + big(monkey(fur='#8f8a7c', ears=3), 1.2, 50, 50, -2, -5)
    elif pid == 'ninehead':
        s = nine_heads()
    elif pid == 'tuolong':
        s = whip() + robe(W['indigo'], W['gold']) + alligator_head()
    else:
        raise KeyError(pid)
    return s


def build(pid):
    bg = PAPER_D if pid in DEMON_GROUND else PAPER
    s = base(bg)
    if pid == 'rulai':
        s += mandorla(47, 44, 32)
    elif pid in GODS:
        s += halo(47, 42, 26)
    body = draw(pid)
    s += body if pid in ('horse', 'ninehead') else zoom(body)
    return s + frame()


def symbols(ids):
    out = []
    for pid in ids:
        out.append(f'<symbol id="pt-{pid}" viewBox="0 0 100 100">'
                   f'<clipPath id="pc-{pid}"><circle cx="50" cy="50" r="50"/></clipPath>'
                   f'<g clip-path="url(#pc-{pid})">{build(pid)}</g></symbol>')
    return '\n'.join(out)
