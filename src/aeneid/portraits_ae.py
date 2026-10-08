# -*- coding: utf-8 -*-
"""Aeneid portraits in the manner of Roman wall painting (Pompeian frescoes).
Same profile drawings as the Homer pages, repainted: flesh-toned faces and colored drapery
on fresco grounds, with a thin painted frame and, for gods, a pale nimbus.
  fg  gods      Pompeian red ground
  fm  mortals   Pompeian green ground
  fx  monsters  yellow-ochre ground, dark figure (like the black-figure monsters of the Odyssey)
  fs  ghosts    pale blue-grey ground, drawn in outline
"""
import os, sys, math, re
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(SRC, 'odyssey'))
sys.path.insert(0, os.path.join(SRC, 'iliad'))
import portraits as O  # noqa: E402
import portraits_il as I  # noqa: E402
from portraits import (P, C_, garment, head, eye, face_lines, ear, hair, beard, fillet, wreath, stephane, veil,  # noqa: E402
                       front_hair_under, attic_helmet, spear, scepter, bow, std_person, HAIR_LONG, small_female_head)
from portraits_il import (plain_veil, phrygian_cap, round_shield, staff, laurel_sprig, wings, dove, corinthian,  # noqa: E402
                          necklace_small, person, woman, zoom, earring)

PAL = {
    'fg': dict(bg='#9b3322', fig='#f1e5c8', ln='#2a1810', hair='#3d2416', hl='#8a5a3a', wh='#fbf4e4',
               acc='#e6b34c', skin='#e9b892', red='#6d1d14', obj='#c99a4a', frame='#e6b34c', nimbus='#f4d9a8'),
    'fm': dict(bg='#2d4a3f', fig='#dcc28c', ln='#21150e', hair='#3a2415', hl='#8b5d3b', wh='#f7efdc',
               acc='#e2ae45', skin='#d69b70', red='#8e2d1f', obj='#b88b4c', frame='#c9a45a'),
    'fx': dict(bg='#c99a3e', fig='#2a1d16', ln='#c99a3e', hair='#2a1d16', hl='#c99a3e', wh='#f4e7c6',
               acc='#7e2a1c', skin='#2a1d16', red='#7e2a1c', obj='#2a1d16', frame='#2a1d16'),
    'fs': dict(bg='#c3cccb', fig='#e7ebe7', ln='#4a585c', hair='#8e9c9e', hl='#4a585c', wh='#f6f8f5',
               acc='#a3b3b3', skin='#e7ebe7', red='#7f9093', obj='#6b7b7e', frame='#7f9093'),
}
FLAME, FLAME_IN = '#ef8a2c', '#f9d266'
LEAF = '#a7c46e'
PURPLE = '#7b355f'


# ------------------------------------------------------------------ new pieces
def penates(c, x=84, y=64):
    """A household god: a little bronze statuette carried out of Troy."""
    g = f'<g transform="translate({x} {y})">'
    g += P("M-7,27 L7,27 L8,31 L-8,31 Z", c['acc'], c['ln'], 0.5)
    g += P("M-4.6,27 L-3.4,7 C-3,3 3,3 3.4,7 L4.6,27 Z", c['acc'], c['ln'], 0.6)
    g += P("M-3.4,11 C-6,14 -7,18 -6.4,21 M3.4,11 C6,13 7.4,15 8,17", 'none', c['acc'], 1.4)
    g += C_(8.4, 16.4, 1.8, c['acc'], c['ln'], 0.4)
    g += C_(0, 0.6, 3.6, c['acc'], c['ln'], 0.6)
    g += P("M-1,9 L0,24 M1.6,9 L2,24", 'none', c['ln'], 0.4)
    g += '</g>'
    return g


def flint(c):
    s = P("M72,94 L76,82 L86,80 L92,88 L88,98 L76,99 Z", '#8d877c', c['ln'], 0.7)
    s += P("M84,78 L88,68 L96,67 L99,75 L94,82 Z", '#a39c8e', c['ln'], 0.7)
    for (a, l) in [(-100, 9), (-70, 12), (-40, 10), (-125, 8), (-15, 7)]:
        r = math.radians(a)
        x1, y1 = 86 + 3 * math.cos(r), 72 + 3 * math.sin(r)
        x2, y2 = 86 + l * math.cos(r) * 1.4, 72 + l * math.sin(r) * 1.4
        s += P(f"M{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f}", 'none', FLAME_IN, 1.1)
    s += C_(86, 72, 1.6, FLAME_IN)
    return s


