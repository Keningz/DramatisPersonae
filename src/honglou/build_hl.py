# -*- coding: utf-8 -*-
"""Builds the Dream of the Red Chamber page (honglou.html): a family tree of the four great houses with a chapter
timeline. The overview lays the families out side by side — the Shis on the left, the Ning and Rong mansions in the
middle, the Lins, Wangs and Xues on the right — one row per generation, with the servants and the outside world in
bands below. A switch adds the last forty chapters (the Cheng-Gao continuation)."""
import json, html, os, re, sys
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.dirname(HERE)
COMMON = os.path.join(SRC, 'common')
os.chdir(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, COMMON)
import dpsite as SITE_MOD  # noqa: E402
from data_hl import NODES, EDGES, EDGE_TYPES, CAMPS, GROUPS, ACTS, CUT, LAST, ref_zh, ref_en  # noqa: E402
from chapters_hl import CH_ZH, CH_EN  # noqa: E402
from portraits_hl import symbols  # noqa: E402

esc = html.escape
bi = SITE_MOD.bi
NODE = {n['id']: n for n in NODES}

# ---------------------------------------------------------------- the family tree
W, H = 1340, 846
HDR, G1, G2, G3, G4 = 34, 118, 238, 358, 478       # column titles, then one row per generation
SA, SB, OUT = 600, 684, 792                          # servants (two rows) and the outside world
R_OV = 24

