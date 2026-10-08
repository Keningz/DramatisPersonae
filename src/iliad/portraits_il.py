# -*- coding: utf-8 -*-
"""Iliad portraits: red-figure style, reusing the Odyssey building blocks."""
import sys, math
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'odyssey'))
import portraits as O
from portraits import (P, C_, PAL, garment, head, eye, face_lines, ear, hair, beard, fillet, wreath,
                       stephane, veil, front_hair_under, petasos, attic_helmet, spear, scepter, trident,
                       thunderbolt, caduceus, owl, bow, pilos, std_person, sakkos)

C = PAL['red']


def zoom(s):
    return f'<g transform="translate(48 50) scale(1.1) translate(-48 -50)">{s}</g>'


# ------------------------------------------------------------------ new pieces
def polos(c):
    s = P("M37.6,31.6 L38.4,15.6 C45,13.6 52,13.2 58.6,14.4 L59.4,29.4 C52,29.2 44.6,29.8 37.6,31.6 Z", c['fig'], c['ln'], 0.8)
    s += P("M38.2,20.4 C45,18.6 52,18.2 58.8,19.2 M38,26 C45,24.4 52,24 59.2,25", 'none', c['ln'], 0.6)
    for x in (41.5, 45.5, 49.5, 53.5, 57):
        s += P(f"M{x},20.6 L{x+0.8},24.6", 'none', c['ln'], 0.5)
    return s


def plain_veil(c):
    """Veil falling behind the head from under a crown."""
    d = ("M40,26 C32,28 27.6,36 27.4,46 C27.2,56 30,64 28,74 C26.6,81 22,89 17,100 L44,100 "
         "C40.6,93 39.4,86 40.4,79.4 C41.2,73.8 40.4,69.4 38.8,66.2 C34.6,60 34,52 35.6,44 C36.8,37.6 39,31 40,26 Z")
    s = P(d, c['fig'], c['ln'], 0.8)
    s += P("M31.6,36 C30,46 30.8,58 32.6,66 M36,48 C35.2,58 36,66 37.4,72", 'none', c['ln'], 0.55)
    return s


def hammer_tongs(c):
    s = P("M70,98 L88,40", 'none', c['obj'], 2.2)
    s += P("M82.4,33.6 L96,38 L93.4,46.2 L79.8,41.8 Z", c['fig'], c['ln'], 0.6)
    s += P("M64,70 C70,60 76,55 84,52 M66,74 C72,66 78,60 86,57", 'none', c['obj'], 1.3)
    s += P("M84,52 L88,50.4 M86,57 L90,56", 'none', c['obj'], 1.6)
    return s


def work_cap(c):
    s = P("M31.4,43.4 C29.6,32.6 36.4,22.4 47.6,21.2 C55.6,20.6 60.8,24.8 61.4,31 C52,33.6 40.8,38.4 31.4,43.4 Z",
          c['fig'], c['ln'], 0.8)
    s += P("M32.2,40 C41,36.4 51,32.8 60.8,29", 'none', c['ln'], 1.1)
    return s


def dolphin(c, x=80, y=76, sc=1.0):
    g = f'<g transform="translate({x} {y}) scale({sc})">'
    g += P("M-15,4 C-10,-6 2,-9 10,-4 C13,-2 15,1 17,1.6 C15,2.6 12.6,3 10.6,3.4 C6,8 -4,9 -11,7 "
           "L-14,11 L-15,6.4 L-20,6 Z", c['fig'], c['ln'], 0.6)
    g += P("M-2,-7.4 L-5,-12.4 L2,-8 Z", c['fig'], c['ln'], 0.5)
    g += P("M1,4 L-2,9 L4,5.4 Z", c['fig'], c['ln'], 0.5)
    g += C_(9.4, -1.4, 0.8, c['ln'])
    g += P("M11,2.4 L16,1.8", 'none', c['ln'], 0.5)
    g += '</g>'
    return g