def oar(c):
    """A steering oar held upright, and a star: Palinurus reads the sky before setting sail (Book 3)."""
    s = P("M86,0 L80.6,50", 'none', c['obj'], 2.4)
    s += P("M85,10 L95,12.4", 'none', c['obj'], 2)
    s += P("M80.8,44 C86.6,50 88.6,64 86.6,84 L74.4,84 C73.4,67 75.4,54 80.8,44 Z", c['obj'], c['ln'], 0.7)
    s += P("M80.6,50 L80.2,83", 'none', c['ln'], 0.5)
    for (x, y, r) in [(73, 16, 2.6), (64, 10, 1.6)]:
        s += P(f"M{x},{y-r} L{x+r*0.28},{y-r*0.28} L{x+r},{y} L{x+r*0.28},{y+r*0.28} L{x},{y+r} "
               f"L{x-r*0.28},{y+r*0.28} L{x-r},{y} L{x-r*0.28},{y-r*0.28} Z", c['wh'])
    return s


def snake(c, d, hx, hy, ang, col=None, crest=True, w=4.6):
    col = col or c['acc']
    s = P(d, 'none', c['ln'], w + 1.4) + P(d, 'none', col, w)
    s += P(d, 'none', c['ln'], 0.4, ' stroke-dasharray="1.2 2.6" opacity=".6"')
    g = f'<g transform="translate({hx} {hy}) rotate({ang})">'
    g += P("M-3,-3 C1,-4.6 6,-3.6 8.4,-0.6 C8.8,0.4 8.2,1.4 7,1.8 L-3,3.4 Z", col, c['ln'], 0.6)
    g += C_(3.4, -1.4, 0.8, c['red'])
    g += P("M8.2,0.8 L11.6,1.6 M11.6,1.6 L13.2,0.4 M11.6,1.6 L13,3", 'none', c['red'], 0.6)
    if crest:
        g += P("M-2,-3.4 L-0.6,-6.6 L1.4,-3.8 L3,-6.4 L4.4,-3.6", c['red'], c['ln'], 0.4)
    g += '</g>'
    return s + g


def serpents(c):
    s = snake(c, "M4,92 C14,78 30,98 42,88 C54,78 60,96 72,90 C82,85 84,74 78,66", 78, 66, -95)
    s += snake(c, "M98,98 C88,90 80,100 70,96 C62,93 64,82 72,78 C80,74 90,70 92,58 C93,50 90,44 84,42", 84, 42, 200)
    return s


def horse_head(c):
    col = c['obj']
    s = P("M70,100 C70,86 73,72 77,60 C79,52 82,46 85,42 L83.6,33 L88.4,38.6 L90.8,32 L92.4,40.4 "
          "C96.6,44.6 99.4,51 100.6,57 C101.2,61 99.4,64 96.6,64 C93.4,64 90.6,61.4 88,59.4 "
          "C86.6,68 88.4,82 94,100 Z", col, c['ln'], 0.8)
    s += P("M73,68 L88,70.4 M71.6,80 L89.4,82 M71,91 L91.6,93", 'none', c['ln'], 0.6)
    s += P("M85,42 C80,48 76,56 74.6,64", 'none', c['ln'], 0.5)
    s += C_(91, 45.6, 1.1, c['ln'])
    s += P("M96,59.6 L99,60.2", 'none', c['ln'], 0.6)
    for (x, y) in [(84, 44), (81, 50), (78.6, 56)]:
        s += P(f"M{x},{y} L{x-3.6},{y+1.2}", 'none', c['ln'], 1.1)
    return s


def palm(c):
    col = c['acc']
    s = P("M72,100 C76,80 80,56 90,24", 'none', col, 1.6)
    for i in range(10):
        t = i / 9
        x = 72 + (90 - 72) * t + 3 * math.sin(t * math.pi)
        y = 100 - 76 * t
        l = 13 - 6 * t
        s += P(f"M{x:.1f},{y:.1f} C{x-l*0.5:.1f},{y-2:.1f} {x-l*0.9:.1f},{y+1:.1f} {x-l:.1f},{y+4:.1f}", 'none', col, 1.2)
        s += P(f"M{x:.1f},{y:.1f} C{x+l*0.5:.1f},{y-3:.1f} {x+l*0.9:.1f},{y-1:.1f} {x+l:.1f},{y+2:.1f}", 'none', col, 1.2)
    return s


