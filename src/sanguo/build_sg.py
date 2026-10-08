# -*- coding: utf-8 -*-
"""Builds the Romance of the Three Kingdoms page (sanguo.html): the dynamic map with a chapter timeline.
The overview is a set of swimlanes (Han court and warlords, Wei, Shu, Wu) with people placed left to right by the
chapter in which they first appear; the acts of the story are marked along the top."""
import json, html, os, sys
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.dirname(HERE)
COMMON = os.path.join(SRC, 'common')
os.chdir(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, COMMON)
import dpsite as SITE_MOD  # noqa: E402
from data_sg import NODES, EDGES, EDGE_TYPES, CAMPS, LANES, ACTS, ref_zh, ref_en  # noqa: E402
from chapters_sg import CH_ZH, CH_EN  # noqa: E402
from portraits_sg import symbols  # noqa: E402

esc = html.escape
bi = SITE_MOD.bi
NODE = {n['id']: n for n in NODES}
LAST = 120

# ---------------------------------------------------------------- the time axis
W = 1280
X0, X1 = 104, 1252            # chapter 1 .. 120; the gutter on the left holds the lane names
debuts = Counter()
for n in NODES:
    debuts[next(i for i, a in enumerate(ACTS) if a['a'] <= n['debut'] <= a['b'])] += 1
shares = [0.5 / len(ACTS) + 0.5 * debuts[i] / len(NODES) for i in range(len(ACTS))]
f = 0.0
for a, s in zip(ACTS, shares):
    a['f0'], a['f1'] = round(f, 5), round(f + s, 5)
    f += s
ACTS[-1]['f1'] = 1.0


def frac(c):
    for a in ACTS:
        if c <= a['b']:
            return a['f0'] + (a['f1'] - a['f0']) * ((c - a['a'] + 0.5) / (a['b'] - a['a'] + 1))
    return 1.0


def xt(c):
    return X0 + (X1 - X0) * frac(c)


# ---------------------------------------------------------------- swimlanes
TOP = 58                       # act titles above this line
ROW_H = 84
ROWS = {'qun': 3, 'wei': 3, 'shu': 3, 'wu': 2}
SP = 60                        # least distance between two portraits in one row
R_OV = 25
lane_top, y = {}, TOP
for key, _, _ in LANES:
    lane_top[key] = y
    y += ROWS[key] * ROW_H + 10
H = y + 6

OV = {}
for key, _, _ in LANES:
    people = sorted((n for n in NODES if n['lane'] == key), key=lambda n: (n['debut'], NODES.index(n)))
    last = [-1e9] * ROWS[key]
    order = list(range(ROWS[key]))
    for n in people:
        want = xt(n['debut'])
        best = min(order, key=lambda r: (max(want, last[r] + SP) - want, r))
        x = min(max(want, last[best] + SP), X1)
        last[best] = x
        OV[n['id']] = (round(x, 1), lane_top[key] + 40 + best * ROW_H)