def dove(c, x=82, y=70, sc=1.0):
    g = f'<g transform="translate({x} {y}) scale({sc})">'
    g += P("M-12,4 C-8,-2 -2,-4 4,-3 C6,-6 9,-7.4 11.6,-6 L14,-5 L11.6,-4 C11.8,0 9,4 4,6 C-2,8 -8,7 -12,4 Z",
           c['fig'], c['ln'], 0.6)
    g += P("M-6,0 C-2,-4 4,-4 7,-1 C3,0 -1,2 -4,4 Z", c['fig'], c['ln'], 0.5)
    g += P("M-12,4 L-17,1 L-16,6 Z", c['fig'], c['ln'], 0.5)
    g += C_(9.6, -5, 0.7, c['ln'])
    g += '</g>'
    return g


def lyre(c):
    s = P("M72,94 C66,90 66,80 72,76 C78,72 88,72 94,76 C100,80 100,90 94,94 C88,98 78,98 72,94 Z",
          c['fig'], c['ln'], 0.7)
    s += P("M70,82 C74,84 90,84 96,82 M72,88 C78,90 88,90 94,88", 'none', c['ln'], 0.5)
    s += P("M74,78 C70,66 70,52 76,40 C77,38 79,38 79,40 M92,78 C96,66 96,52 90,40 C89,38 87,38 87,40",
           'none', c['fig'], 1.8)
    s += P("M74.4,44 L91.6,44", 'none', c['fig'], 1.8)
    for x in (78, 81, 84, 87):
        s += P(f"M{x},44.6 L{x},84", 'none', c['fig'], 0.45)
    return s


def corinthian(c, crest=False, tall=False):
    s = ''
    if crest:
        if tall:
            s += P("M47,18 L46,10", 'none', c['ln'], 2.4) + P("M47,18 L46,10", 'none', c['fig'], 1.2)
            s += P("M60,8 C56,-2 40,-4 30,2 C22,7 16,16 14,30 C13,36 13.6,42 15,46 L19,45 "
                   "C18.4,38 19,30 22,23 C26,14 34,9 43,9 C50,9 56,11 58.4,14 Z", c['hair'], c['hl'], 0.9)
            for i in range(9):
                a = i / 8
                x1 = 56 - a * 38; y1 = 6 + a * 34 - 10 * math.sin(a * math.pi)
                x2 = 52 - a * 32; y2 = 11 + a * 32 - 7 * math.sin(a * math.pi)
                s += P(f"M{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f}", 'none', c['hl'], 0.45)
        else:
            s += P("M56,20 C54,12 44,9 36,12 C30,15 27,20 26,26 L30,28 C31,22 34,18 38,16.6 C44,14.6 50,16 52.6,21 Z",
                   c['fig'], c['ln'], 0.7)
    # bowl pushed up on the head, face guard projecting forward
    s += P("M30.6,45.4 C28.8,33 36.4,22.4 47.6,21.2 C55.4,20.4 60.4,23.4 62.4,28 C65.6,29.6 68.2,32.4 68.6,35.6 "
           "C66,37.4 62.6,37.8 60,37.2 C56.4,38.4 52,40.6 48,42.8 C42,43.2 36,44.2 30.6,45.4 Z", c['fig'], c['ln'], 0.9)
    s += P("M56.6,31.8 C58.4,30.2 61,30.4 62.2,32.2 C60.6,33.8 58.2,33.8 56.6,31.8 Z", c['ln'])       # eye hole
    s += P("M62.4,35.8 L66.8,39.6", 'none', c['ln'], 1.2)                                           # nose guard
    s += P("M35.4,40.4 C41,37.4 49,35 55,34.2", 'none', c['ln'], 0.8)
    return s


def reeds(c):
    s = ''
    for (x1, y1, x2, y2, bend, w) in [(38, 32, 24, 6, -7, 2.2), (43, 29, 40, 1, 3, 2.4), (48, 28, 60, 4, 7, 2.2), (35, 38, 16, 22, -5, 2)]:
        mx, my = (x1 + x2) / 2 + bend, (y1 + y2) / 2
        s += P(f"M{x1-w},{y1} Q{mx-w},{my} {x2},{y2} Q{mx+w},{my} {x1+w},{y1} Z", c['fig'], c['ln'], 0.5)
        s += P(f"M{x1},{y1} Q{mx},{my} {x2},{y2}", 'none', c['ln'], 0.4)
    return s