def golden_bough(c):
    col = c['acc']
    s = P("M70,98 C74,84 80,66 90,40", 'none', c['obj'], 1.6)
    s += P("M78,72 C84,70 90,66 94,60", 'none', c['obj'], 1.1)
    for (x, y, a) in [(72.6, 90, -30), (75, 82, 40), (77.6, 74, -35), (80.6, 66, 35), (84, 57, -30), (87, 49, 35),
                      (89.6, 41, -20), (86, 70, 60), (91, 64, -10), (94.4, 58.6, 40)]:
        s += (f'<ellipse cx="{x}" cy="{y}" rx="4.2" ry="1.9" transform="rotate({a} {x} {y})" '
              f'fill="{col}" stroke="{c["ln"]}" stroke-width="0.45"/>')
    s += P("M85,52 L86.4,51 M79,69 L80.4,68.4", 'none', c['wh'], 0.8)
    return s


def baldric(c):
    s = P("M20,84 C34,82.4 52,88 66,100 L58,100 C46,91 32,87.4 18,88.8 Z", c['acc'], c['ln'], 0.6)
    for i in range(5):
        t = (i + 0.5) / 5
        x = 20 + 42 * t
        y = 86.4 + 9 * t * t + 1
        s += C_(round(x, 1), round(y, 1), 0.9, c['ln'])
    return s


def chimaera_crest(c):
    s = ''
    for (d, w) in [("M50,21 C44,8 30,4 18,12", 2.6), ("M48,22 C40,13 28,12 17,20", 2.4), ("M46,23 C38,18 28,19 19,27", 2.2)]:
        s += P(d, 'none', c['ln'], w + 1.2) + P(d, 'none', c['red'], w)
    # the Chimaera: a small lion head on the crown of the helmet, breathing fire
    s += P("M47,21 C47,15 50,11 55,10.4 C58.6,10 61.4,11.4 63,14 L66.4,15.6 C66.6,17 65.8,18 64.4,18.2 "
           "L60.6,18.6 C58,20 55,21.4 52,22 Z", c['acc'], c['ln'], 0.6)
    s += P("M49,13.6 C47,11.6 47.4,9 49.6,8.4 C50,10.4 51,11.6 52.6,12.4", c['acc'], c['ln'], 0.5)
    s += C_(59, 13.4, 0.7, c['ln'])
    s += P("M66,16 C70,13 74,14 78,11 C76,15.4 73,17 70,17.2 C73,18.4 76,18 79,19.6 C75,21.4 70,20.6 66.4,18.2 Z",
           FLAME, c['ln'], 0.4)
    s += P("M67.6,16.4 C70.6,15.6 72.6,15.8 74.6,15", 'none', FLAME_IN, 0.9)
    return s


def radiate(c):
    s = ''
    cx, cy = 45, 44
    for i in range(7):
        t = i / 6
        x = 57 - t * 22.6
        y = 30.2 + t * 12.6
        dx, dy = x - cx, y - cy
        n = math.hypot(dx, dy)
        ux, uy = dx / n, dy / n
        px, py = -uy, ux
        tipx, tipy = x + ux * 10.5, y + uy * 10.5
        s += P(f"M{x+px*1.9:.1f},{y+py*1.9:.1f} L{tipx:.1f},{tipy:.1f} L{x-px*1.9:.1f},{y-py*1.9:.1f} Z", c['acc'], c['ln'], 0.45)
    s += P("M58.2,30 C50,32.4 41.4,36.6 32.6,43.8", 'none', c['ln'], 3.2) + P("M58.2,30 C50,32.4 41.4,36.6 32.6,43.8", 'none', c['acc'], 2.2)
    return s