OV = {
  # 史家
  'xiangyun': (66, G3),
  # 宁国府
  'jiajing': (325, G2), 'youerjie': (136, G3), 'yousanjie': (190, G3), 'youshi': (244, G3), 'jiazhen': (298, G3),
  'xichun': (352, G3), 'jiaqiang': (217, G4), 'jiarong': (271, G4), 'qinkeqing': (325, G4),
  # 荣国府 · 长房 and 二房
  'jiamu': (646, G1), 'jiashe': (449, G2), 'xingfuren': (503, G2), 'jialian': (422, G3), 'xifeng': (476, G3),
  'yingchun': (530, G3), 'qiaojie': (449, G4),
  'wangfuren': (708, G2), 'jiazheng': (762, G2), 'zhaoyiniang': (843, G2), 'liwan': (654, G3), 'yuanchun': (708, G3),
  'baoyu': (762, G3), 'tanchun': (816, G3), 'jiahuan': (870, G3), 'jialan': (627, G4), 'jiarui': (735, G4), 'jiayun': (789, G4),
  # 林 · 王 · 薛
  'linruhai': (940, G2), 'daiyu': (940, G3), 'wangziteng': (1010, G2),
  'xueyima': (1134, G2), 'xiajingui': (1080, G3), 'xuepan': (1134, G3), 'baochai': (1188, G3), 'xueke': (1258, G3), 'baoqin': (1312, G3),
  # servants, under the households they serve
  'cuilv': (66, SA), 'jiaoda': (190, SA), 'ruhua': (352, SA), 'lingguan': (244, SB),
  'pinger': (422, SA), 'qiutong': (476, SA), 'siqi': (530, SA), 'baoer': (449, SB), 'wangshanbao': (503, SB),
  'yuanyang': (600, SA), 'shadajie': (654, SA), 'zhouruijia': (708, SA), 'jinchuan': (762, SA), 'yuchuan': (816, SA), 'caixia': (870, SA),
  'limama': (573, SB), 'mingyan': (627, SB), 'xiren': (681, SB), 'qingwen': (735, SB), 'sheyue': (789, SB), 'xiaohong': (843, SB), 'fangguan': (897, SB),
  'zijuan': (940, SA), 'xueyan': (960, SB), 'xiangling': (1134, SA), 'yinger': (1188, SA),
  # the world outside, near the people they touch
  'zhanghua': (136, OUT), 'liuxianglian': (190, OUT), 'qinzhong': (298, OUT), 'zhineng': (352, OUT),
  'liulaolao': (449, OUT), 'sunshaozu': (530, OUT), 'madaopo': (600, OUT), 'beijingwang': (654, OUT),
  'jiangyuhan': (708, OUT), 'zhenbaoyu': (762, OUT), 'miaoyu': (816, OUT), 'yucun': (900, OUT), 'jiaoxing': (954, OUT),
  'shiyin': (1134, OUT), 'fengyuan': (1188, OUT),
  # the Land of Illusion, above it all
  'jinghuan': (98, G1), 'sengdao': (170, G1),
}
assert set(OV) == set(NODE), set(OV) ^ set(NODE)
CX, CY = W // 2, H // 2 - 6
R1 = [230, 372]
R2 = min(470, (H - 40) // 2, CX - 40)

# columns: (zh, en, x0, x1, camp colour)
COLS = [('史', 'Shi', 38, 94, 'shi'), ('宁国府', 'Ning mansion', 106, 382, 'ning'), ('荣国府', 'Rong mansion', 394, 900, 'rong'),
        ('林', 'Lin', 912, 970, 'lin'), ('王', 'Wang', 982, 1038, 'wang'), ('薛', 'Xue', 1050, 1336, 'xue')]


# ---------------------------------------------------------------- households in the whole-book view
def life_end(n, cap):
    if n['dies'] and n['dies'] <= cap:
        return n['dies']
    chs = [p['ch'] for e in EDGES if n['id'] in (e['s'], e['t']) for p in e['phases'] if p['ch'] <= cap]
    return max(chs + [n['debut']] + [c[0] for c in n['camps'] if c[0] <= cap])


def home_camp(n, cap):
    """The household a person belongs to in the whole-book view: the one they spent longest in."""
    held = Counter()
    end = life_end(n, cap)
    cs = [c for c in n['camps'] if c[0] <= cap]
    for j, c in enumerate(cs):
        nxt = cs[j + 1][0] if j + 1 < len(cs) else end + 1
        held[c[1]] += max(1, nxt - c[0])
    return max(held, key=lambda k: (held[k], -[c[1] for c in cs].index(k)))


HOME = {n['id']: home_camp(n, LAST) for n in NODES}
HOME80 = {n['id']: home_camp(n, CUT) for n in NODES}


# ---------------------------------------------------------------- svg pieces
def use(pid, extra=''):
    return f'<use xlink:href="#pt-{pid}" href="#pt-{pid}"{extra}/>'


DEAD = '<g class="dead" transform="translate(29 29)"><circle r="9"/><path d="M-3.8,-3.8 L3.8,3.8 M3.8,-3.8 L-3.8,3.8"/></g>'


def node_svg(v):
    n = NODE[v]
    x, y = OV[v]
    k = R_OV / 40
    s = (f'<g class="node camp-{HOME80[v]}" data-id="{v}" tabindex="0" role="button" '
         f'transform="translate({x} {y})" aria-label="{esc(n["zh"])}">')
    s += f'<g class="pt" transform="scale({k})"><circle class="glow" r="47"/><circle class="hit" r="48"/>'
    s += '<g class="flip">' + use(v, ' x="-40" y="-40" width="80" height="80"') + '</g>'
    s += '<circle class="ring" r="40" stroke-width="3.6"/>'
    if n['born']:      # a little seal with the woman's birth family, shown in the overview
        s += (f'<g class="seal" transform="translate(-31 -31)"><rect x="-8" y="-8" width="16" height="16" rx="2.5"/>'
              f'<text y="5.2" text-anchor="middle">{esc(n["born"][0])}</text></g>')
    if n['death'] and n['death'][2]:
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
    dead = ('<g class="dead" transform="translate(36 36)"><circle r="12"/><path d="M-5,-5 L5,5 M5,-5 L-5,5"/></g>'
            if n['death'] and n['death'][2] and n['dies'] <= CUT else '')
    inner = use(pid, ' x="-50" y="-50" width="100" height="100"')
    return (f'<svg class="{cls} camp-{HOME80[pid]}" viewBox="-56 -56 112 112" width="{size}" height="{size}" aria-hidden="true">'
            f'{inner}<circle class="ring" r="50" stroke-width="{sw}"/>{dead}</svg>')


def T(zh, en, x, y, cls='', anchor='start', extra=''):
    return (f'<text class="{cls}" x="{x}" y="{y}" text-anchor="{anchor}" data-zh="{esc(zh)}" data-en="{esc(en)}"{extra}>'
            f'{esc(zh)}</text>')


# genealogy lines
RN = R_OV + 3          # clearance around a portrait
NAMEGAP = 48           # from a portrait's center to below its name


def marriage(a, b, kind='wed'):
    (xa, y), (xb, _) = (OV[a] if a in OV else GHOST[a][:2]), (OV[b] if b in OV else GHOST[b][:2])
    x0, x1 = min(xa, xb) + RN, max(xa, xb) - RN
    if kind == 'wed':
        return f'<path class="gl wed" d="M{x0},{y - 1.6} L{x1},{y - 1.6} M{x0},{y + 1.6} L{x1},{y + 1.6}"/>'
    return f'<path class="gl con" d="M{x0},{y} L{x1},{y}"/>'


def pos(k):
    return OV[k] if k in OV else GHOST[k][:2]


def descent(parents, children, drop=0):
    """From the middle of the parents (or below a single parent) down to a bar, then down to each child."""
    ps = [pos(p) for p in parents]
    px = sum(p[0] for p in ps) / len(ps)
    py = ps[0][1]
    cs = [pos(c) for c in children]
    cy = cs[0][1]
    bar = cy - 38 + drop
    y0 = py + (NAMEGAP if len(parents) == 1 else 2)
    xs = [c[0] for c in cs] + [px]
    d = f'M{px},{y0} L{px},{bar} M{min(xs)},{bar} L{max(xs)},{bar}'
    for c in cs:
        d += f' M{c[0]},{bar} L{c[0]},{c[1] - RN}'
    return f'<path class="gl" d="{d}"/>'


# people who are not on the map but complete the tree
GHOST = {
  'daihua': (325, G1, '贾代化', 'Daihua'), 'daishan': (590, G1, '贾代善', 'Daishan'),
  'jiamin': (890, G2, '贾敏', 'Jia Min'), 'jiazhu': (600, G3, '贾珠', 'Jia Zhu'),
  'xuegong': (1188, G2, '薛公', 'Mr Xue'), 'xueer': (1285, G2, '薛家二房', 'His brother'),
}


def ghost(k):
    x, y, zh, en = GHOST[k]
    return (f'<g class="ghost"><circle cx="{x}" cy="{y}" r="13"/>'
            + T(zh, en, x, y + 4, 'gname', 'middle') + '</g>')


deco = '<g class="deco">'
# family columns
for zh, en, x0, x1, camp in COLS:
    deco += f'<rect class="col col-{camp}" x="{x0}" y="{HDR + 14}" width="{x1 - x0}" height="{G4 + 50 - HDR - 14}" rx="12"/>'
for zh, en, x0, x1, camp in COLS:
    cx = (x0 + x1) / 2
    deco += T(zh + ('家' if len(zh) == 1 else ''), en, round(cx, 1), HDR + 2, f'colname c-{camp}', 'middle')
deco += T('长房 · 贾赦', 'Elder branch', 476, G2 - 50, 'branch', 'middle') + T('二房 · 贾政', 'Younger branch', 776, G2 - 50, 'branch', 'middle')
deco += T('族中子弟', 'Clansmen', 762, G4 + 52, 'branch', 'middle')
deco += f'<rect class="clan" x="705" y="{G4 - 34}" width="114" height="80" rx="10"/>'
# generation rows
for y, zh, en in ((G1, '代', 'I'), (G2, '文', 'II'), (G3, '玉', 'III'), (G4, '草', 'IV')):
    deco += f'<line class="genline" x1="14" y1="{y}" x2="30" y2="{y}"/>'
    deco += T(zh, en, 22, y - 8, 'gen', 'middle') + T('字辈', 'gen.', 22, y + 10, 'gensub', 'middle')
# the Land of Illusion
deco += f'<rect class="xian" x="58" y="{G1 - 40}" width="152" height="92" rx="16"/>'
deco += T('太虚幻境', 'Land of Illusion', 134, G1 - 46, 'colname c-kong', 'middle')
# the "officials' amulet" of chapter 4
AMULET = [('贾不假，白玉为堂金作马。', 'The Jias are no sham: their halls are jade, their horses gold.'),
          ('阿房宫，三百里，住不下金陵一个史。', 'A palace three hundred li long could not house the Shis of Jinling.'),
          ('东海缺少白玉床，龙王来请金陵王。', 'When the Dragon King lacks a jade bed, he asks the Wangs of Jinling.'),
          ('丰年好大雪，珍珠如土金如铁。', 'In a year of plenty the snow (Xue) lies deep: pearls like dirt, gold like iron.')]
deco += T('护官符（第4回）', 'The officials’ amulet (ch. 4)', 1004, G1 - 42, 'amuhd', 'start')
for j, (zh, en) in enumerate(AMULET):
    deco += T(zh, en, 1004, G1 - 20 + j * 19, 'amu', 'start')
# genealogy
deco += ghost('daihua') + ghost('daishan') + ghost('jiamin') + ghost('jiazhu') + ghost('xuegong') + ghost('xueer')
deco += f'<path class="gl" d="M325,{G1 + 15} L325,{G2 - RN}"/>'                 # 代化 -> 敬
deco += descent(['jiajing'], ['jiazhen', 'xichun'])
deco += marriage('youshi', 'jiazhen') + descent(['youshi', 'jiazhen'], ['jiarong'])
deco += marriage('jiarong', 'qinkeqing')
deco += f'<path class="gl sis" d="M136,{G3 - RN} L136,{G3 - 36} L244,{G3 - 36} L244,{G3 - RN} M190,{G3 - 36} L190,{G3 - RN}"/>'
deco += T('继妹', 'stepsisters', 163, G3 - 41, 'gtag', 'middle')
deco += T('宁府玄孙', 'of the Ning line', 200, G4 - 34, 'gtag', 'middle')
deco += marriage('daishan', 'jiamu')
deco += descent(['daishan', 'jiamu'], ['jiashe', 'jiazheng', 'jiamin'])
deco += marriage('jiashe', 'xingfuren') + descent(['jiashe', 'xingfuren'], ['jialian', 'yingchun'])
deco += marriage('jialian', 'xifeng') + descent(['jialian', 'xifeng'], ['qiaojie'])
deco += marriage('wangfuren', 'jiazheng') + marriage('jiazheng', 'zhaoyiniang', 'con')
deco += descent(['wangfuren', 'jiazheng'], ['jiazhu', 'yuanchun', 'baoyu'])
deco += descent(['jiazheng', 'zhaoyiniang'], ['tanchun', 'jiahuan'], drop=8)
deco += marriage('jiazhu', 'liwan') + descent(['jiazhu', 'liwan'], ['jialan'])
deco += marriage('jiamin', 'linruhai') + descent(['jiamin', 'linruhai'], ['daiyu'])
deco += marriage('xueyima', 'xuegong') + descent(['xueyima', 'xuegong'], ['xuepan', 'baochai'])
deco += marriage('xiajingui', 'xuepan')
deco += f'<path class="gl sis" d="M{1188 + 15},{G2} L{1285 - 15},{G2}"/>'
deco += descent(['xueer'], ['xueke', 'baoqin'])
# bands for the servants and the outside world
deco += f'<rect class="band" x="8" y="{SA - 40}" width="{W - 16}" height="{SB - SA + 82}" rx="12"/>'
deco += f'<rect class="band" x="8" y="{OUT - 40}" width="{W - 16}" height="84" rx="12"/>'
for y0, y1, zh, en in ((SA - 40, SB + 42, '丫鬟仆妇', 'SERVANTS'), (OUT - 40, OUT + 44, '府外', 'OUTSIDE')):
    cy = (y0 + y1) / 2
    chars = list(zh)
    zs = ''.join(f'<tspan x="26" dy="{0 if i == 0 else 17}">{esc(ch)}</tspan>' for i, ch in enumerate(chars))
    deco += (f'<text class="lname l-zh" x="26" y="{cy - (len(chars) - 1) * 8.5 + 5:.1f}" text-anchor="middle">{zs}</text>'
             f'<text class="lname l-en" x="0" y="0" text-anchor="middle" transform="translate(30 {cy:.1f}) rotate(-90)">{esc(en)}</text>')
deco += '</g>'

rings = f'<g class="rings"><circle cx="{CX}" cy="{CY}" r="{R1[1] - 60}"/><circle cx="{CX}" cy="{CY}" r="{R2}"/></g>'
defs = '<defs><filter id="tl-grey"><feColorMatrix type="saturate" values="0.08"/></filter></defs>'
edges_svg = '<g class="edges">' + ''.join(edge_svg(i, e) for i, e in enumerate(EDGES)) + '</g>'
labels_svg = '<g class="labels">' + ''.join(label_svg(i, e) for i, e in enumerate(EDGES)) + '</g>'
nodes_svg = '<g class="nodes">' + ''.join(node_svg(n['id']) for n in NODES) + '</g>'
MAP = (f'<svg id="map" class="mode-ov" viewBox="0 0 {W} {H}" role="img" aria-label="红楼梦人物关系图 / Dream of the Red Chamber character map" '
       f'xmlns:xlink="http://www.w3.org/1999/xlink">{defs}{deco}{rings}{edges_svg}{labels_svg}{nodes_svg}</svg>')

# ---------------------------------------------------------------- timeline control
TRACK_FRAC = 0.92
acts_html = ''.join(f'<div class="tlact"><span class="tln">{bi(a["zs"], a["es"])}</span></div>' for a in ACTS)
TIMELINE = f'''<div class="tl" id="tl">
  <div class="tlhead">
    <button type="button" class="tlbtn tlplay" id="tl-play" aria-label="播放"><span class="ic" aria-hidden="true">▶</span></button>
    <div class="tlnow" aria-live="polite"><span class="tlch" id="tl-ch"></span><span class="tltitle" id="tl-title"></span></div>
    <button type="button" class="tlbtn tllate" id="tl-late" aria-pressed="false" title="第八十一至一百二十回为程伟元、高鹗整理刊行的续书 / Chapters 81–120 are the continuation published by Cheng Weiyuan and Gao E"><span class="sw2" aria-hidden="true"></span>{bi('后四十回', 'Chapters 81–120')}</button>
    <button type="button" class="tlbtn tlall" id="tl-all" aria-pressed="true">{bi('全书', 'Whole book')}</button>
  </div>
  <div class="tltrack all" id="tl-track" role="slider" tabindex="0" aria-label="回目 / Chapter" aria-valuemin="1" aria-valuemax="81" aria-valuenow="81">
    <div class="tlacts" style="width:{TRACK_FRAC * 100:.0f}%">{acts_html}</div>
    <div class="tlend" style="left:{TRACK_FRAC * 100:.0f}%">{bi('全书', 'All')}</div>
    <div class="tlfill" id="tl-fill"></div>
    <div class="tlhandle" id="tl-handle"></div>
  </div>
  <div class="tlstat" id="tl-stat"></div>
</div>'''


# ---------------------------------------------------------------- roster
def life_line(n):
    d = n['death']
    zh = f'第{n["debut"]}回登场'
    en = f'Appears ch. {n["debut"]}'
    if d:
        late = n['dies'] > CUT
        zh += f' · 第{n["dies"]}回{d[0]}' + ('（续书）' if late else '')
        en += f' · {d[1]}, ch. {n["dies"]}' + (' (continuation)' if late else '')
    return bi(zh, en)


def strip_refs(s):
    return re.sub(r' ?\((?:第[0-9、至—]+回|chs?\. [0-9–, ]+)\)', '', s)


roster = ''
for key, zh, en, dzh, den in GROUPS:
    items = [n for n in NODES if n['grp'] == key]
    roster += (f'<div class="rgroup"><h3>{bi(zh, en)}<span class="cnt">{len(items)}</span>'
               f'<span class="rdesc">{bi(dzh, den)}</span></h3><div class="rgrid">')
    for n in items:
        v = n['id']
        roster += (f'<button class="rcard" data-id="{v}" type="button">{mini(v, 64, "rp")}'
                   f'<span class="rtext"><span class="rname">{bi(esc(n["zh"]), esc(n["en"]))}'
                   f'<span class="rgr">{bi(esc(n["py"]), esc(n["zh"]))}</span></span>'
                   f'<span class="rsub">{bi(esc(n["sub"][0]), esc(n["sub"][1]))}</span>'
                   f'<span class="rlife">{life_line(n)}</span>'
                   f'<span class="rbio">{bi(esc(strip_refs(n["bio"][0])), esc(strip_refs(n["bio"][1])))}</span></span></button>')
    roster += '</div></div>'

# ---------------------------------------------------------------- legend
dash = {'kin': '', 'love': '', 'mas': '10 3 2 3', 'aid': '', 'foe': '7 5', 'tie': '1.5 4.5'}
toggles = ''.join(
    f'<button class="tog t-{k}" data-type="{k}" aria-pressed="true" type="button" title="{v["desc"]}">'
    f'<svg width="34" height="10" aria-hidden="true"><line x1="2" y1="5" x2="32" y2="5" stroke-dasharray="{dash[k]}"/></svg>'
    f'{bi(v["zh"], v["en"])}<span class="tc">0</span></button>' for k, v in EDGE_TYPES.items())
swatches = ''.join(f'<span class="lgi"><span class="sw camp-{k}" aria-hidden="true"></span>{bi(v["zh"], v["en"])}</span>'
                   for k, v in CAMPS.items())
n_phase = sum(len(e['phases']) for e in EDGES)
n_changing = sum(1 for e in EDGES if len(e['phases']) > 1)
n_verse = sum(1 for n in NODES if n['verses'])

# ---------------------------------------------------------------- data for the page script
def ph(p):
    return dict(ch=p['ch'], type=p['type'], label=p['zl'], text=p['zt'], label_en=p['el'], text_en=p['et'],
                bk=ref_zh(p['ref']), bk_en=ref_en(p['ref']))


def verse(v):
    return dict(k=v['k'], t=v['t'], pic=v['pic'], zh=v['zh'], en=v['en'], note=v['note'])


DATA = {
    'nodes': {n['id']: dict(zh=n['zh'], en=n['en'], gr=n['py'], debut=n['debut'], dies=n['dies'],
                            death=(n['death'][0] if n['death'] else None), death_en=(n['death'][1] if n['death'] else None),
                            violent=bool(n['death'] and n['death'][2]),
                            camps=[list(c) for c in n['camps']], home=HOME[n['id']], home80=HOME80[n['id']],
                            born=(n['born'][0] if n['born'] else None), born_en=(n['born'][1] if n['born'] else None),
                            sub=n['sub'][0], sub_en=n['sub'][1], bio=n['bio'][0], bio_en=n['bio'][1],
                            late=(n['late'][0] if n['late'] else None), late_en=(n['late'][1] if n['late'] else None),
                            verses=[verse(v) for v in n['verses']],
                            icon=n['icon'][0], icon_en=n['icon'][1], ox=OV[n['id']][0], oy=OV[n['id']][1])
              for n in NODES},
    'order': [n['id'] for n in NODES],
    'edges': [dict(s=e['s'], t=e['t'], phases=[ph(p) for p in e['phases']]) for e in EDGES],
    'types': EDGE_TYPES,
    'camp': {k: dict(zh=v['zh'], en=v['en']) for k, v in CAMPS.items()},
    'campsLabel': {'zh': '所在', 'en': 'Household'},
    'acts': [dict(a=a['a'], b=a['b']) for a in ACTS],
    'chapters': [dict(zh=z, en=e) for z, e in zip(CH_ZH, CH_EN)],
    'trackFrac': TRACK_FRAC, 'uniform': True, 'cut': CUT, 'last': LAST, 'page': 'honglou',
    'W': W, 'H': H, 'CX': CX, 'CY': CY, 'R_OV': R_OV, 'R1': R1, 'R2': R2,
    'title': {'zh': '红楼梦人物谱', 'en': 'Who’s Who in the Dream of the Red Chamber'},
}

starts = ''.join(f'<button class="chipbtn" type="button" data-go="{v}">{mini(v, 26, "mini")}{bi(NODE[v]["zh"], NODE[v]["en"])}</button>'
                 for v in ['baoyu', 'daiyu', 'baochai', 'xifeng', 'jiamu', 'liulaolao'])
MOMENTS = [(3, '黛玉进府', 'Daiyu arrives'), (5, '太虚幻境', 'The dream'), (18, '元妃省亲', 'The visit'),
           (27, '黛玉葬花', 'Burying flowers'), (33, '宝玉挨打', 'The beating'), (40, '刘姥姥游园', 'Granny Liu'),
           (74, '抄检大观园', 'The search'), (77, '晴雯抱屈', 'Qingwen wronged'), (98, '黛玉之死（续）', 'Daiyu dies (late)'),
           (120, '归结红楼梦（续）', 'The end (late)')]
moments = ''.join(f'<button class="chipbtn introgo" type="button" data-ch="{c}"><span class="chn{" chl" if c > CUT else ""}">{c}</span>{bi(zh, en)}</button>'
                  for c, zh, en in MOMENTS)

INTRO = f'''<div class="intro">
  <h2>{bi('怎么看这张图', 'How to read this map')}</h2>
  <ol class="howto">
    <li>{bi('上方的滑块是回目。默认只显示曹雪芹原著的前八十回；打开“后四十回”开关，才加上程伟元、高鹗整理刊行的第八十一至一百二十回，续书里的事都标着“续”。拖到哪一回，图上就只剩到那一回为止已经登场的人：去世的人变成灰色，自尽、被害、中毒等死于非命的另加 ✕；小像边框的颜色是他此时所在的府第或家族；连线也换成那一回的关系。按 ▶ 可以从第一回一路播放。',
            'The slider above runs through the chapters. By default it shows only Cao Xueqin’s first eighty; switch on “Chapters 81–120” to add the continuation published by Cheng Weiyuan and Gao E, whose events are marked “late”. Wherever you stop, the map shows only the people who have appeared by then: the dead turn grey, with a ✕ for suicide, murder or poison; each portrait’s border takes the colour of the household that person belongs to at that moment; and every line shows the relationship as it stands in that chapter. Press ▶ to play from chapter 1.')}</li>
    <li>{bi('全景是一张家谱：横向按家族排开，史家在左，宁国府、荣国府居中，林、王、薛三家在右；纵向按辈分，贾家四代分别以“代”“文”“玉”“草”字取名。嫁进来的女子，小像左上角的小印是她的娘家。下面两排是各房的丫鬟仆妇，最下一排是府外和方外之人，左上角是太虚幻境。',
            'The overview is a family tree: the Shis on the left, the Ning and Rong mansions in the middle, the Lins, Wangs and Xues on the right, one row per generation (the four Jia generations are named after the radicals of their given names). A small seal on a married woman’s portrait shows the family she was born into. Below come the servants of each household, then the world outside; the Land of Illusion sits at the top left.')}</li>
    <li>{bi('点任何人，他就移到中央，与他（在这一回）有关系的人围成一圈；右边按回目列出他的经历，金陵十二钗等人还附有太虚幻境里的判词和曲子。点连线上的字，看这段关系前后怎样变化。点图上空白处回到全景。',
            'Click anyone to bring them to the center with everyone they are connected to (as of this chapter) in a ring around them; the panel tells their story chapter by chapter, and for the Twelve Beauties and a few others gives the verses Baoyu reads about them in the Land of Illusion. Click a line label to see how that relationship changed. Click empty space to return to the overview.')}</li>
    <li>{bi(f'图中 {len(NODES)} 人、{len(EDGES)} 段关系，共 {n_phase} 个阶段；其中 {n_changing} 段关系前后有变化，{n_verse} 人附有判词或诗曲。',
            f'The map has {len(NODES)} people and {len(EDGES)} relationships in {n_phase} stages; {n_changing} relationships change over the story, and {n_verse} people have verses.')}</li>
  </ol>
  <p class="l-zh" lang="zh-CN" style="color:var(--muted);font-size:13px">从这些人开始：</p><p class="l-en" lang="en" style="color:var(--muted);font-size:13px">Start with:</p>
  <div class="starts">{starts}</div>
  <p class="l-zh" lang="zh-CN" style="color:var(--muted);font-size:13px;margin-top:12px">或者跳到这些回目：</p><p class="l-en" lang="en" style="color:var(--muted);font-size:13px;margin-top:12px">Or jump to:</p>
  <div class="starts">{moments}</div>
</div>'''

css_raw = (open(os.path.join(COMMON, 'dynamic.css'), encoding='utf-8').read()
           + open(os.path.join(COMMON, 'timeline.css'), encoding='utf-8').read()
           + open('page_hl.css', encoding='utf-8').read())
js = SITE_MOD.NAV_JS + open(os.path.join(COMMON, 'timeline.js'), encoding='utf-8').read()
css = SITE_MOD.FONTFACES + SITE_MOD.PINYIN_FACE + css_raw + SITE_MOD.NAV_CSS

legend = (f'<div class="lg"><span class="lgt">{bi("小像边框＝此时所在", "Border = household at the time")}</span>{swatches}'
          f'<span class="lgi"><span class="sw gonesw" aria-hidden="true"></span>{bi("已去世（变灰）", "Dead (greyed)")}</span>'
          f'<span class="lgi"><span class="deadmark" aria-hidden="true">✕</span>{bi("死于非命", "Violent death")}</span>'
          f'<span class="lgi"><span class="sealmark" aria-hidden="true">史</span>{bi("娘家", "Born into")}</span></div>'
          f'<div class="lg" role="group" aria-label="按关系类型显示连线 / Show lines by type"><span class="lgt">{bi("连线", "Lines")}</span>{toggles}</div>')

body = f'''<svg width="0" height="0" style="position:absolute" aria-hidden="true" xmlns:xlink="http://www.w3.org/1999/xlink"><defs>{symbols([n['id'] for n in NODES])}</defs></svg>
<div class="page" id="app" data-lang="zh">
<header class="top">
  <div class="topbar">
    {SITE_MOD.nav_html('honglou')}
    <div class="langsw" role="group" aria-label="语言 / Language">
      <button type="button" data-setlang="zh" aria-pressed="true" lang="zh-CN">中文</button>
      <button type="button" data-setlang="en" aria-pressed="false" lang="en">English</button>
    </div>
  </div>
  <p class="eyebrow">{bi('清 · 曹雪芹', 'Cao Xueqin, 18th century')} <span class="gr">紅樓夢</span> {bi('一百二十回', '120 chapters')}</p>
  <h1>{bi('红楼梦人物谱', 'Who’s Who in the Dream of the Red Chamber')}</h1>
  <p class="lede">{bi(f'贾、史、王、薛四大家族，{len(NODES)} 位主子、丫鬟与过客，{len(EDGES)} 段随回目变化的关系。拖动回目，看他们相聚、相爱、离散。',
                       f'The four great families of Jinling — {len(NODES)} masters, maids and passers-by, and {len(EDGES)} relationships that change chapter by chapter. Move through the book and watch them gather, love and scatter.')}</p>
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
  {roster}
</section>

<footer class="foot">
  <p>{bi('人物、关系与回目依据一百二十回程高本系统的通行文本。前八十回是曹雪芹的原著；后四十回是程伟元、高鹗在乾隆五十六年（1791）整理刊行的续书，人物结局与前八十回的伏笔多有出入，所以页面默认只显示前八十回。判词、曲子和诗句的英文是本站自译。',
         'People, relationships and chapter numbers follow the common 120-chapter Cheng–Gao text. The first eighty chapters are Cao Xueqin’s; the last forty were published by Cheng Weiyuan and Gao E in 1791, and the fates they give the characters often differ from what the first eighty foreshadow, so the page shows only the first eighty unless you ask for more. The English versions of the verses are our own.')}</p>
  <p>{bi('小像仿清代孙温《全本红楼梦》图的工笔重彩：细线勾勒，石青、石绿、朱砂、泥金平涂；女子挽髻插簪，男子戴清代冠帽，每人配一件标志性的物件（黛玉的花锄、宝钗的金锁、晴雯撕破的扇子……）。这些都是示意图，不是孙温原画的复制。',
         'The portraits follow the gongbi manner of Sun Wen’s nineteenth-century album of the novel: fine ink outlines and flat mineral colours — azurite, malachite, cinnabar, gold. Women wear their hair in buns with pins, men wear Qing hats, and each person carries one telling object (Daiyu’s flower hoe, Baochai’s gold locket, Qingwen’s torn fan …). They are illustrations, not copies of Sun Wen’s paintings.')}</p>
</footer>
</div>
<script>const DATA = {json.dumps(DATA, ensure_ascii=False)};</script>
<script>const INTRO_HTML = {json.dumps(INTRO, ensure_ascii=False)};</script>
<script>{js}</script>
'''

size = SITE_MOD.write_page('honglou.html', '红楼梦人物谱',
                           '《红楼梦》四大家族人物关系图，可按回目查看，前八十回与后四十回分开，中英双语 · A bilingual family tree of the Dream of the Red Chamber with a chapter timeline.', css, body)
print('ok honglou', size // 1024, 'KB')