def water(c):
    s = ''
    for k, y in enumerate((70, 78, 86, 94)):
        x0 = 60 + (k % 2) * 3
        d = f"M{x0},{y}"
        for i in range(4):
            d += f" c3,-3.4 6,-3.4 9,0"
        s += P(d, 'none', c['fig'], 1.6)
    return s


def round_shield(c, cx=82, cy=66, r=19):
    s = C_(cx, cy, r, c['fig'], c['ln'], 0.9)
    s += C_(cx, cy, r - 3.2, 'none', c['ln'], 0.7)
    s += C_(cx, cy, r - 8.4, 'none', c['ln'], 0.6)
    s += C_(cx, cy, 3.4, c['ln'])
    for k in range(12):
        a = k * math.pi / 6
        s += C_(round(cx + (r - 5.8) * math.cos(a), 2), round(cy + (r - 5.8) * math.sin(a), 2), 0.7, c['ln'])
    for k in range(6):
        a = k * math.pi / 3 + 0.3
        x, y = cx + (r - 11.6) * math.cos(a), cy + (r - 11.6) * math.sin(a)
        s += P(f"M{x-1.4:.1f},{y:.1f} L{x+1.4:.1f},{y:.1f} M{x:.1f},{y-1.4:.1f} L{x:.1f},{y+1.4:.1f}", 'none', c['ln'], 0.5)
    return s


def tower_shield(c):
    s = P("M68,100 L68,34 C68,24 76,18 84,18 C92,18 100,24 100,34 L100,100 Z", c['fig'], c['ln'], 0.9)
    s += P("M71.4,100 L71.4,35 C71.4,27 77,21.6 84,21.6 C91,21.6 96.6,27 96.6,35 L96.6,100", 'none', c['ln'], 0.7)
    for y in (46, 62, 78):
        s += P(f"M71.4,{y} L96.6,{y}", 'none', c['ln'], 0.6)
    return s


def flames(c):
    s = ''
    for (x, h, w) in [(38, 12, 3.2), (43, 16, 3.6), (48.6, 13, 3.2), (53.4, 10, 2.8)]:
        base = 23 if x > 40 else 26
        s += P(f"M{x-w},{base} C{x-w},{base-h*0.5} {x-0.4},{base-h*0.6} {x},{base-h} "
               f"C{x+0.6},{base-h*0.6} {x+w},{base-h*0.5} {x+w},{base} Z", c['acc'], c['ln'], 0.5)
    return s


def nestor_cup(c):
    s = P("M68,62 C68,70 72,75 81,75 C90,75 94,70 94,62 Z", c['acc'], c['ln'], 0.7)
    s += P("M79,75 L83,75 L84,82 L78,82 Z M74,84 C76,82.6 86,82.6 88,84 Z", c['acc'], c['ln'], 0.5)
    s += P("M68,63 C63,62 62,54 66,50 M94,63 C99,62 100,54 96,50", 'none', c['acc'], 1.5)
    for (x, y, f) in [(65.4, 48.6, -1), (96.6, 48.6, 1)]:
        s += P(f"M{x-3*f},{y} C{x-1.6*f},{y-2.4} {x+1.6*f},{y-2.6} {x+3.2*f},{y-1} L{x+4.4*f},{y-0.6} "
               f"L{x+3*f},{y+0.2} C{x+1*f},{y+1.4} {x-1.6*f},{y+1.2} {x-3*f},{y} Z", c['acc'], c['ln'], 0.4)
    s += P("M71,66 C76,67.6 86,67.6 91,66", 'none', c['ln'], 0.5)
    return s