def ivy(c):
    s = P("M57.6,30.2 C50,32.8 41.5,36.8 32.8,43.6", 'none', '#5d7a38', 1)
    for i in range(6):
        t = i / 5
        x = 56 - t * 21.4
        y = 30.6 + t * 11.4
        for side in (-1, 1):
            lx, ly = x + side * 0.6, y + side * 2.6 - 0.6
            s += (f'<path d="M{lx:.1f},{ly+2.2:.1f} C{lx-3:.1f},{ly:.1f} {lx-2.4:.1f},{ly-2.8:.1f} {lx:.1f},{ly-1.4:.1f} '
                  f'C{lx+2.4:.1f},{ly-2.8:.1f} {lx+3:.1f},{ly:.1f} {lx:.1f},{ly+2.2:.1f} Z" fill="{LEAF}" stroke="{c["ln"]}" stroke-width="0.35"/>')
    for (x, y) in [(52, 28.4), (44, 32.4), (37, 37.6)]:
        s += C_(x, y, 1.1, '#3b3042', c['ln'], 0.3)
    return s


def thyrsus(c):
    s = P("M74,100 L86,18", 'none', c['obj'], 2)
    s += f'<ellipse cx="86.8" cy="12" rx="4.2" ry="6.6" fill="{c["acc"]}" stroke="{c["ln"]}" stroke-width="0.6"/>'
    s += P("M83.4,9 L89.6,15 M83,13 L88.6,18 M84.6,6.4 L90.4,11.6 M89.8,8.6 L83.6,14.6 M90.4,12.8 L84.6,18", 'none', c['ln'], 0.4)
    s += P("M85.6,20 C80,24 82,30 77,34 M86.4,21 C90,26 88,31 92,36", 'none', LEAF, 1.1)
    return s


def hair_flames(c):
    s = ''
    for (x, y, h, w, lean) in [(31, 42, 11, 3, -2), (29.6, 52, 12, 3.2, -3), (31, 62, 11, 3, -3), (33.6, 72, 10, 2.8, -2),
                               (37, 30, 12, 3.2, -1), (44, 25.6, 13, 3.4, 0), (51, 25, 10, 2.8, 1)]:
        s += P(f"M{x-w},{y} C{x-w},{y-h*0.5} {x+lean-0.6},{y-h*0.6} {x+lean},{y-h} "
               f"C{x+lean+0.6},{y-h*0.6} {x+w},{y-h*0.5} {x+w},{y} Z", FLAME, c['ln'], 0.45)
        s += P(f"M{x},{y-1} C{x},{y-h*0.35} {x+lean*0.6},{y-h*0.5} {x+lean*0.6},{y-h*0.62}", 'none', FLAME_IN, 1)
    return s


def quiver(c):
    s = P("M12,88 L23,38 L30.6,40 L20,90 Z", c['red'], c['ln'], 0.7)
    s += P("M14.6,76 L22.4,78 M18.6,58 L26.4,60", 'none', c['acc'], 1.2)
    for (x, y) in [(24.2, 37.4), (27.4, 38.2), (30.4, 39)]:
        s += P(f"M{x},{y} L{x+0.8},{y-9}", 'none', c['obj'], 0.9)
        s += P(f"M{x+0.8},{y-9} L{x-1.2},{y-5.6} M{x+0.8},{y-9} L{x+2.6},{y-5.4}", 'none', c['wh'], 0.9)
    return s


def winds(c):
    s = ''
    for (x, y, sc, flip) in [(78, 22, 1.0, 1), (86, 44, 0.8, 1), (18, 26, 0.9, -1), (80, 70, 0.7, 1)]:
        g = f'<g transform="translate({x} {y}) scale({sc * flip} {sc})">'
        g += P("M-12,4 C-6,4 2,3 6,-1 C9,-4 7,-9 3,-8 C0,-7.4 0,-3.6 3,-3.4", 'none', c['wh'], 1.4)
        g += P("M-14,9 C-6,9 4,8.6 10,6", 'none', c['wh'], 1.0)
        g += '</g>'
        s += g
    return s


def hydria(c):
    col = '#c47a4c'
    s = P("M73,70 C69,74 68,82 71,88 C74,94 80,96 86,96 C92,96 97,92 98,86 C99,80 96,74 92,70 Z", col, c['ln'], 0.7)
    s += P("M78,70 L78,64 L87,64 L87,70 Z", col, c['ln'], 0.6)
    s += P("M76,62.6 L89,62.6", 'none', c['ln'], 1.6)
    s += P("M72,78 C66,76 66,70 71,69.6 M97,78 C102,76 101,70 96,69.8", 'none', col, 1.6)
    s += P("M72,82 C80,85 90,85 98,82", 'none', c['ln'], 0.6)
    for (x0, y0) in [(74, 96), (80, 97), (86, 97)]:
        s += P(f"M{x0},{y0} c1,2 -1,3 0,5", 'none', '#9cc6d6', 1.3)
    return s


