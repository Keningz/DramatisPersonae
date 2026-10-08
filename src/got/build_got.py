# -*- coding: utf-8 -*-
"""Builds the Game of Thrones (TV) page (got.html): a map of Westeros and Essos laid out by region, north at the top,
with each great house drawn as a small family tree in its own lands, and an episode timeline that keeps the story
spoiler-free up to the episode you have reached.

The people are shown as seals in their house colours with a small generic emblem for their role at the time and the
first letter of their name (no portraits and no sigils: the characters and their sigils belong to the series)."""
import json, html, os, re, sys
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.dirname(HERE)
COMMON = os.path.join(SRC, 'common')
os.chdir(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, COMMON)
import dpsite as SITE_MOD  # noqa: E402
from data_got import (NODES, EDGES, EDGE_TYPES, CAMPS, HOUSES, GROUPS, ACTS, DOWN, EPISODES, SEASONS, LAST,  # noqa: E402
                      code, ref_zh, ref_en, GLYPHS, EMBLEMS, EM_HOME)
from episodes_got import *  # noqa: E402,F401,F403

esc = html.escape
bi = SITE_MOD.bi
NODE = {n['id']: n for n in NODES}

# ---------------------------------------------------------------- the map
W, H = 1400, 1176
R_OV = 22
BY, NWY = 90, 230                            # beyond the Wall, the Night's Watch
G1, G2, G3 = 334, 420, 520                   # the North: three generations
D1, D2 = 632, 722                            # Iron Islands, Riverlands, Vale, Dragonstone
K1, K2, K3 = 832, 922, 1012                  # the Reach, King's Landing, the Stormlands
DY = 1114                                    # Dorne
T1, T2 = 82, 202                             # the Targaryens
Q1, Q2 = 360, 478                            # the queen's people
F1, F2 = 632, 722                            # the Free Cities