def wheel(c, cx=82, cy=70, r=15):
    s = C_(cx, cy, r, 'none', c['fig'], 2.6)
    s += C_(cx, cy, r, 'none', c['ln'], 0.5)
    s += C_(cx, cy, 3.2, c['fig'], c['ln'], 0.5)
    for k in range(4):
        a = k * math.pi / 4 + 0.4
        s += P(f"M{cx + 3*math.cos(a):.1f},{cy + 3*math.sin(a):.1f} L{cx + (r-1)*math.cos(a):.1f},{cy + (r-1)*math.sin(a):.1f} "
               f"M{cx - 3*math.cos(a):.1f},{cy - 3*math.sin(a):.1f} L{cx - (r-1)*math.cos(a):.1f},{cy - (r-1)*math.sin(a):.1f}",
               'none', c['fig'], 1.6)
    return s


def staff(c, x0=76, y0=100, x1=84, y1=18, crook=True):
    s = P(f"M{x0},{y0} L{x1},{y1+6}", 'none', c['obj'], 2)
    if crook:
        s += P(f"M{x1},{y1+6} C{x1},{y1} {x1+7},{y1-2} {x1+8},{y1+4}", 'none', c['obj'], 2)
    return s


def laurel_sprig(c):
    s = P("M68,90 C74,80 80,72 90,64", 'none', c['fig'], 1.1)
    for i, (x, y) in enumerate([(71, 85), (74.4, 80), (78, 75.6), (82, 71.4), (86.4, 67.4), (90, 64)]):
        a = -40 if i % 2 else 50
        s += f'<ellipse cx="{x}" cy="{y}" rx="3.4" ry="1.4" transform="rotate({a} {x} {y})" fill="{c["fig"]}" stroke="{c["ln"]}" stroke-width="0.4"/>'
    s += P("M80,40 C83,36 86,35 88,36 C90,33 93,32 96,33 C94,34.6 92.6,36 92,38 C89,40 84,40.6 80,40 Z", c['fig'], c['ln'], 0.5)
    s += P("M78,32 C81,29.4 84,29 86,30.4", 'none', c['fig'], 0.9)
    return s


def pointed_skull(c):
    s = P("M36,36 C37,26 44,14 50,9 C54,14 57,21 58,29 C52,30 44,32 36,36 Z", c['skin'], c['ln'], 0.8)
    for d in ["M45,15 L43,12", "M49,11 L48.4,7.6", "M53,14 L54.4,11", "M41,20 L38.6,18", "M56,20 L58,18.4"]:
        s += P(d, 'none', c['hair'], 1.1)
    return s


def earring(c, x=44.6, y=54.6):
    return C_(x, y, 1.3, c['acc'], c['ln'], 0.4) + P(f"M{x},{y-1.3} L{x},{y-3}", 'none', c['ln'], 0.5)


def phiale(c):
    s = P("M64,70 C64,78 72,84 82,84 C92,84 100,78 100,70 Z", c['acc'], c['ln'], 0.7)
    s += P("M63,70 L101,70", 'none', c['ln'], 1.4)
    s += C_(82, 76.6, 2.6, 'none', c['ln'], 0.6)
    for k in range(8):
        a = k * math.pi / 8 + math.pi / 16
        s += P(f"M{82 + 4.6*math.cos(a):.1f},{76.6 + 4*math.sin(a) * 0.5:.1f} L{82 + 14*math.cos(a):.1f},{72 + 10*math.sin(a):.1f}",
               'none', c['ln'], 0.4)
    return s


def robe(c):
    s = P("M64,100 C64,86 66,74 72,66 C78,60 88,60 94,64 C98,70 100,84 100,100 Z", c['fig'], c['ln'], 0.7)
    s += P("M66,86 C76,82 88,82 99,86 M65,94 C76,90 88,90 99,94", 'none', c['ln'], 0.7)
    for x in range(68, 100, 4):
        s += C_(x, 88.8, 0.7, c['ln'])
    s += P("M72,66 C74,74 74,84 73,98 M86,62 C86,72 87,86 88,98", 'none', c['ln'], 0.5)
    return s