def thorns(c):
    s = ''
    for (x, y) in [(24, 90), (34, 84), (46, 90), (62, 86), (76, 92), (54, 96), (30, 97)]:
        s += P(f"M{x-2},{y} L{x+2},{y} M{x},{y-1.6} L{x+1.4},{y-3} M{x-1},{y+0.6} L{x-2.4},{y+2}", 'none', c['ln'], 0.6)
    s += P("M26,84 L22,90 L28,92 M58,80 L54,86 L60,88 M70,86 L66,94", 'none', c['ln'], 0.7)
    return s


def torch(c):
    s = P("M72,100 L84,38", 'none', c['obj'], 2.6)
    s += P("M81.6,44 L87.2,45.4", 'none', c['obj'], 1.8)
    s += P("M78,40 C76,32 80,26 82,18 C84,24 86,22 86,14 C90,20 93,28 90,36 C89,40 86,42 83,42 C80.6,42 78.6,41.4 78,40 Z",
           FLAME, c['wh'], 0.4)
    s += P("M81,38 C80,33 83,30 84,25 C86,30 88,32 86.6,38 Z", FLAME_IN)
    s += P("M84,14 C86,8 90,6 92,2 M88,20 C92,16 94,14 98,13", 'none', c['wh'], 0.7, ' opacity=".6"')
    return s


def snake_hair(c):
    col = '#5d6b3a'
    s = ''
    for (d, hx, hy, a) in [("M44,26 C42,18 48,12 44,6", 44, 6, -80), ("M36,31 C30,24 30,16 24,12", 24, 12, -140),
                           ("M32,42 C24,40 20,34 12,34", 12, 34, 180), ("M32,54 C24,56 20,62 12,62", 12, 62, 170),
                           ("M52,25 C54,18 60,16 62,10", 62, 10, -50)]:
        s += snake(c, d, hx, hy, a, col=col, crest=False, w=3)
    return s


def harpy(C):
    s = ''
    s += P("M36,66 C26,66 16,70 8,78 C16,77 22,76.6 28,77 C20,80 14,85 10,91 C20,87 30,82 38,76 Z", C['fig'], C['ln'], 0.6)
    s += P("M34,70 C34,58 44,50 56,50 C66,50 74,56 76,64 C78,74 72,84 60,86 C48,88 36,82 34,70 Z", C['fig'], C['ln'], 0.6)
    s += P("M40,62 C48,52 62,50 74,56 C66,60 62,66 58,72 C52,70 46,68 40,62 Z", C['red'], C['ln'], 0.6)
    for d in ["M44,64 C50,62 56,64 60,68", "M46,67 C52,66 56,68 58,71", "M40,70 C46,72 52,74 56,78", "M36,74 C44,78 52,80 58,82"]:
        s += P(d, 'none', C['ln'], 0.6)
    # raised wing
    s += P("M56,52 C62,40 72,30 90,24 C86,30 84,34 84,38 C88,36 92,36 96,36 C90,42 84,48 76,56 Z", C['fig'], C['ln'], 0.6)
    for d in ["M62,48 C70,40 78,34 88,28", "M66,52 C74,46 82,42 92,38"]:
        s += P(d, 'none', C['ln'], 0.6)
    # legs and hooked talons
    s += P("M52,86 L50,93 M60,86 L62,93", 'none', C['fig'], 1.9)
    s += P("M45,96 C46.6,93.4 49,93 50.4,93.4 C51.6,94 52.4,95.6 52.6,97.4 M58.6,96.4 C59.6,93.4 62,93 63.6,93.6 "
           "C65,94.2 66,95.6 66.4,97.6 M50.4,93.4 L48.6,97.6 M62.4,93.2 L61,97.8", 'none', C['fig'], 1.1)
    s += P("M40,99 L74,99", 'none', C['fig'], 1.2)
    s += P("M62,52 C62,46 63.4,42 65,38 L72,40 C71,45 71,49 72.6,55 Z", C['wh'], '#1f1612', 0.8)
    s += small_female_head(C, 66, 30, 0.56)
    return s