OV = {
  # beyond the Wall
  'craster': (120, BY), 'gilly': (190, BY), 'mance': (330, BY), 'tormund': (400, BY), 'ygritte': (470, BY),
  'threeeyed': (650, BY), 'nightking': (900, BY),
  # the Night's Watch
  'jeor': (380, NWY), 'aemon': (450, NWY), 'alliser': (520, NWY), 'edd': (590, NWY), 'olly': (660, NWY), 'sam': (730, NWY),
  # the North
  'lyanna': (400, G2), 'benjen': (470, G2), 'ned': (560, G2), 'catelyn': (630, G2),
  'jon': (400, G3), 'talisa': (470, G3), 'robb': (540, G3), 'sansa': (610, G3), 'arya': (680, G3), 'bran': (750, G3), 'rickon': (820, G3),
  'roose': (90, G2), 'ramsay': (90, G3), 'meera': (190, G2), 'jojen': (260, G2), 'lyannamo': (225, G3),
  'luwin': (920, G2), 'hodor': (1000, G2), 'osha': (960, G3),
  # the Iron Islands
  'balon': (80, D1), 'euron': (180, D1), 'yara': (60, D2), 'theon': (130, D2),
  # the Riverlands
  'blackfish': (380, D1), 'edmure': (300, D2), 'walder': (465, 677), 'beric': (555, D1), 'thoros': (555, D2),
  # the Vale
  'jonarryn': (690, D1), 'lysa': (770, D1), 'robin': (730, D2),
  # Dragonstone
  'stannis': (900, D1), 'selyse': (980, D1), 'davos': (868, D2), 'shireen': (940, D2), 'melisandre': (1022, D2),
  # the Reach
  'olenna': (100, K1), 'mace': (100, K2), 'loras': (65, K3), 'margaery': (135, K3), 'randyll': (232, K2),
  # King's Landing: the Lannisters and the royal family
  'kevan': (345, K1), 'tywin': (425, K1), 'lancel': (345, K2), 'tyrion': (405, K2), 'jaime': (465, K2), 'cersei': (525, K2),
  'robert': (595, K2), 'joffrey': (530, K3), 'myrcella': (595, K3), 'tommen': (660, K3),
  # King's Landing: the court and the swords
  'varys': (600, K1), 'littlefinger': (670, K1), 'pycelle': (740, K1), 'highsparrow': (810, K1),
  'sandor': (690, K2), 'gregor': (750, K2), 'qyburn': (810, K2),
  'syrio': (355, K3), 'shae': (425, K3), 'bronn': (730, K3), 'pod': (800, K3),
  # the Stormlands
  'renly': (940, K1), 'brienne': (1030, K1), 'gendry': (985, K2),
  # Dorne
  'doran': (500, DY), 'oberyn': (580, DY), 'ellaria': (660, DY),
  # the Targaryens
  'aerys': (1170, T1), 'rhaegar': (1125, T2), 'viserys': (1195, T2), 'daenerys': (1265, T2), 'drogo': (1340, T2),
  # the queen's people
  'jorah': (1130, Q1), 'barristan': (1205, Q1), 'missandei': (1280, Q1), 'greyworm': (1350, Q1),
  'daario': (1165, Q2), 'hizdahr': (1305, Q2),
  # the Free Cities and the Dothraki sea
  'illyrio': (1135, F1), 'jaqen': (1335, F1), 'mirri': (1235, F2),
}
assert set(OV) == set(NODE), set(OV) ^ set(NODE)
CX, CY = 700, 588
R1 = [230, 372]
R2 = min(500, (H - 40) // 2, CX - 40)

# regions: (zh, en, x0, y0, x1, y1, camp colour for the tint)
REGIONS = [
  ('长城以北', 'Beyond the Wall', 20, 26, 1075, 148, 'beyond'),
  ('守夜人 · 黑城堡', 'The Night’s Watch', 20, 180, 1075, 282, 'nw'),
  ('北境', 'The North', 20, 296, 1075, 568, 'stark'),
  ('铁群岛', 'Iron Islands', 20, 584, 235, 772, 'greyjoy'),
  ('河间', 'Riverlands', 250, 584, 620, 772, 'river'),
  ('谷地', 'The Vale', 635, 584, 825, 772, 'arryn'),
  ('龙石岛', 'Dragonstone', 840, 584, 1075, 772, 'baratheon'),
  ('河湾', 'The Reach', 20, 788, 300, 1056, 'tyrell'),
  ('君临', 'King’s Landing', 315, 788, 880, 1056, 'lannister'),
  ('风暴地', 'Stormlands', 895, 788, 1075, 1056, 'baratheon'),
  ('多恩', 'Dorne', 400, 1072, 820, 1158, 'martell'),
  ('坦格利安家', 'House Targaryen', 1090, 26, 1385, 282, 'targaryen'),
  ('女王的人', 'The queen’s people', 1090, 296, 1385, 568, 'targaryen'),
  ('自由贸易城邦 · 多斯拉克海', 'Free Cities · Dothraki sea', 1090, 584, 1385, 772, 'essos'),
]

# people not on the map who complete a family tree
GHOST = {
  'rickard': (470, G1, '瑞卡德', 'Rickard'), 'hoster': (300, D1, '霍斯特', 'Hoster'),
  'joanna': (495, K1, '乔安娜', 'Joanna'), 'rhaella': (1250, T1, '蕾拉', 'Rhaella'),
}


# ---------------------------------------------------------------- whose side, in the whole-series view
def life_end(n):
    if n['dies']:
        return n['dies']
    chs = [p['ch'] for e in EDGES if n['id'] in (e['s'], e['t']) for p in e['phases']]
    return max(chs + [n['debut']] + [c[0] for c in n['camps']])


def home_camp(n):
    """The side a person belongs to in the whole-series view: the one held longest (unless set by hand)."""
    if n['home']:
        return n['home']
    held = Counter()
    end = life_end(n)
    cs = n['camps']
    for j, c in enumerate(cs):
        nxt = cs[j + 1][0] if j + 1 < len(cs) else end + 1
        held[c[1]] += max(1, nxt - c[0])
    return max(held, key=lambda k: (held[k], -[c[1] for c in cs].index(k)))


HOME = {n['id']: home_camp(n) for n in NODES}


def home_emblem(n):
    """The emblem in the whole-series view: the one held longest (unless set by hand)."""
    v = n['id']
    if v in EM_HOME:
        return EM_HOME[v]
    held = Counter()
    em, end = EMBLEMS[v], life_end(n)
    for j, (ep, g) in enumerate(em):
        nxt = em[j + 1][0] if j + 1 < len(em) else end + 1
        held[g] += max(1, nxt - ep)
    return max(held, key=lambda k: (held[k], -[g for _, g in em].index(k)))


EM = {n['id']: home_emblem(n) for n in NODES}


def initials(n):
    """The letter on a seal: the first character of the Chinese name; the first letter of the English name."""
    en = re.sub(r'^(The|Maester|High|Khal) ', '', n['en'])
    return n['zh'][0], en[0]


INI = {n['id']: initials(n) for n in NODES}


# ---------------------------------------------------------------- svg pieces
def use(pid, extra=''):
    return f'<use xlink:href="#pt-{pid}" href="#pt-{pid}"{extra}/>'


def seal_symbols():
    out = []
    for n in NODES:
        bg, ink = HOUSES[n['house']]
        out.append(f'<symbol id="pt-{n["id"]}" viewBox="0 0 100 100"><circle cx="50" cy="50" r="50" fill="{bg}"/>'
                   f'<circle cx="50" cy="50" r="42" fill="none" stroke="{ink}" stroke-width="1.6" opacity=".45"/></symbol>')
    for k, (_, _, markup) in GLYPHS.items():
        out.append(f'<symbol id="em-{k}" viewBox="0 0 100 100">{markup}</symbol>')
    return ''.join(out)


def emb(key, ink, x, y, size):
    return (f'<use class="emb" xlink:href="#em-{key}" href="#em-{key}" x="{x}" y="{y}" width="{size}" height="{size}" '
            f'color="{ink}"/>')


DEAD = '<g class="dead" transform="translate(29 29)"><circle r="9"/><path d="M-3.8,-3.8 L3.8,3.8 M3.8,-3.8 L-3.8,3.8"/></g>'


def node_svg(v):
    n = NODE[v]
    x, y = OV[v]
    k = R_OV / 40
    zi, ei = INI[v]
    ink = HOUSES[n['house']][1]
    s = (f'<g class="node camp-{HOME[v]}" data-id="{v}" tabindex="0" role="button" '
         f'transform="translate({x} {y})" aria-label="{esc(n["zh"])}">')
    s += f'<g class="pt" transform="scale({k})"><circle class="glow" r="47"/><circle class="hit" r="48"/>'
    s += ('<g class="flip">' + use(v, ' x="-40" y="-40" width="80" height="80"') + emb(EM[v], ink, -29, -38, 58) +
          f'<text class="ini" y="25" dy=".36em" text-anchor="middle" fill="{ink}" data-zh="{esc(zi)}" data-en="{esc(ei)}">{esc(zi)}</text></g>')
    s += '<circle class="ring" r="40" stroke-width="3.6"/>'
    if n['born']:      # a little seal with the woman's birth family, shown in the overview
        s += (f'<g class="seal" transform="translate(-31 -31)"><rect x="-8" y="-8" width="16" height="16" rx="2.5"/>'
              f'<text y="5.2" text-anchor="middle">{esc(n["born"][0][0])}</text></g>')
    if (n['death'] and n['death'][2]) or n['down']:
        s += DEAD
    s += '</g>'
    s += f'<text class="nm" y="{40 * k + 16}" text-anchor="middle" font-size="13.5">{esc(n["zh"])}</text>'
    s += f'<text class="sb" y="{40 * k + 30}" text-anchor="middle" font-size="12">{esc(n["sub"][0])}</text>'
    return s + '</g>'


def edge_svg(i, e):
    a, b = OV[e['s']], OV[e['t']]
    return f'<path class="edge t-{e["phases"][-1]["type"]}" data-e="{i}" d="M{a[0]},{a[1]} L{b[0]},{b[1]}"/>'


def label_svg(i, e):
    return (f'<g class="elab t-{e["phases"][-1]["type"]}" data-e="{i}" tabindex="-1" role="button">'
            f'<rect x="0" y="0" width="10" height="21" rx="10.5"/><text x="0" y="0" text-anchor="middle"></text></g>')


def mini(pid, size, cls='mini'):
    n = NODE[pid]
    sw = 7 if size < 50 else 5
    zi, ei = INI[pid]
    ink = HOUSES[n['house']][1]
    inner = use(pid, ' x="-50" y="-50" width="100" height="100"') + emb(EMBLEMS[pid][0][1], ink, -36, -47, 72)
    ini = (f'<text class="ini" y="31" dy=".36em" text-anchor="middle" font-size="20" fill="{ink}">'
           f'<tspan class="l-zh">{esc(zi)}</tspan><tspan class="l-en" font-size="21">{esc(ei)}</tspan></text>')
    return (f'<svg class="{cls} camp-{HOME[pid]}" viewBox="-56 -56 112 112" width="{size}" height="{size}" aria-hidden="true">'
            f'{inner}{ini}<circle class="ring" r="50" stroke-width="{sw}"/></svg>')


def T(zh, en, x, y, cls='', anchor='start', extra=''):
    return (f'<text class="{cls}" x="{x}" y="{y}" text-anchor="{anchor}" data-zh="{esc(zh)}" data-en="{esc(en)}"{extra}>'
            f'{esc(zh)}</text>')


RN = R_OV + 3          # clearance around a seal
NAMEGAP = 44           # from a seal's center to below its name


def pos(k):
    return OV[k] if k in OV else GHOST[k][:2]


def when(frm=None, until=None):
    return (f' data-from="{frm}"' if frm else '') + (f' data-until="{until}"' if until else '')


def marriage(a, b, frm=None, until=None):
    (xa, y), (xb, _) = pos(a), pos(b)
    x0, x1 = min(xa, xb) + RN, max(xa, xb) - RN
    return f'<path class="gl wed"{when(frm, until)} d="M{x0},{y - 1.6} L{x1},{y - 1.6} M{x0},{y + 1.6} L{x1},{y + 1.6}"/>'


def sibling(a, b):
    (xa, y), (xb, _) = pos(a), pos(b)
    x0, x1 = min(xa, xb) + RN, max(xa, xb) - RN
    return f'<path class="gl sis" d="M{x0},{y} L{x1},{y}"/>'


def descent(parents, children, drop=0, cls='gl', frm=None, until=None):
    """From the middle of the parents (or below a single parent) down to a bar, then down to each child."""
    ps = [pos(p) for p in parents]
    px = sum(p[0] for p in ps) / len(ps)
    py = ps[0][1]
    cs = [pos(c) for c in children]
    cy = cs[0][1]
    bar = cy - 36 + drop
    y0 = py + (NAMEGAP if len(parents) == 1 else 2)
    xs = [c[0] for c in cs] + [px]
    d = f'M{px},{y0} L{px},{bar} M{min(xs)},{bar} L{max(xs)},{bar}'
    for c in cs:
        d += f' M{c[0]},{bar} L{c[0]},{c[1] - RN}'
    return f'<path class="{cls}"{when(frm, until)} d="{d}"/>'


def ghost(k):
    x, y, zh, en = GHOST[k]
    return (f'<g class="ghost"><circle cx="{x}" cy="{y}" r="12"/>'
            + T(zh, en, x, y + 4, 'gname', 'middle') + '</g>')


deco = '<g class="deco">'
for zh, en, x0, y0, x1, y1, camp in REGIONS:
    deco += f'<rect class="reg reg-{camp}" x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" rx="10"/>'
for zh, en, x0, y0, x1, y1, camp in REGIONS:
    deco += T(zh, en, x0 + 10, y0 + 17, f'regname c-{camp}', 'start')
# the Wall
deco += '<rect class="wall" x="20" y="158" width="1055" height="12" rx="3"/>'
deco += T('长城', 'THE WALL', 547, 168, 'wallname', 'middle')
deco += T('临冬城', 'Winterfell', 600, G1 - 6, 'place', 'middle')
deco += T('恐怖堡 · 熊岛 · 颈泽', 'Dreadfort · Bear Island · the Neck', 160, G1 - 6, 'place', 'middle')
deco += T('临冬城的家臣', 'Winterfell’s household', 960, G1 - 6, 'place', 'middle')
deco += T('奔流城 · 孪河城', 'Riverrun · the Twins', 435, D1 - 30, 'place', 'middle')
deco += T('凯岩城 · 红堡', 'Casterly Rock · the Red Keep', 590, K1 - 32, 'place', 'end')
deco += T('御前会议与宫中', 'The council and the court', 705, K1 - 32, 'place', 'middle')
deco += T('弥林', 'Meereen', 1235, Q2 - 30, 'place', 'middle')
# family trees
deco += ''.join(ghost(k) for k in GHOST)
deco += descent(['rickard'], ['lyanna', 'benjen', 'ned'])
deco += marriage('ned', 'catelyn') + descent(['ned', 'catelyn'], ['robb', 'sansa', 'arya', 'bran', 'rickon'])
deco += marriage('talisa', 'robb', frm=S2E10)
# Jon: Ned's bastard, until the Tower of Joy shows whose son he is
deco += f'<path class="gl con"{when(until=S6E10)} d="M560,{G2 + NAMEGAP} L560,{G2 + NAMEGAP + 6} L400,{G2 + NAMEGAP + 6} L400,{G3 - RN}"/>'
deco += f'<path class="gl"{when(frm=S6E10)} d="M400,{G2 + NAMEGAP} L400,{G3 - RN}"/>'
deco += T('私生子', 'bastard', 476, G2 + NAMEGAP + 2, 'gtag', 'middle', when(until=S6E10))
deco += T('莱安娜之子', 'Lyanna’s son', 352, G3 - 40, 'gtag', 'middle', when(frm=S6E10))
deco += f'<path class="gl"{when(frm=S3E10)} d="M90,{G2 + NAMEGAP} L90,{G3 - RN}"/>'
deco += sibling('meera', 'jojen')
deco += sibling('balon', 'euron') + descent(['balon'], ['yara', 'theon'])
deco += sibling('hoster', 'blackfish') + descent(['hoster'], ['edmure'])
deco += marriage('jonarryn', 'lysa') + descent(['jonarryn', 'lysa'], ['robin'])
deco += marriage('stannis', 'selyse') + descent(['stannis', 'selyse'], ['shireen'])
deco += descent(['olenna'], ['mace']) + descent(['mace'], ['loras', 'margaery'])
deco += sibling('kevan', 'tywin') + descent(['kevan'], ['lancel'])
deco += marriage('tywin', 'joanna') + descent(['tywin', 'joanna'], ['tyrion', 'jaime', 'cersei'])
deco += marriage('cersei', 'robert') + descent(['cersei', 'robert'], ['joffrey', 'myrcella', 'tommen'])
deco += sibling('doran', 'oberyn')
deco += marriage('aerys', 'rhaella') + descent(['aerys', 'rhaella'], ['rhaegar', 'viserys', 'daenerys'])
deco += marriage('daenerys', 'drogo')
# house words, in the empty south-east
WORDS = [('史塔克', '凛冬将至', 'Stark', 'Winter Is Coming'), ('兰尼斯特', '听我怒吼', 'Lannister', 'Hear Me Roar'),
         ('拜拉席恩', '怒火燎原', 'Baratheon', 'Ours Is the Fury'), ('坦格利安', '血火同源', 'Targaryen', 'Fire and Blood'),
         ('葛雷乔伊', '强取胜于苦耕', 'Greyjoy', 'We Do Not Sow'), ('徒利', '家族、责任、荣誉', 'Tully', 'Family, Duty, Honor'),
         ('提利尔', '茁壮成长', 'Tyrell', 'Growing Strong'), ('马泰尔', '不屈不挠', 'Martell', 'Unbowed, Unbent, Unbroken'),
         ('艾林', '高如荣誉', 'Arryn', 'As High as Honor')]
deco += T('家族箴言', 'HOUSE WORDS', 1110, 822, 'amuhd', 'start')
for j, (hz, wz, he, we) in enumerate(WORDS):
    y = 852 + j * 30
    deco += T(hz, he, 1110, y, 'whouse', 'start') + T(wz, we, 1190, y, 'amu', 'start')
deco += '</g>'

rings = f'<g class="rings"><circle cx="{CX}" cy="{CY}" r="{R1[1] - 60}"/><circle cx="{CX}" cy="{CY}" r="{R2}"/></g>'
defs = '<defs><filter id="tl-grey"><feColorMatrix type="saturate" values="0.08"/></filter></defs>'
edges_svg = '<g class="edges">' + ''.join(edge_svg(i, e) for i, e in enumerate(EDGES)) + '</g>'
labels_svg = '<g class="labels">' + ''.join(label_svg(i, e) for i, e in enumerate(EDGES)) + '</g>'
nodes_svg = '<g class="nodes">' + ''.join(node_svg(n['id']) for n in NODES) + '</g>'
MAP = (f'<svg id="map" class="mode-ov" viewBox="0 0 {W} {H}" role="img" aria-label="权力的游戏人物关系图 / Game of Thrones character map" '
       f'xmlns:xlink="http://www.w3.org/1999/xlink">{defs}{deco}{rings}{edges_svg}{labels_svg}{nodes_svg}</svg>')

# ---------------------------------------------------------------- timeline control
TRACK_FRAC = 0.92
acts_html = ''.join(f'<div class="tlact"><span class="tln">{bi(a["zs"], a["es"])}</span></div>' for a in ACTS)
TIMELINE = f'''<div class="tl" id="tl">
  <div class="tlhead">
    <button type="button" class="tlbtn tlplay" id="tl-play" aria-label="播放"><span class="ic" aria-hidden="true">▶</span></button>
    <div class="tlnow" aria-live="polite"><span class="tlch" id="tl-ch"></span><span class="tltitle" id="tl-title"></span></div>
    <button type="button" class="tlbtn tlall" id="tl-all" aria-pressed="true">{bi('全剧', 'Whole series')}</button>
  </div>
  <div class="tltrack all" id="tl-track" role="slider" tabindex="0" aria-label="集数 / Episode" aria-valuemin="1" aria-valuemax="74" aria-valuenow="74">
    <div class="tlacts" style="width:{TRACK_FRAC * 100:.0f}%">{acts_html}</div>
    <div class="tlend" style="left:{TRACK_FRAC * 100:.0f}%">{bi('全剧', 'All')}</div>
    <div class="tlfill" id="tl-fill"></div>
    <div class="tlhandle" id="tl-handle"></div>
  </div>
  <div class="tlstat" id="tl-stat"></div>
</div>'''


# ---------------------------------------------------------------- roster
def strip_refs(s):
    return re.sub(r' ?\(S\d+E\d+(?:[—–]S\d+E\d+)?\)', '', s)


def first_sub(n):
    return (n['subs'][0][1], n['subs'][0][2]) if n['subs'] else n['sub']


roster = ''
for key, zh, en, dzh, den in GROUPS:
    items = [n for n in NODES if n['grp'] == key]
    roster += (f'<div class="rgroup"><h3>{bi(zh, en)}<span class="cnt">{len(items)}</span>'
               f'<span class="rdesc">{bi(dzh, den)}</span></h3><div class="rgrid">')
    for n in items:
        v = n['id']
        fz, fe = first_sub(n)
        b0 = n['bios'][0]
        when_zh = ('首次提到于 ' if n['dies'] == 0 else '') + code(n['debut']) + ('' if n['dies'] == 0 else ' 登场')
        when_en = ('First mentioned in ' if n['dies'] == 0 else 'Appears in ') + code(n['debut'])
        roster += (f'<button class="rcard" data-id="{v}" type="button">{mini(v, 64, "rp")}'
                   f'<span class="rtext"><span class="rname">{bi(esc(n["zh"]), esc(n["en"]))}'
                   f'<span class="rgr">{bi(esc(n["full"][1]), esc(n["full"][0]))}</span></span>'
                   f'<span class="rsub">{bi(esc(fz), esc(fe))}</span>'
                   f'<span class="rlife">{bi(when_zh, when_en)}</span>'
                   f'<span class="rbio">{bi(esc(strip_refs(b0[1])), esc(strip_refs(b0[2])))}</span></span></button>')
    roster += '</div></div>'

# ---------------------------------------------------------------- legend
dash = {'kin': '', 'love': '', 'mas': '10 3 2 3', 'aid': '', 'foe': '7 5', 'tie': '1.5 4.5'}
toggles = ''.join(
    f'<button class="tog t-{k}" data-type="{k}" aria-pressed="true" type="button" title="{v["desc"]}">'
    f'<svg width="34" height="10" aria-hidden="true"><line x1="2" y1="5" x2="32" y2="5" stroke-dasharray="{dash[k]}"/></svg>'
    f'{bi(v["zh"], v["en"])}<span class="tc">0</span></button>' for k, v in EDGE_TYPES.items())
swatches = ''.join(f'<span class="lgi"><span class="sw camp-{k}" aria-hidden="true"></span>{bi(v["zh"], v["en"])}</span>'
                   for k, v in CAMPS.items())
emblem_key = ''.join(
    f'<span class="lgi"><svg class="emi" viewBox="0 0 100 100" aria-hidden="true"><use xlink:href="#em-{k}" href="#em-{k}"/></svg>'
    f'{bi(z, e)}</span>' for k, (z, e, _) in GLYPHS.items())
n_phase = sum(len(e['phases']) for e in EDGES)
n_changing = sum(1 for e in EDGES if len(e['phases']) > 1)
n_dead = sum(1 for n in NODES if n['dies'])


# ---------------------------------------------------------------- data for the page script
def ph(p):
    return dict(ch=p['ch'], type=p['type'], label=p['zl'], text=p['zt'], label_en=p['el'], text_en=p['et'],
                bk=ref_zh(p['ref']), bk_en=ref_en(p['ref']), alt=p['ref'] != p['ch'])


def node_data(n):
    v = n['id']
    zi, ei = INI[v]
    d = dict(zh=n['zh'], en=n['en'], gr=n['full'][1], full=n['full'][0], full_en=n['full'][1],
             debut=n['debut'], dies=(n['dies'] or None), pre=(n['dies'] == 0),
             death=(n['death'][0] if n['death'] else None), death_en=(n['death'][1] if n['death'] else None),
             violent=bool(n['death'] and n['death'][2]),
             camps=[list(c) for c in n['camps']], home=HOME[v],
             born=(n['born'][0] if n['born'] else None), born_en=(n['born'][1] if n['born'] else None),
             sub=n['sub'][0], sub_en=n['sub'][1], subs=[list(s) for s in n['subs']], bios=[list(b) for b in n['bios']],
             ini=zi, ini_en=ei, ink=HOUSES[n['house']][1], ox=OV[v][0], oy=OV[v][1],
             em=[list(x) for x in EMBLEMS[v]], emHome=EM[v])
    if n['seen']:
        d['seen'] = n['seen']
    if n['down']:
        d['down'] = [[a, b] + list(DOWN[v]) for a, b in n['down']]
    return d


DATA = {
    'nodes': {n['id']: node_data(n) for n in NODES},
    'order': [n['id'] for n in NODES],
    'edges': [dict(s=e['s'], t=e['t'], phases=[ph(p) for p in e['phases']]) for e in EDGES],
    'types': EDGE_TYPES,
    'camp': {k: dict(zh=v['zh'], en=v['en']) for k, v in CAMPS.items()},
    'campsLabel': {'zh': '阵营', 'en': 'Side'},
    'acts': [dict(a=a['a'], b=a['b']) for a in ACTS],
    'chapters': [dict(zh=z, en=e) for z, e in EPISODES],
    'trackFrac': TRACK_FRAC, 'uniform': True, 'last': LAST, 'page': 'got',
    'seasons': SEASONS, 'spoil': True, 'remember': True,
    'allTitle': {'zh': '全剧八季七十三集', 'en': 'All 8 seasons, 73 episodes'},
    'allHint': {'zh': '拖动上面的滑块到你看到的那一集，后面的剧情都不会显示；或按 ▶ 从第一集播放',
                'en': 'Drag the slider to the episode you have reached and nothing after it will show — or press ▶ to play from the start'},
    'W': W, 'H': H, 'CX': CX, 'CY': CY, 'R_OV': R_OV, 'R1': R1, 'R2': R2,
    'title': {'zh': '权力的游戏人物谱', 'en': 'Who’s Who in Game of Thrones'},
}

starts = ''.join(f'<button class="chipbtn" type="button" data-go="{v}">{mini(v, 26, "mini")}{bi(NODE[v]["zh"], NODE[v]["en"])}</button>'
                 for v in ['jon', 'daenerys', 'tyrion', 'arya', 'cersei', 'sansa'])
MOMENTS = [(S1E9, '贝勒圣堂', 'Baelor'), (S2E9, '黑水河之战', 'Blackwater'), (S3E9, '红色婚礼', 'The Red Wedding'),
           (S4E2, '紫色婚礼', 'The Purple Wedding'), (S4E8, '比武审判', 'Viper and Mountain'), (S5E8, '艰难屯', 'Hardhome'),
           (S6E5, '阿多', 'Hodor'), (S6E9, '私生子之战', 'Battle of the Bastards'), (S6E10, '大圣堂', 'The Sept'),
           (S7E7, '龙与狼', 'Dragon and wolf'), (S8E3, '长夜', 'The Long Night'), (S8E6, '铁王座', 'The Iron Throne')]
moments = ''.join(f'<button class="chipbtn introgo" type="button" data-ch="{c}"><span class="chn">{code(c)}</span>{bi(zh, en)}</button>'
                  for c, zh, en in MOMENTS)

INTRO = f'''<div class="intro">
  <h2>{bi('怎么看这张图', 'How to read this map')}</h2>
  <ol class="howto">
    <li>{bi('上方的滑块是剧集，八季共七十三集。拖到你看到的那一集，图上就只剩到那一集为止已经出场的人：死去的人变成灰色，死于非命的另加 ✕；外圈的颜色是他此时站在哪一边；连线也换成那一集的关系。点开人物，经历、阵营和关系史也只讲到这一集，后面的剧情一概不显示。浏览器会记住你停在哪一集。按 ▶ 可以从第一集一路播放。',
            'The slider runs through all 73 episodes of the eight seasons. Stop at the episode you have reached and the map shows only the people who have appeared by then: the dead turn grey, with a ✕ for a violent death; each seal’s outer ring shows whose side that person is on at that moment; and every line shows the relationship as it stands. Open a person and their story, sides and relationships also stop at that episode — nothing later is shown. Your browser remembers where you stopped. Press ▶ to play from the first episode.')}</li>
    <li>{bi('全景大致按地理排开：长城以北在最上，往下是守夜人、北境，再往南是铁群岛、河间、谷地、龙石岛，然后是河湾、君临、风暴地和多恩；狭海对岸的坦格利安家和厄索斯在右边。各大家族在自己的地盘上排成小家谱，嫁进来的女子，左上角的小印是她的娘家。',
            'The overview is laid out roughly like the map: beyond the Wall at the top, then the Night’s Watch and the North; further south the Iron Islands, the Riverlands, the Vale and Dragonstone; then the Reach, King’s Landing, the Stormlands and Dorne. The Targaryens and Essos are across the Narrow Sea on the right. Each great house is drawn as a small family tree in its own lands; a little seal on a married woman shows the family she was born into.')}</li>
    <li>{bi('每个人是一枚印：底色是他出身家族的颜色，中间的小图案是他此时的身份（王冠是国王或王后，火炬是守夜人，锁是被囚禁……），会随剧情改变，下方是名字的第一个字。点任何人，他就移到中央，与他（在这一集）有关系的人围成一圈；点连线上的字，看这段关系前后怎样变化；点图上空白处回到全景。',
            'Each person is a seal in the colours of their house. The little emblem shows their role at that point (a crown for a king or queen, a torch for the Night’s Watch, a padlock for a captive …) and changes as the story goes on; below it is the first letter of their name. Click anyone to bring them to the center with everyone connected to them (as of this episode) in a ring around them; click a line label to see how that relationship changed; click empty space to return to the overview.')}</li>
    <li>{bi(f'图中 {len(NODES)} 人、{len(EDGES)} 段关系，共 {n_phase} 个阶段，每个阶段都注明出自哪一集；其中 {n_changing} 段关系前后有变化，{n_dead} 人死在剧中。',
            f'The map has {len(NODES)} people and {len(EDGES)} relationships in {n_phase} stages, each with the episode it happens in; {n_changing} relationships change over the series, and {n_dead} people die in it.')}</li>
  </ol>
  <p class="l-zh" lang="zh-CN" style="color:var(--muted);font-size:13px">从这些人开始：</p><p class="l-en" lang="en" style="color:var(--muted);font-size:13px">Start with:</p>
  <div class="starts">{starts}</div>
  <p class="l-zh" lang="zh-CN" style="color:var(--muted);font-size:13px;margin-top:12px">或者跳到这些集（会剧透）：</p><p class="l-en" lang="en" style="color:var(--muted);font-size:13px;margin-top:12px">Or jump to (spoilers):</p>
  <div class="starts">{moments}</div>
</div>'''

css_raw = (open(os.path.join(COMMON, 'dynamic.css'), encoding='utf-8').read()
           + open(os.path.join(COMMON, 'timeline.css'), encoding='utf-8').read()
           + open('page_got.css', encoding='utf-8').read())
js = SITE_MOD.NAV_JS + open(os.path.join(COMMON, 'timeline.js'), encoding='utf-8').read()
css = SITE_MOD.FONTFACES + css_raw + SITE_MOD.NAV_CSS

legend = (f'<div class="lg"><span class="lgt">{bi("外圈＝此时的阵营", "Outer ring = side at the time")}</span>{swatches}'
          f'<span class="lgi"><span class="sw gonesw" aria-hidden="true"></span>{bi("已死（变灰）", "Dead (greyed)")}</span>'
          f'<span class="lgi"><span class="deadmark" aria-hidden="true">✕</span>{bi("死于非命", "Violent death")}</span>'
          f'<span class="lgi"><span class="sealmark" aria-hidden="true">徒</span>{bi("娘家", "Born into")}</span></div>'
          f'<div class="lg" role="group" aria-label="按关系类型显示连线 / Show lines by type"><span class="lgt">{bi("连线", "Lines")}</span>{toggles}</div>'
          f'<details class="emlg"><summary>{bi("印章上的图案：此时的身份", "Seal emblems: the role at the time")}</summary><div class="emgrid">{emblem_key}</div></details>')

body = f'''<svg width="0" height="0" style="position:absolute" aria-hidden="true" xmlns:xlink="http://www.w3.org/1999/xlink"><defs>{seal_symbols()}</defs></svg>
<div class="page" id="app" data-lang="zh">
<header class="top">
  <div class="topbar">
    {SITE_MOD.nav_html('got')}
    <div class="langsw" role="group" aria-label="语言 / Language">
      <button type="button" data-setlang="zh" aria-pressed="true" lang="zh-CN">中文</button>
      <button type="button" data-setlang="en" aria-pressed="false" lang="en">English</button>
    </div>
  </div>
  <p class="eyebrow">{bi('HBO 电视剧', 'HBO television series')} <span class="gr">2011–2019</span> {bi('八季 · 七十三集', '8 seasons · 73 episodes')}</p>
  <h1>{bi('权力的游戏人物谱', 'Who’s Who in Game of Thrones')}</h1>
  <p class="lede">{bi(f'维斯特洛与厄索斯的 {len(NODES)} 个人物、{len(EDGES)} 段随剧集变化的关系。拖到你看到的那一集，不会被剧透。',
                       f'{len(NODES)} people of Westeros and Essos and {len(EDGES)} relationships that change episode by episode. Stop at the episode you have reached, and nothing later is given away.')}</p>
  <div class="legend">{legend}</div>
</header>

<section class="stage">
  <div class="mapcol">
    <div class="toolbar">
      <div class="grp"><button type="button" id="btn-ov" disabled>{bi('← 全景', '← Overview')}</button></div>
      <div class="grp" role="group" aria-label="缩放 / Zoom">
        <button type="button" data-z="-1" aria-label="缩小 / Zoom out">−</button>
        <button type="button" data-z="0" aria-label="适应宽度 / Fit">{bi('适应', 'Fit')}</button>
        <button type="button" data-z="1" aria-label="放大 / Zoom in">＋</button>
      </div>
      <p class="tbhint">{bi('点人物换主角 · 点连线上的字看原委 · 点空白处回到全景', 'Click a person to put them at the center · a line label for the story · empty space for the overview')}</p>
    </div>
    {TIMELINE}
    <div class="mapscroll" id="mapscroll">{MAP}</div>
  </div>
  <aside class="panel" id="panel" aria-live="polite">{INTRO}</aside>
</section>

<section class="roster" id="roster">
  <h2>{bi('人物一览', 'All characters')}</h2>
  <p class="rnote">{bi('这里只写每个人出场时的身份，不剧透。', 'Each card describes the person as they first appear — no spoilers.')}</p>
  {roster}
</section>

<footer class="foot">
  <p>{bi('人物、关系与集数依据 HBO 电视剧《权力的游戏》（2011—2019），只收电视剧里的情节，与原著小说《冰与火之歌》不同之处一概以电视剧为准。人名和集名的中文译法参照冰与火之歌中文维基。',
         'People, relationships and episode numbers follow the HBO series Game of Thrones (2011–2019); where the show departs from George R. R. Martin’s novels, the show is followed. Chinese names and episode titles follow the Chinese A Song of Ice and Fire wiki.')}</p>
  <p>{bi('剧中人物与家族纹章受版权保护，本页不画肖像和纹章，只用各家族的颜色、名字的首字和表示身份的通用小图案（王冠、剑、火炬之类）做成印章。',
         'The characters and the house sigils belong to the series, so this page draws neither portraits nor sigils: each person is a seal in their house colours with the first letter of their name and a generic emblem for their role (a crown, a sword, a torch and so on).')}</p>
</footer>
</div>
<script>const DATA = {json.dumps(DATA, ensure_ascii=False)};</script>
<script>const INTRO_HTML = {json.dumps(INTRO, ensure_ascii=False)};</script>
<script>{js}</script>
'''

size = SITE_MOD.write_page('got.html', '权力的游戏人物谱',
                           '《权力的游戏》电视剧人物关系图，按剧集拖动不剧透，中英双语 · A bilingual, spoiler-safe map of the characters of Game of Thrones, episode by episode.', css, body)
print('ok got', size // 1024, 'KB')