def tears(c):
    return (P("M57.6,47 C57.2,48.6 57.4,49.6 58,50 C58.6,49.6 58.6,48.4 57.6,47 Z", c['wh'], c['ln'], 0.3)
            + P("M58.6,52.4 C58.2,54 58.4,55 59,55.4 C59.6,55 59.6,53.8 58.6,52.4 Z", c['wh'], c['ln'], 0.3))


def phrygian_cap(c):
    s = P("M30.6,46 C28.4,36 32,25 41,19.6 C46,16.4 52,15 56,13 C60,11.4 63,12.4 63.6,15.2 C61,15.6 59.4,17.6 60,20.4 "
          "C61.2,25 61.6,29 60.6,32.6 C52,34.6 42,38.8 36,43 L36.6,62 C34.6,64 32.2,64 30.4,62 Z", c['fig'], c['ln'], 0.8)
    s += P("M32.2,40 C41,36.4 51,32.6 60.8,29.2", 'none', c['ln'], 1)
    for (x, y) in [(40, 26), (46, 23), (52, 20), (44, 31), (50, 28.4), (38, 33)]:
        s += C_(x, y, 0.8, c['ln'])
    s += P("M31.6,48 L35.4,48 M31.8,54 L35.6,54", 'none', c['ln'], 0.5)
    return s


def apple(c, x=82, y=70):
    s = C_(x, y, 6.4, c['acc'], c['ln'], 0.7)
    s += P(f"M{x},{y-6} C{x-0.4},{y-9} {x+0.6},{y-11} {x+2},{y-12}", 'none', c['ln'], 0.9)
    s += P(f"M{x+1},{y-9.4} C{x+4},{y-11} {x+6.4},{y-10} {x+7},{y-8} C{x+4.6},{y-7.2} {x+2.6},{y-7.8} {x+1},{y-9.4} Z",
           c['fig'], c['ln'], 0.4)
    s += P(f"M{x-3},{y-2} C{x-2},{y-3.6} {x-0.6},{y-4} {x+0.4},{y-3.8}", 'none', c['wh'], 0.8, ' opacity=".7"')
    return s


def mirror(c):
    s = P("M82,100 L82,80", 'none', c['obj'], 2.4)
    s += P("M78,82 L86,82", 'none', c['obj'], 1.6)
    s += C_(82, 67, 12, c['acc'], c['ln'], 0.8)
    s += C_(82, 67, 9.4, 'none', c['ln'], 0.5)
    s += P("M76,62 C78,59 81,58 84,58.4", 'none', c['wh'], 0.9, ' opacity=".7"')
    return s


def wings(c):
    s = ''
    for side in (1,):
        s += P("M34,70 C20,64 8,50 4,30 C10,34 14,36 18,37 C12,30 10,22 10,14 C16,22 21,26 26,28 C22,20 22,12 24,6 "
               "C30,20 36,30 42,40 C44,50 42,60 34,70 Z", c['fig'], c['ln'], 0.7)
        for d in ["M36,62 C26,56 16,46 10,34", "M38,52 C30,46 22,38 16,24", "M40,44 C34,36 28,26 26,12"]:
            s += P(d, 'none', c['ln'], 0.5)
    return s


def eagle_snake(c, x=82, y=34):
    g = f'<g transform="translate({x} {y})">'
    g += P("M-16,-2 C-10,-10 -2,-12 4,-8 L12,-12 L10,-6 C14,-4 16,-2 17,0 C12,0 8,1 4,2 C0,6 -8,6 -12,3 Z",
           c['fig'], c['ln'], 0.6)
    g += P("M-16,-2 C-12,-16 -2,-20 6,-18 C0,-14 -4,-10 -6,-6", c['fig'], c['ln'], 0.5)
    g += C_(13.6, -2.4, 0.7, c['ln'])
    g += P("M0,4 C-2,10 4,12 2,18 C0,22 -6,22 -6,26", 'none', c['fig'], 1.6)
    g += P("M0,4 C-2,10 4,12 2,18 C0,22 -6,22 -6,26", 'none', c['ln'], 0.4)
    g += '</g>'
    return g