def polyphemus_blind(C):
    """The Odyssey's Cyclops, after Ulysses: the single eye is a wound."""
    g = '<g transform="translate(50 52) scale(1.14) translate(-48 -50)">'
    g += garment(C, folds=False) + head(C)
    g += P("M57.4,29.2 C56,32.6 53.6,35.2 50.6,36.8 C48.6,39.6 48,43 47.6,46 L47,50 C44.4,53 42,57.5 40.5,63.5 "
           "L38.8,66.2 C32,62 27,54 26,45 C25,38 27,30 33,25 C38,21 45,20 52,22 C55,23 56.8,26 57.4,29.2 Z",
           C['hair'], C['hl'], 0.6)
    for d in ["M30,30 L27,28 M29,38 L25.6,37.6 M29,46 L25.6,47 M31,54 L27.6,56 M37,24 L35.6,20.6 M45,22 L45,18.4"]:
        g += P(d, 'none', C['hair'], 1.6)
    g += beard(C, 'long', color=C['red']) + ear(C) + face_lines(C)
    g += P("M53.2,32.6 Q58.6,29.6 63.6,33", 'none', C['ln'], 1.0)
    g += P("M54.6,35.8 Q58.8,33.6 62.8,35.4 Q58.8,38.4 54.6,35.8 Z", C['red'], C['ln'], 0.6)
    g += P("M55.6,35.8 Q58.8,35 62,35.6", 'none', C['ln'], 0.7)
    for (x0, y0, l) in [(57, 37.8, 7), (59.8, 38, 5)]:
        g += P(f"M{x0},{y0} C{x0-0.4},{y0+l*0.4} {x0+0.4},{y0+l*0.7} {x0},{y0+l}", 'none', C['red'], 1.1)
    g += '</g>'
    # the pine trunk he leans on
    g += P("M76,100 L90,6", 'none', C['fig'], 4.2)
    g += P("M84.6,40 L78,34 M87,24 L94,20 M81.4,62 L88,58", 'none', C['fig'], 1.6)
    return g


def cupid(c):
    s = wings(c)
    s += garment(dict(c, fig=c['skin']), folds=False)
    s += head(c) + hair(c, 'short') + ear(c) + eye(c) + face_lines(c)
    s += P("M20,86 C34,82 50,84 62,92", 'none', c['red'], 1.8)                     # quiver strap
    s += P("M84,26 C92,36 80,48 84.4,60 C80,72 90,82 84,92", 'none', c['obj'], 2.2)  # small bow
    s += P("M84,26 L84,92", 'none', c['obj'], 0.5)
    return s


def bird(c, x, y, sc=1.0, col=None):
    cc = dict(c, fig=col or c['wh'])
    return dove(cc, x, y, sc)


def gleam(c, pts):
    s = ''
    for (x, y) in pts:
        s += P(f"M{x-2.4},{y} L{x+2.4},{y} M{x},{y-2.4} L{x},{y+2.4}", 'none', c['wh'], 0.7)
    return s


# ------------------------------------------------------------------ characters
REUSE = {  # Aeneid id -> (module, id there)
    'jupiter': (O, 'zeus'), 'neptune': (O, 'poseidon'), 'mercury': (O, 'hermes'), 'minerva': (O, 'athena'),
    'ulysses': (O, 'odysseus'),
    'juno': (I, 'hera'), 'venus': (I, 'aphrodite'), 'vulcan': (I, 'hephaestus'), 'apollo': (I, 'apollo'),
    'helen': (I, 'helen'), 'andromache': (I, 'andromache'), 'hector': (I, 'hector'),
}