CX, CY = 668, round(TOP + (H - TOP) / 2)
R1 = [230, 380]
R2 = min(470, (H - 40) // 2, CX - 40)


# ---------------------------------------------------------------- camps
def life_end(n):
    if n['dies']:
        return n['dies']
    last = max([p['ch'] for e in EDGES if n['id'] in (e['s'], e['t']) for p in e['phases']] + [n['debut']])
    return last


def home_camp(n):
    """The side a person belongs to in the whole-book view: their lane's kingdom if they ever served it,
    otherwise the side they spent longest on."""
    held = Counter()
    end = life_end(n)
    for j, (ch, cp) in enumerate(n['camps']):
        nxt = n['camps'][j + 1][0] if j + 1 < len(n['camps']) else end + 1
        held[cp] += max(1, nxt - ch)
    if n['lane'] != 'qun' and n['lane'] in held:
        return n['lane']
    return held.most_common(1)[0][0]


HOME = {n['id']: home_camp(n) for n in NODES}


# ---------------------------------------------------------------- svg pieces
def use(pid, extra=''):
    return f'<use xlink:href="#pt-{pid}" href="#pt-{pid}"{extra}/>'


DEAD = '<g class="dead" transform="translate(29 29)"><circle r="9"/><path d="M-3.8,-3.8 L3.8,3.8 M3.8,-3.8 L-3.8,3.8"/></g>'


def node_svg(v):
    n = NODE[v]
    x, y = OV[v]
    k = R_OV / 40
    s = (f'<g class="node camp-{HOME[v]}" data-id="{v}" tabindex="0" role="button" '
         f'transform="translate({x} {y})" aria-label="{esc(n["zh"])}">')
    s += f'<g class="pt" transform="scale({k})"><circle class="glow" r="47"/><circle class="hit" r="48"/>'
    s += '<g class="flip">' + use(v, ' x="-40" y="-40" width="80" height="80"') + '</g>'
    s += '<circle class="ring" r="40" stroke-width="3.6"/>'
    if n['death'] and n['death'][2]:          # the ✕ marks a violent death only
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
    dead = '<g class="dead" transform="translate(36 36)"><circle r="12"/><path d="M-5,-5 L5,5 M5,-5 L-5,5"/></g>' if n['death'] and n['death'][2] else ''
    inner = use(pid, ' x="-50" y="-50" width="100" height="100"')
    return (f'<svg class="{cls} camp-{HOME[pid]}" viewBox="-56 -56 112 112" width="{size}" height="{size}" aria-hidden="true">'
            f'{inner}<circle class="ring" r="50" stroke-width="{sw}"/>{dead}</svg>')


def T(zh, en, x, y, cls='', anchor='start', extra=''):
    return (f'<text class="{cls}" x="{x}" y="{y}" text-anchor="{anchor}" data-zh="{esc(zh)}" data-en="{esc(en)}"{extra}>'
            f'{esc(zh)}</text>')


deco = '<g class="deco">'
for j, (key, zh, en) in enumerate(LANES):
    y0, h = lane_top[key], ROWS[key] * ROW_H
    deco += f'<rect class="lane lane-{key}" x="6" y="{y0}" width="{W - 12}" height="{h}" rx="10"/>'
    # lane names: Chinese set vertically one character per line, English turned on its side
    cy = y0 + h / 2
    chars = list(zh.replace('·', '・'))
    zs = ''.join(f'<tspan x="34" dy="{0 if i == 0 else 19}">{esc(ch)}</tspan>' for i, ch in enumerate(chars))
    deco += (f'<text class="lname l-zh" x="34" y="{cy - (len(chars) - 1) * 9.5 + 6:.1f}" text-anchor="middle">{zs}</text>'
             f'<text class="lname l-en" x="0" y="0" text-anchor="middle" transform="translate(38 {cy:.1f}) rotate(-90)">{esc(en.upper())}</text>')
for j, a in enumerate(ACTS):
    xa, xb = X0 + (X1 - X0) * a['f0'], X0 + (X1 - X0) * a['f1']
    if j:
        deco += f'<line class="actsep" x1="{xa:.1f}" y1="{TOP - 16}" x2="{xa:.1f}" y2="{H - 4}"/>'
    mid = (xa + xb) / 2
    deco += T(a['zs'], a['es'], round(mid, 1), 24, 'act', 'middle')
    deco += T(f'{a["a"]}–{a["b"]}', f'{a["a"]}–{a["b"]}', round(mid, 1), 41, 'actch', 'middle')
deco += '</g>'
nowline = (f'<g class="nowline" style="display:none"><line x1="0" y1="{TOP - 6}" x2="0" y2="{H - 4}"/>'
           f'<rect x="-17" y="{TOP - 22}" width="34" height="18" rx="9"/><text x="0" y="{TOP - 9}" text-anchor="middle">1</text></g>')
rings = f'<g class="rings"><circle cx="{CX}" cy="{CY}" r="{R1[1] - 60}"/><circle cx="{CX}" cy="{CY}" r="{R2}"/></g>'
defs = '<defs><filter id="tl-grey"><feColorMatrix type="saturate" values="0.08"/></filter></defs>'
edges_svg = '<g class="edges">' + ''.join(edge_svg(i, e) for i, e in enumerate(EDGES)) + '</g>'
labels_svg = '<g class="labels">' + ''.join(label_svg(i, e) for i, e in enumerate(EDGES)) + '</g>'
nodes_svg = '<g class="nodes">' + ''.join(node_svg(n['id']) for n in NODES) + '</g>'
MAP = (f'<svg id="map" class="mode-ov" viewBox="0 0 {W} {H}" role="img" aria-label="三国演义人物关系图 / Romance of the Three Kingdoms character map" '
       f'xmlns:xlink="http://www.w3.org/1999/xlink">{defs}{deco}{rings}{nowline}{edges_svg}{labels_svg}{nodes_svg}</svg>')

# ---------------------------------------------------------------- timeline control
TRACK_FRAC = 0.93
acts_html = ''.join(
    f'<div class="tlact" style="flex:{(a["f1"] - a["f0"]):.5f} 1 0"><span class="tln">{bi(a["zs"], a["es"])}</span></div>'
    for a in ACTS)
TIMELINE = f'''<div class="tl" id="tl">
  <div class="tlhead">
    <button type="button" class="tlbtn tlplay" id="tl-play" aria-label="播放"><span class="ic" aria-hidden="true">▶</span></button>
    <div class="tlnow" aria-live="polite"><span class="tlch" id="tl-ch"></span><span class="tltitle" id="tl-title"></span></div>
    <button type="button" class="tlbtn tlall" id="tl-all" aria-pressed="true">{bi('全书', 'Whole book')}</button>
  </div>
  <div class="tltrack all" id="tl-track" role="slider" tabindex="0" aria-label="回目 / Chapter" aria-valuemin="1" aria-valuemax="121" aria-valuenow="121">
    <div class="tlacts" style="width:{TRACK_FRAC * 100:.0f}%">{acts_html}</div>
    <div class="tlend" style="left:{TRACK_FRAC * 100:.0f}%">{bi('全书', 'All')}</div>
    <div class="tlfill" id="tl-fill"></div>
    <div class="tlhandle" id="tl-handle"></div>
  </div>
  <div class="tlstat" id="tl-stat"></div>
</div>'''

# ---------------------------------------------------------------- roster
GROUPS = {
    'qun': ('汉室与群雄', 'The Han court and the warlords', '皇帝与朝臣、各路诸侯、方士与神医，以及南中的蛮王',
            'The emperor and his ministers, the rival lords, Daoist adepts and a physician, and the king of the south'),
    'wei': ('曹魏与司马氏', 'Wei and the Sima clan', '曹操父子与他们的谋士、将领；司马氏最终代魏建晋',
            'Cao Cao, his sons, strategists and generals; the Sima clan who finally replace Wei with Jin'),
    'shu': ('蜀汉', 'Shu Han', '刘关张、诸葛亮与五虎上将，直到后主出降', 'Liu Bei and his brothers, Zhuge Liang and the Five Tigers, down to the last surrender'),
    'wu': ('东吴', 'Wu', '孙氏三代与江东的都督、将领', 'Three generations of the Sun family and the commanders of the east'),
}


def life_line(n):
    d = n['death']
    zh = f'第{n["debut"]}回登场' + (f' · 第{n["dies"]}回{d[0]}' if d else '')
    en = f'Appears ch. {n["debut"]}' + (f' · {d[1]}, ch. {n["dies"]}' if d else '')
    return bi(zh, en)


def strip_refs(s):
    import re
    return re.sub(r' ?\((?:第[0-9、至]+回|ch\. [0-9–, ]+)\)', '', s)


roster = ''
for key, _, _ in LANES:
    zh, en, dzh, den = GROUPS[key]
    items = [n for n in NODES if n['lane'] == key]
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
dash = {'kin': '', 'mas': '10 3 2 3', 'aid': '', 'foe': '7 5', 'tie': '1.5 4.5'}
toggles = ''.join(
    f'<button class="tog t-{k}" data-type="{k}" aria-pressed="true" type="button" title="{v["desc"]}">'
    f'<svg width="34" height="10" aria-hidden="true"><line x1="2" y1="5" x2="32" y2="5" stroke-dasharray="{dash[k]}"/></svg>'
    f'{bi(v["zh"], v["en"])}<span class="tc">0</span></button>' for k, v in EDGE_TYPES.items())
swatches = ''.join(f'<span class="lgi"><span class="sw camp-{k}" aria-hidden="true"></span>{bi(v["zh"], v["en"])}</span>'
                   for k, v in CAMPS.items())
n_gone = sum(1 for n in NODES if n['dies'])
n_violent = sum(1 for n in NODES if n['death'] and n['death'][2])
n_turn = sum(1 for n in NODES if len({c for _, c in n['camps']}) > 1)
n_phase = sum(len(e['phases']) for e in EDGES)
n_changing = sum(1 for e in EDGES if len(e['phases']) > 1)

# ---------------------------------------------------------------- data for the page script
def ph(p):
    return dict(ch=p['ch'], type=p['type'], label=p['zl'], text=p['zt'], label_en=p['el'], text_en=p['et'],
                bk=ref_zh(p['ref']), bk_en=ref_en(p['ref']))


DATA = {
    'nodes': {n['id']: dict(zh=n['zh'], en=n['en'], gr=n['py'], lane=n['lane'], debut=n['debut'], dies=n['dies'],
                            death=(n['death'][0] if n['death'] else None), death_en=(n['death'][1] if n['death'] else None),
                            violent=bool(n['death'] and n['death'][2]),
                            camps=n['camps'], home=HOME[n['id']],
                            sub=n['sub'][0], sub_en=n['sub'][1], bio=n['bio'][0], bio_en=n['bio'][1],
                            icon=n['icon'][0], icon_en=n['icon'][1], ox=OV[n['id']][0], oy=OV[n['id']][1])
              for n in NODES},
    'order': [n['id'] for n in NODES],
    'edges': [dict(s=e['s'], t=e['t'], phases=[ph(p) for p in e['phases']]) for e in EDGES],
    'types': EDGE_TYPES,
    'camp': {k: dict(zh=v['zh'], en=v['en']) for k, v in CAMPS.items()},
    'acts': [dict(a=a['a'], b=a['b'], f0=a['f0'], f1=a['f1']) for a in ACTS],
    'chapters': [dict(zh=z, en=e) for z, e in zip(CH_ZH, CH_EN)],
    'trackFrac': TRACK_FRAC, 'X0': X0, 'X1': X1, 'last': LAST, 'page': 'sanguo',
    'W': W, 'H': H, 'CX': CX, 'CY': CY, 'R_OV': R_OV, 'R1': R1, 'R2': R2,
    'title': {'zh': '三国演义人物谱', 'en': 'Who’s Who in the Romance of the Three Kingdoms'},
}

starts = ''.join(f'<button class="chipbtn" type="button" data-go="{v}">{mini(v, 26, "mini")}{bi(NODE[v]["zh"], NODE[v]["en"])}</button>'
                 for v in ['caocao', 'liubei', 'zhugeliang', 'guanyu', 'sunquan', 'lvbu'])
MOMENTS = [(1, '桃园结义', 'The peach garden'), (21, '煮酒论英雄', 'Heroes over wine'), (49, '赤壁', 'Red Cliffs'),
           (77, '关羽之死', 'Guan Yu dies'), (104, '五丈原', 'Wuzhang'), (120, '三分归一', 'One realm again')]
moments = ''.join(f'<button class="chipbtn introgo" type="button" data-ch="{c}"><span class="chn">{c}</span>{bi(zh, en)}</button>'
                  for c, zh, en in MOMENTS)

INTRO = f'''<div class="intro">
  <h2>{bi('怎么看这张图', 'How to read this map')}</h2>
  <ol class="howto">
    <li>{bi('上方的滑块是全书一百二十回。拖到哪一回，图上就只剩下到那一回为止已经登场的人；去世的人变成灰色，死于非命的另加 ✕，小像边框的颜色是他此时所属的势力，连线也换成那一回的关系。按 ▶ 可以从第一回一路播放。',
            'The slider above runs through the 120 chapters. Wherever you stop it, the map shows only the people who have appeared by then; the dead turn grey (with a ✕ for those who die by violence), each portrait’s border takes the colour of the side that person is on at that moment, and every line shows the relationship as it stands in that chapter. Press ▶ to play from chapter 1.')}</li>
    <li>{bi('全景按势力分成四条横带，每个人大致排在他登场的那一回的位置；上方标着故事的九个段落。',
            'In the overview the four bands are the Han court and warlords, Wei, Shu and Wu; each person sits roughly at the chapter where they first appear, with the nine stages of the story marked along the top.')}</li>
    <li>{bi('点任何人，他就移到中央，与他（在这一回）有直接关系的人围成一圈；右边按回目列出他的经历。点连线上的字，看这段关系前后怎样变化。点图上空白处回到全景。',
            'Click anyone to bring them to the center with everyone they are connected to (as of this chapter) in a ring around them; the panel lists their life chapter by chapter. Click a line label to see how that relationship changed. Click empty space to return to the overview.')}</li>
    <li>{bi(f'图中 {len(NODES)} 人、{len(EDGES)} 段关系；其中 {n_changing} 段关系前后有变化，{n_turn} 人换过阵营。',
            f'The map has {len(NODES)} people and {len(EDGES)} relationships; {n_changing} of the relationships change over the story, and {n_turn} people change sides.')}</li>
  </ol>
  <p class="l-zh" lang="zh-CN" style="color:var(--muted);font-size:13px">从这些人开始：</p><p class="l-en" lang="en" style="color:var(--muted);font-size:13px">Start with:</p>
  <div class="starts">{starts}</div>
  <p class="l-zh" lang="zh-CN" style="color:var(--muted);font-size:13px;margin-top:12px">或者跳到这些回目：</p><p class="l-en" lang="en" style="color:var(--muted);font-size:13px;margin-top:12px">Or jump to:</p>
  <div class="starts">{moments}</div>
</div>'''

css_raw = (open(os.path.join(COMMON, 'dynamic.css'), encoding='utf-8').read()
           + open(os.path.join(COMMON, 'timeline.css'), encoding='utf-8').read()
           + open('page_sg.css', encoding='utf-8').read())
js = SITE_MOD.NAV_JS + open(os.path.join(COMMON, 'timeline.js'), encoding='utf-8').read()
css = SITE_MOD.FONTFACES + SITE_MOD.PINYIN_FACE + css_raw + SITE_MOD.NAV_CSS

legend = (f'<div class="lg"><span class="lgt">{bi("小像边框＝此时所属", "Border = side at the time")}</span>{swatches}'
          f'<span class="lgi"><span class="sw gonesw" aria-hidden="true"></span>{bi("已去世（变灰）", "Dead (greyed)")} <b>{n_gone}</b></span>'
          f'<span class="lgi"><span class="deadmark" aria-hidden="true">✕</span>{bi("死于非命", "Died a violent death")} <b>{n_violent}</b></span></div>'
          f'<div class="lg" role="group" aria-label="按关系类型显示连线 / Show lines by type"><span class="lgt">{bi("连线", "Lines")}</span>{toggles}</div>')

body = f'''<svg width="0" height="0" style="position:absolute" aria-hidden="true" xmlns:xlink="http://www.w3.org/1999/xlink"><defs>{symbols([n['id'] for n in NODES])}</defs></svg>
<div class="page" id="app" data-lang="zh">
<header class="top">
  <div class="topbar">
    {SITE_MOD.nav_html('sanguo')}
    <div class="langsw" role="group" aria-label="语言 / Language">
      <button type="button" data-setlang="zh" aria-pressed="true" lang="zh-CN">中文</button>
      <button type="button" data-setlang="en" aria-pressed="false" lang="en">English</button>
    </div>
  </div>
  <p class="eyebrow">{bi('元末明初 · 罗贯中', 'Luo Guanzhong, 14th century')} <span class="gr">三國演義</span> {bi('一百二十回', '120 chapters')}</p>
  <h1>{bi('三国演义人物谱', 'Who’s Who in the Romance of the Three Kingdoms')}</h1>
  <p class="lede">{bi(f'{len(NODES)} 位英雄、谋士与君王，{len(EDGES)} 段会随回目变化的关系。拖动回目，看他们登场、结盟、反目、死去。',
                       f'{len(NODES)} heroes, strategists and rulers, and {len(EDGES)} relationships that change as the chapters go by. Move through the book and watch them enter, ally, turn on each other and die.')}</p>
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
  <p>{bi('人物、关系与回目依据毛宗岗评本《三国演义》一百二十回。演义是小说，许多情节与正史不同，这里只讲小说里的故事。',
         'People, relationships and chapter numbers follow the 120-chapter Mao Zonggang edition of the Romance of the Three Kingdoms. The novel often departs from the historical record; this map follows the novel.')}</p>
  <p>{bi('小像仿京剧脸谱：关羽的红脸、曹操的白脸、张飞的黑十字门等依照戏曲的传统画法；没有固定脸谱的人物画作俊扮，靠髯口、盔头和服装区分，部分细节取自小说的描写。这些都是示意图，不是某个剧团的原样。',
         'The portraits are in the manner of Peking-opera face painting: Guan Yu’s red face, Cao Cao’s white face and Zhang Fei’s black cross follow stage tradition; characters without a set mask wear plain make-up and are told apart by beard, headgear and costume, some details taken from the novel. They are illustrations, not copies of any company’s designs.')}</p>
</footer>
</div>
<script>const DATA = {json.dumps(DATA, ensure_ascii=False)};</script>
<script>const INTRO_HTML = {json.dumps(INTRO, ensure_ascii=False)};</script>
<script>{js}</script>
'''

size = SITE_MOD.write_page('sanguo.html', '三国演义人物谱',
                           '《三国演义》人物关系图，可按回目查看，中英双语 · A bilingual character map of the Romance of the Three Kingdoms with a chapter timeline.', css, body)
print('ok sanguo', size // 1024, 'KB', 'H', H)