def wolf_hood(c):
    s = P("M29,50 C26,36 31,24 42,19 C47,17 52,17 56,18.6 L62,15 L61.6,20.4 C64,22 66.6,25.4 68.6,29 "
          "L72,31.4 C72.6,33 72,34.6 70.6,35 L64,35.4 C58,35.4 52,37.4 47,40 C40,43 34,47 31,54 Z",
          c['fig'], c['ln'], 0.8)
    s += P("M44,19.4 L41.6,11 L48.4,17.4 Z", c['fig'], c['ln'], 0.6)
    s += C_(60, 25.4, 0.9, c['ln'])
    s += P("M64,31.6 L70,32.6", 'none', c['ln'], 0.6)
    for (x, y) in [(36, 30), (40, 26), (46, 23), (52, 22), (38, 38), (44, 33), (50, 30), (33, 44)]:
        s += P(f"M{x-1},{y-0.6} L{x},{y+0.8} L{x+1},{y-0.6}", 'none', c['ln'], 0.45)
    s += P("M31,54 C28,62 26,70 22,78 C28,76 32,70 34,62", c['fig'], c['ln'], 0.6)
    return s


def fillet_staff(c):
    s = P("M76,100 L84,16", 'none', c['acc'], 2.2)
    s += C_(84.2, 14, 2.6, c['acc'], c['ln'], 0.5)
    for (dx, l) in [(-1.6, 18), (1.2, 22), (3.4, 15)]:
        s += P(f"M{83.6+dx*0.2},20 C{83+dx},{24} {84+dx*1.6},{20+l*0.6} {82.6+dx*2},{20+l}", 'none', c['wh'], 1.1)
    for y in (24, 30):
        s += P(f"M81.6,{y} L86,{y}", 'none', c['wh'], 1.6)
    return s


def necklace_small(c):
    s = ''
    for i in range(9):
        t = i / 8
        x = 50.4 + t * 9
        y = 74 + 6 * math.sin(t * math.pi)
        s += C_(round(x, 1), round(y, 1), 0.95 if i % 2 else 1.3, c['acc'], c['ln'], 0.3)
    return s


def baby(c):
    """Round-headed infant in profile, with the nodding crest at the edge."""
    s = ''
    s += P("M98,6 C88,10 80,18 76,28 L80,29 C84,21 90,15 98,12 Z", c['hair'], c['hl'], 0.8)
    for i in range(6):
        s += P(f"M{96-i*3.2},{8+i*3.2} L{93-i*3.2},{7+i*3.2}", 'none', c['hl'], 0.5)
    s += P("M14,100 C16,90 26,82 38,80 C46,84 56,84 62,80 C74,82 84,90 86,100 Z", c['fig'], c['ln'], 0.8)
    s += P("M40,80 C48,84 56,84 62,80", 'none', c['ln'], 0.7)
    s += P("M56,30 C66,32 72,42 72,52 C72,56 71,58 70.4,59.6 C70.8,61 70,62.6 68.4,63 C68.6,65 67.6,67 65,68 "
           "C64,74 60,78 54,80 L44,80 C38,78 30,72 28,60 C26,46 34,30 56,30 Z", c['skin'], c['ln'], 0.8)
    s += P("M56,30 C46,29 36,34 31,44 C30,48 29.6,52 30,56 C33,52 35,46 40,43 C46,40 52,38 56,36 C60,34.4 60,31.4 56,30 Z",
           c['hair'], c['hl'], 0.7)
    for (x, y) in [(35, 44), (40, 40), (46, 37), (52, 35)]:
        s += C_(x, y, 1, 'none', c['hl'], 0.5)
    s += ear(c, -4, 8)
    s += P("M61,49.6 Q64,48 66.4,49.8", 'none', c['ln'], 0.9)
    s += P("M62.4,52.6 Q64.6,54 66.6,52.4", 'none', c['ln'], 0.6)
    s += C_(65, 51.6, 0.9, c['ln'])
    s += P("M69.4,61.6 L67.4,61.8", 'none', c['ln'], 0.8)
    s += P("M60.6,56 C62,58 63.4,58.6 64.6,58.4", 'none', c['ln'], 0.5)   # cheek
    s += P("M64.8,55 Q66.4,52.8 64.2,51.4", 'none', c['ln'], 0.0)
    # tear
    s += P("M66,55 C65.6,56.8 65.8,57.8 66.4,58.2 C67,57.8 67,56.6 66,55 Z", c['wh'], c['ln'], 0.3)
    return s