def draw(pid, c):
    """Portrait body (no background) in palette c."""
    if pid in REUSE:
        mod, oid = REUSE[pid]
        m = mod.build(oid, c)
        return re.sub(r'^<rect[^>]*/>', '', m)
    s = ''
    if pid == 'aeneas':
        s = person(c, 'short', 'short', show_ear=False) + attic_helmet(c, crest=True)
        s += round_shield(dict(c, fig=c['acc']), 81, 59, 12.2)
    elif pid == 'anchises':
        s = person(c, 'long', 'long', old=True, hair_col=c['wh'], beard_col=c['wh'], himation=True) + phrygian_cap(dict(c, fig='#b5624a'))
        s += f'<g transform="translate(82 62) scale(1.35) translate(-82 -62)">{penates(c, 81, 58)}</g>'
    elif pid == 'creusa':
        cc = dict(c, fig='#a9b7c0')
        s = garment(cc) + head(c) + front_hair_under(c) + veil(cc) + eye(c) + face_lines(c)
    elif pid == 'ascanius':
        s = bow(dict(c, fig=c['obj'])) + person(c, 'short', show_ear=False) + phrygian_cap(dict(c, fig='#b5624a'))
        s += ''.join(P(f"M{x-w},{y} C{x-w},{y-h*0.5} {x-0.4},{y-h*0.6} {x},{y-h} C{x+0.6},{y-h*0.6} {x+w},{y-h*0.5} {x+w},{y} Z",
                       FLAME, c['ln'], 0.45) for (x, y, h, w) in [(52, 16, 12, 3), (57, 14.4, 10, 2.6), (46.4, 19, 9, 2.6)])
    elif pid == 'achates':
        s = person(c, 'short', 'short') + fillet(c, c['red'], 1.8)
        s += f'<g transform="translate(-9 -19)">{flint(c)}</g>'
    elif pid == 'palinurus':
        s = oar(c) + person(c, 'short', 'short', himation=True) + fillet(c, c['wh'], 1.6)
    elif pid == 'priam':
        s = spear(c, 70, 100, 84, 6) + person(c, 'long', 'long', old=True, hair_col=c['wh'], beard_col=c['wh']) + stephane(c, c['acc'])
    elif pid == 'laocoon':
        s = person(c, 'long', 'short', himation=True) + wreath(c, LEAF) + serpents(c)
    elif pid == 'sinon':
        s = f'<g transform="translate(-7 2) translate(86 60) scale(0.9) translate(-86 -60)">{horse_head(c)}</g>' + person(c, 'short', 'point')
    elif pid == 'pyrrhus':
        s = spear(c, 70, 100, 84, 4) + person(c, 'short', show_ear=False) + corinthian(dict(c, fig=c['acc']), crest=True)
        s += gleam(c, [(44, 28), (60, 30)])
    elif pid == 'helenus':
        s = laurel_sprig(dict(c, fig=LEAF)) + person(c, 'long', 'short', himation=True) + phrygian_cap(dict(c, fig='#b5624a'))
    elif pid == 'dido':
        cp = dict(c, fig=PURPLE)
        s = palm(c) + garment(cp) + head(c) + front_hair_under(c) + veil(c) + stephane(c, c['acc'], points=True) + eye(c) + face_lines(c)
        s += earring(c, 47.4, 55.6)
    elif pid == 'anna':
        cc = dict(c, fig='#9fb2c4')
        s = garment(cc) + head(c) + hair(c, 'bun') + ear(c) + eye(c) + face_lines(c) + fillet(c, c['red'], 1.6) + necklace_small(c)
    elif pid == 'sychaeus':
        s = person(c, 'short', 'short', himation=True) + fillet(c, c['obj'], 1.4)
        s += P("M40,88 L47,84 M43.6,90.6 L48.8,86", 'none', c['red'], 1.3)
    elif pid == 'sibyl':
        cc = dict(c, fig='#cfc6b4')
        s = golden_bough(c) + garment(cc) + head(c) + front_hair_under(dict(c, hair=c['wh'])) + veil(cc) + eye(c) + face_lines(c, old=True)
    elif pid == 'achaemenides':
        cc = dict(c, fig='#a7916a')
        s = person(cc, 'long', 'long') + thorns(c)
        s += P("M52,24 L50,19 M46,25 L42,21 M40,28 L35,25 M35,34 L30,32", 'none', c['hair'], 1.5)
    elif pid == 'evander':
        s = staff(c) + person(c, 'short', 'long', old=True, hair_col=c['wh'], beard_col=c['wh'], himation=True) + fillet(c, c['acc'], 1.6)
    elif pid == 'pallas':
        s = spear(c, 70, 100, 84, 4) + person(c, 'short') + fillet(c, c['acc'], 1.6) + baldric(c)
    elif pid == 'nisus':
        s = spear(c, 70, 100, 84, 4) + person(c, 'short', 'short') + fillet(c, c['red'], 1.8)
    elif pid == 'euryalus':
        s = person(c, 'short', show_ear=False) + attic_helmet(dict(c, fig=c['acc']), crest=True) + gleam(c, [(40, 30), (56, 26), (64, 36)])
    elif pid == 'turnus':
        s = spear(c, 70, 100, 84, 4) + person(c, 'short', 'short', show_ear=False) + attic_helmet(c, crest=False) + chimaera_crest(c) + baldric(c)
    elif pid == 'latinus':
        s = scepter(c, 76, 100, 84, 12) + person(c, 'long', 'long', old=True, hair_col=c['wh'], beard_col=c['wh'], himation=True) + radiate(c)
    elif pid == 'amata':
        cc = dict(c, fig='#c9a2b4')
        s = thyrsus(c) + garment(cc) + head(c) + hair(c, 'long') + ear(c) + eye(c) + face_lines(c) + ivy(c)
    elif pid == 'lavinia':
        s = garment(c) + head(c) + hair(c, 'long', color='#8a5a2a') + ear(c) + eye(c) + face_lines(c) + hair_flames(c) + fillet(c, c['acc'], 1.4)
    elif pid == 'camilla':
        s = quiver(c) + bow(dict(c, fig=c['obj'])) + garment(dict(c, fig=PURPLE)) + head(c) + hair(c, 'bun') + ear(c) + eye(c) + face_lines(c)
        s += C_(38, 36, 2.2, c['acc'], c['ln'], 0.5)
    elif pid == 'mezentius':
        s = spear(c, 70, 100, 84, 4) + person(c, 'short', 'point', show_ear=False) + attic_helmet(dict(c, fig='#8e7a5e'), crest=True)
        s += P("M53.4,39.4 L61.4,41.8", 'none', c['ln'], 1.2)
    elif pid == 'lausus':
        s = person(c, 'short') + fillet(c, c['acc'], 1.4) + round_shield(dict(c, fig='#a88d5c'), 81, 61, 11.4)
    elif pid == 'diomedes':
        s = person(c, 'short', 'short', old=True, hair_col='#b9a58a', beard_col='#b9a58a') + stephane(c, c['acc'], points=True)
        s += bird(c, 84, 66, 1.15) + bird(c, 88, 36, 0.75)
    elif pid == 'cupid':
        s = cupid(c)
    elif pid == 'aeolus':
        s = scepter(c, 78, 100, 86, 12) + person(c, 'long', 'long') + fillet(c, '#9fb2c4', 1.8) + winds(c)
    elif pid == 'juturna':
        cc = dict(c, fig='#9fc0c4')
        s = garment(cc) + head(c) + front_hair_under(c) + plain_veil(cc) + eye(c) + face_lines(c)
        s += f'<g transform="translate(80 66) scale(0.75) translate(-85 -82)">{hydria(c)}</g>'
    elif pid == 'allecto':
        s = torch(c) + garment(c) + head(c) + hair(c, 'short', curls=False) + snake_hair(c) + ear(c) + eye(dict(c, ln=c['wh'])) + face_lines(c)
        return s
    elif pid == 'celaeno':
        return harpy(c)
    elif pid == 'polyphemus':
        return polyphemus_blind(c)
    else:
        raise KeyError(pid)
    return zoom(s)


def build(pid, style):
    c = PAL[style]
    s = f'<rect width="100" height="100" fill="{c["bg"]}"/>'
    if style == 'fg':
        s += f'<circle cx="47" cy="42" r="27" fill="{c["nimbus"]}" opacity=".28"/>'
    s += draw(pid, c)
    s += f'<circle cx="50" cy="50" r="46.6" fill="none" stroke="{c["frame"]}" stroke-width="0.9" opacity=".55"/>'
    return s


def symbols(ids_styles):
    out = []
    for pid, style in ids_styles:
        out.append(f'<symbol id="pt-{pid}" viewBox="0 0 100 100">'
                   f'<clipPath id="pc-{pid}"><circle cx="50" cy="50" r="50"/></clipPath>'
                   f'<g clip-path="url(#pc-{pid})">{build(pid, style)}</g></symbol>')
    return '\n'.join(out)