def demi_face_old(c):
    return face_lines(c, old=True)


# ------------------------------------------------------------------ characters
def person(c, hair_kind='short', beard_kind=None, old=False, hair_col=None, beard_col=None, himation=False,
           show_ear=True, eye_kind='open'):
    return std_person(c, hair_kind, beard_kind, old=old, hair_col=hair_col, beard_col=beard_col,
                      himation=himation, show_ear=show_ear, eye_kind=eye_kind)


def woman(c, hair_kind='bun', old=False, show_ear=True):
    s = garment(c) + head(c) + hair(c, hair_kind)
    if show_ear:
        s += ear(c)
    s += eye(c) + face_lines(c, old=old)
    return s


def build(pid, c=None):
    """c: palette dict; defaults to red-figure. Other books pass their own palettes."""
    c = c or C
    bg = f'<rect width="100" height="100" fill="{c["bg"]}"/>'
    if pid in ('zeus', 'athena', 'poseidon', 'hermes', 'odysseus', 'menelaus'):
        return O.build(pid, c)
    s = ''
    if pid == 'hera':
        s = scepter(c, 76, 100, 84, 12, lotus=True) + garment(c) + head(c) + plain_veil(c) + front_hair_under(c) + polos(c) + eye(c) + face_lines(c)
    elif pid == 'hephaestus':
        s = person(c, 'short', 'short', himation=True) + work_cap(c) + hammer_tongs(c)
    elif pid == 'thetis':
        s = woman(c, 'long') + fillet(c, c['fig'], 1.6) + dolphin(c, 79, 62, 1.15)
    elif pid == 'aphrodite':
        s = woman(c, 'bun') + stephane(c) + dove(c, 80, 62, 1.2)
    elif pid == 'apollo':
        s = lyre(c) + person(c, 'long') + wreath(c)
    elif pid == 'ares':
        s = spear(c, 72, 100, 86, 4) + person(c, 'short', 'point', show_ear=False) + corinthian(c, crest=True)
    elif pid == 'scamander':
        s = reeds(c) + person(c, 'long', 'long') + fillet(c, c['acc'], 1.4) + water(c)
    elif pid == 'achilles':
        s = person(c, 'long') + fillet(c, c['acc'], 1.6) + round_shield(c)
    elif pid == 'agamemnon':
        s = scepter(c, 76, 100, 84, 12) + person(c, 'short', 'long') + stephane(c, c['acc'], points=True)
    elif pid == 'patroclus':
        s = spear(c, 72, 100, 86, 6) + person(c, 'short', 'short', show_ear=False) + attic_helmet(c, crest=True)
    elif pid == 'diomedes':
        s = spear(c, 72, 100, 86, 6) + person(c, 'short', 'short', show_ear=False) + flames(c) + attic_helmet(c, crest=False)
    elif pid == 'ajax':
        s = person(c, 'short', 'short', show_ear=False) + attic_helmet(c, crest=False) + tower_shield(c)
    elif pid == 'nestor':
        s = person(c, 'long', 'long', old=True, hair_col=c['wh'], beard_col=c['wh']) + fillet(c) + nestor_cup(c)
    elif pid == 'antilochus':
        s = person(c, 'short') + fillet(c) + wheel(c)
    elif pid == 'phoenix':
        s = staff(c) + person(c, 'short', 'long', old=True, hair_col=c['wh'], beard_col=c['wh'], himation=True)
    elif pid == 'calchas':
        s = person(c, 'long', 'short', himation=True) + wreath(c) + laurel_sprig(c)
    elif pid == 'thersites':
        s = garment(c) + head(c) + pointed_skull(c) + beard(c, 'point') + ear(c) + eye(c) + face_lines(c, old=True)
        s += P("M53.4,39.2 L61.2,41.8", 'none', c['ln'], 1.1)
    elif pid == 'briseis':
        s = garment(c) + head(c) + front_hair_under(c) + plain_veil(c) + eye(c) + face_lines(c) + earring(c, 47.4, 55.6)
        s += P("M58.4,30.2 C52,30.6 44.6,31.6 39.4,27", 'none', c['ln'], 1.2)
    elif pid == 'hector':
        s = spear(c, 72, 100, 88, 6) + person(c, 'short', 'short', show_ear=False) + corinthian(c, crest=True, tall=True)
    elif pid == 'priam':
        s = person(c, 'long', 'long', old=True, hair_col=c['wh'], beard_col=c['wh']) + stephane(c, c['acc']) + phiale(c)
    elif pid == 'hecuba':
        s = garment(c) + head(c) + front_hair_under(c) + veil(c) + eye(c) + face_lines(c, old=True) + robe(c)
    elif pid == 'andromache':
        s = garment(c) + head(c) + front_hair_under(c) + veil(c) + eye(c) + face_lines(c) + tears(c)
    elif pid == 'astyanax':
        return bg + baby(c)
    elif pid == 'paris':
        s = person(c, 'short', show_ear=False) + phrygian_cap(c) + apple(c, 82, 70)
    elif pid == 'helen':
        s = mirror(c) + garment(c) + head(c) + front_hair_under(c) + plain_veil(c) + stephane(c, c['acc']) + eye(c) + face_lines(c)
    elif pid == 'aeneas':
        s = spear(c, 72, 100, 86, 6) + person(c, 'short', 'short', show_ear=False) + attic_helmet(c, crest=False)
        s += P("M40,28 C44,24 50,22 56,22.4", 'none', c['acc'], 1.4)
    elif pid == 'sarpedon':
        s = wings(c) + person(c, 'long', 'short') + stephane(c, c['acc'], points=True)
    elif pid == 'glaucus':
        cc = dict(c); cc['fig'] = c['acc']
        s = spear(c, 72, 100, 86, 6) + person(c, 'short', 'short', show_ear=False) + attic_helmet(cc, crest=True)
    elif pid == 'pandarus':
        s = bow(c) + person(c, 'short', 'point', show_ear=False) + attic_helmet(c, crest=False)
    elif pid == 'polydamas':
        s = person(c, 'short', 'short', himation=True) + fillet(c) + eagle_snake(c, 80, 30)
    elif pid == 'dolon':
        s = spear(c, 72, 100, 86, 8) + person(c, 'short', 'short', show_ear=False) + wolf_hood(c)
    elif pid == 'chryses':
        s = fillet_staff(c) + person(c, 'long', 'long', old=True, hair_col=c['wh'], beard_col=c['wh'], himation=True) + fillet(c, c['wh'], 2)
    elif pid == 'chryseis':
        s = woman(c, 'bun') + fillet(c, c['fig'], 1.6) + necklace_small(c)
    else:
        raise KeyError(pid)
    return bg + zoom(s)


IDS = ['zeus', 'hera', 'athena', 'poseidon', 'hermes', 'hephaestus', 'thetis', 'aphrodite', 'apollo', 'ares',
       'scamander', 'achilles', 'agamemnon', 'menelaus', 'patroclus', 'odysseus', 'diomedes', 'ajax', 'nestor',
       'antilochus', 'phoenix', 'calchas', 'thersites', 'briseis', 'hector', 'priam', 'hecuba', 'andromache',
       'astyanax', 'paris', 'helen', 'aeneas', 'sarpedon', 'glaucus', 'pandarus', 'polydamas', 'dolon', 'chryses',
       'chryseis']


def symbols():
    out = []
    for pid in IDS:
        out.append(f'<symbol id="pt-{pid}" viewBox="0 0 100 100">'
                   f'<clipPath id="pc-{pid}"><circle cx="50" cy="50" r="50"/></clipPath>'
                   f'<g clip-path="url(#pc-{pid})">{build(pid)}</g></symbol>')
    return '\n'.join(out)
