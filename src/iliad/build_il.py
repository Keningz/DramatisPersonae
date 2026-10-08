# -*- coding: utf-8 -*-
"""Builds the Iliad page: iliad.html (artifact body) and the standalone document."""
import json, html, re, os, base64, sys
HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'odyssey'))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'common'))
import dpsite as SITE_MOD  # noqa: E402  (src/common/dpsite.py)
from data_il import NODES, EDGES, EDGE_TYPES
from data_en import book_en
from portraits_il import symbols

esc = html.escape
NODE = {n['id']: n for n in NODES}
OV = json.load(open('overview.json'))
W, H = 1100, 1000
CX, CY = 550, 500
R_OV = 30


def bi(zh, en, tag='span'):
    return f'<{tag} class="l-zh" lang="zh-CN">{zh}</{tag}><{tag} class="l-en" lang="en">{en}</{tag}>'


def use(pid, extra=''):
    return f'<use xlink:href="#pt-{pid}" href="#pt-{pid}"{extra}/>'


def ring_markup(cat, r=40, sw=3.6):
    if cat == 'demi':
        return (f'<path class="ring ring-g" d="M{-r},0 A{r},{r} 0 0 1 {r},0" stroke-width="{sw}"/>'
                f'<path class="ring ring-m" d="M{r},0 A{r},{r} 0 0 1 {-r},0" stroke-width="{sw}"/>')
    s = f'<circle class="ring" r="{r}" stroke-width="{sw}"/>'
    if cat == 'god':
        s += f'<circle class="halo" r="{r + 6.5}"/>'
    return s


DEAD = '<g class="dead" transform="translate(29 29)"><circle r="9"/><path d="M-3.8,-3.8 L3.8,3.8 M3.8,-3.8 L-3.8,3.8"/></g>'


def face(v):
    n = NODE[v]
    x = OV[v][0]
    if n['cat'] != 'god':
        return 1 if n['camp'] == 'ach' else -1
    return 1 if x < CX else -1


def node_svg(v):
    n = NODE[v]
    x, y = OV[v]
    k = R_OV / 40
    f = face(v)
    s = (f'<g class="node cat-{n["cat"]} camp-{n["camp"]}" data-id="{v}" tabindex="0" role="button" '
         f'transform="translate({x} {y})" aria-label="{esc(n["zh"])}">')
    s += f'<g class="pt" transform="scale({k})"><circle class="hit" r="48"/>'
    s += f'<g class="flip" transform="scale({f} 1)">' + use(v, ' x="-40" y="-40" width="80" height="80"') + '</g>'
    s += ring_markup(n['cat'])
    if n['dies']:
        s += DEAD
    s += '</g>'
    s += f'<text class="nm" y="{R_OV + 18}" text-anchor="middle" font-size="14">{esc(n["zh"])}</text>'
    s += f'<text class="sb" y="{R_OV + 32}" text-anchor="middle" font-size="12">{esc(n["sub"][0])}</text>'
    return s + '</g>'


def edge_svg(i, e):
    a, b = OV[e[0]], OV[e[1]]
    return f'<path class="edge t-{e[2]}" data-e="{i}" d="M{a[0]},{a[1]} L{b[0]},{b[1]}"/>'


def label_svg(i, e):
    return (f'<g class="elab t-{e[2]}" data-e="{i}" tabindex="-1" role="button">'
            f'<rect x="0" y="0" width="10" height="21" rx="10.5"/><text x="0" y="0" text-anchor="middle"></text></g>')


def mini(pid, size, cls='mini'):
    n = NODE[pid]
    sw = 7 if size < 50 else 5
    inner = use(pid, ' x="-50" y="-50" width="100" height="100"')
    ring = ring_markup(n['cat'], 50, sw).replace(f'r="{56.5}"', 'r="55.5"')
    dead = '<g class="dead" transform="translate(36 36)"><circle r="12"/><path d="M-5,-5 L5,5 M5,-5 L-5,5"/></g>' if n['dies'] else ''
    return (f'<svg class="{cls} cat-{n["cat"]}" viewBox="-56 -56 112 112" width="{size}" height="{size}" aria-hidden="true">'
            f'{inner}{ring}{dead}</svg>')


def T(zh, en, x, y, cls='', anchor='start'):
    return (f'<text class="{cls}" x="{x}" y="{y}" text-anchor="{anchor}" data-zh="{esc(zh)}" data-en="{esc(en)}">{esc(zh)}</text>')


deco = ('<g class="deco">'
        + T('奥林波斯', 'OLYMPUS', CX, 34, 'camp', 'middle') + T('ΟΛΥΜΠΟΣ', 'ΟΛΥΜΠΟΣ', CX, 52, 'gk', 'middle')
        + T('← 偏向希腊的神', '← Gods for the Greeks', 70, 44, '', 'start')
        + T('偏向特洛伊的神 →', 'Gods for Troy →', 1030, 44, '', 'end')
        + '<line x1="70" y1="292" x2="1030" y2="292"/>'
        + T('希腊联军', 'THE GREEKS', 70, 318, 'camp', 'start') + T('ΑΧΑΙΟΙ', 'ΑΧΑΙΟΙ', 70, 336, 'gk', 'start')
        + T('特洛伊一方', 'TROY & ALLIES', 1030, 318, 'camp', 'end') + T('ΤΡΩΕΣ', 'ΤΡΩΕΣ', 1030, 336, 'gk', 'end')
        + '<line x1="550" y1="310" x2="550" y2="960" stroke-dasharray="3 8"/>'
        + T('特洛伊平原', 'THE TROJAN PLAIN', CX, 986, '', 'middle')
        + '</g>')
rings = f'<g class="rings"><circle cx="{CX}" cy="{CY}" r="300"/><circle cx="{CX}" cy="{CY}" r="455"/></g>'
edges_svg = '<g class="edges">' + ''.join(edge_svg(i, e) for i, e in enumerate(EDGES)) + '</g>'
labels_svg = '<g class="labels">' + ''.join(label_svg(i, e) for i, e in enumerate(EDGES)) + '</g>'
nodes_svg = '<g class="nodes">' + ''.join(node_svg(n['id']) for n in NODES) + '</g>'
MAP = (f'<svg id="map" class="mode-ov" viewBox="0 0 {W} {H}" role="img" aria-label="伊利亚特人物关系图 / Iliad character map" '
       f'xmlns:xlink="http://www.w3.org/1999/xlink">{deco}{rings}{edges_svg}{labels_svg}{nodes_svg}</svg>')

# ---------------------------------------------------------------- roster
CAMP = {'ach': ('希腊联军', 'The Greeks'), 'troy': ('特洛伊一方', 'Troy and its allies'), 'neutral': ('中立', 'Neutral')}
groups = [
    ('gods', '众神', 'The gods', '按荷马的安排分列两边：赫拉、雅典娜、波塞冬等帮希腊，阿波罗、阿佛洛狄忒、阿瑞斯等帮特洛伊，宙斯居中裁决',
     'Split as Homer arranges them: Hera, Athena, Poseidon and others for the Greeks; Apollo, Aphrodite, Ares and others for Troy; Zeus above both',
     [n for n in NODES if n['cat'] == 'god']),
    ('ach', '希腊联军', 'The Greeks', '围攻特洛伊的亚该亚人，营地扎在海边船旁', 'The Achaeans besieging Troy, camped by their ships on the shore',
     [n for n in NODES if n['cat'] != 'god' and n['camp'] == 'ach']),
    ('troy', '特洛伊一方', 'Troy and its allies', '特洛伊王室、守城将士、吕基亚等盟军，以及特洛阿德的百姓', 'The royal house, its defenders, Lycian and other allies, and people of the Troad',
     [n for n in NODES if n['cat'] != 'god' and n['camp'] == 'troy']),
]
CROSS = SITE_MOD.cross_for('iliad')


def xtags(v):
    return SITE_MOD.xtags(CROSS.get(v, []))


roster = ''
for key, zh, en, dzh, den, items in groups:
    roster += (f'<div class="rgroup"><h3>{bi(zh, en)}<span class="cnt">{len(items)}</span>'
               f'<span class="rdesc">{bi(dzh, den)}</span></h3><div class="rgrid">')
    for n in items:
        v = n['id']
        roster += (f'<button class="rcard" data-id="{v}" type="button">{mini(v, 64, "rp")}'
                   f'<span class="rtext"><span class="rname">{bi(esc(n["zh"]), esc(n["en"]))}<span class="rgr">{esc(n["gr"])}</span>{xtags(v)}</span>'
                   f'<span class="rsub">{bi(esc(n["sub"][0]), esc(n["sub"][1]))}</span>'
                   f'<span class="rbio">{bi(esc(n["bio"][0]), esc(n["bio"][1]))}</span></span></button>')
    roster += '</div></div>'

counts = {k: sum(1 for e in EDGES if e[2] == k) for k in EDGE_TYPES}
dash = {'kin': '', 'aid': '', 'foe': '7 5', 'tie': '1.5 4.5'}
toggles = ''.join(
    f'<button class="tog t-{k}" data-type="{k}" aria-pressed="true" type="button" title="{v["desc"]}">'
    f'<svg width="34" height="10" aria-hidden="true"><line x1="2" y1="5" x2="32" y2="5" stroke-dasharray="{dash[k]}"/></svg>'
    f'{bi(v["zh"], v["en"])}<span class="tc">{counts[k]}</span></button>' for k, v in EDGE_TYPES.items())

n_god = sum(1 for n in NODES if n['cat'] == 'god')
n_demi = sum(1 for n in NODES if n['cat'] == 'demi')
n_mor = len(NODES) - n_god - n_demi
n_dead = sum(1 for n in NODES if n['dies'])

DATA = {
    'nodes': {n['id']: dict(zh=n['zh'], en=n['en'], gr=n['gr'], cat=n['cat'], camp=n['camp'],
                            dies=n['dies'], dies_en=book_en(n['dies']) if n['dies'] else None,
                            sub=n['sub'][0], sub_en=n['sub'][1], bio=n['bio'][0], bio_en=n['bio'][1],
                            icon=n['icon'][0], icon_en=n['icon'][1], ox=OV[n['id']][0], oy=OV[n['id']][1], f=face(n['id']))
              for n in NODES},
    'order': [n['id'] for n in NODES],
    'edges': [dict(s=e[0], t=e[1], type=e[2], label=e[3], text=e[4], label_en=e[5], text_en=e[6],
                   bk=e[7], bk_en=book_en(e[7])) for e in EDGES],
    'types': EDGE_TYPES,
    'camp': {k: dict(zh=v[0], en=v[1]) for k, v in CAMP.items()},
    'cat': {'zh': {'god': '神', 'demi': '半神', 'mortal': '凡人'}, 'en': {'god': 'God', 'demi': 'Demigod', 'mortal': 'Mortal'}},
    'W': W, 'H': H, 'CX': CX, 'CY': CY, 'R_OV': R_OV, 'cross': CROSS, 'R1': [240, 320], 'R2': 455,
    'title': {'zh': '伊利亚特人物谱', 'en': 'Who’s Who in the Iliad'},
}

starts = ''.join(f'<button class="chipbtn" type="button" data-go="{v}">{mini(v, 26, "mini")}{bi(NODE[v]["zh"], NODE[v]["en"])}</button>'
                 for v in ['achilles', 'hector', 'helen', 'zeus', 'patroclus', 'priam'])

INTRO = f'''<div class="intro">
  <h2>{bi('怎么看这张图', 'How to read this map')}</h2>
  <ol class="howto">
    <li>{bi('全景按战场排开：上方是众神，左边希腊联军，右边特洛伊一方；众神也按偏向分在两侧。',
            'The overview is laid out like the battlefield: gods above, the Greeks on the left, Troy on the right; the gods stand on the side they favor.')}</li>
    <li>{bi('点任何人，他就移到中央，与他有直接关系的人围成一圈，每条线写着关系；其余人物退到外圈，点一下即可换成主角。',
            'Click anyone and they move to the center, with everyone directly connected to them in a ring and each line labeled; everyone else moves to the outer ring, one click away.')}</li>
    <li>{bi('点连线上的字看这段关系的原委与卷数；点图上空白处或“全景”按钮，回到战场布局。',
            'Click a line label for the story and the book it comes from; click an empty part of the map, or the Overview button, to return to the battlefield.')}</li>
  </ol>
  <p class="l-zh" lang="zh-CN" style="color:var(--muted);font-size:13px">从这些人开始：</p><p class="l-en" lang="en" style="color:var(--muted);font-size:13px">Start with:</p>
  <div class="starts">{starts}</div>
</div>'''

COMMON = os.path.join(os.path.dirname(HERE), 'common')
css_raw = open(os.path.join(COMMON, 'dynamic.css'), encoding='utf-8').read()
js = SITE_MOD.NAV_JS + open(os.path.join(COMMON, 'dynamic.js'), encoding='utf-8').read()

css = SITE_MOD.FONTFACES + css_raw + SITE_MOD.NAV_CSS

body = f'''<svg width="0" height="0" style="position:absolute" aria-hidden="true" xmlns:xlink="http://www.w3.org/1999/xlink"><defs>{symbols()}</defs></svg>
<div class="page" id="app" data-lang="zh">
<header class="top">
  <div class="topbar">
    {SITE_MOD.nav_html('iliad')}
    <div class="langsw" role="group" aria-label="语言 / Language">
      <button type="button" data-setlang="zh" aria-pressed="true" lang="zh-CN">中文</button>
      <button type="button" data-setlang="en" aria-pressed="false" lang="en">English</button>
    </div>
  </div>
  <p class="eyebrow">{bi('荷马史诗', 'Homer')} <span class="gr">ΙΛΙΑΣ</span> {bi('二十四卷', '24 books')}</p>
  <h1>{bi('伊利亚特人物谱', 'Who’s Who in the Iliad')}</h1>
  <p class="lede">{bi(f'{len(NODES)} 位神与凡人、{len(EDGES)} 段关系。没有固定的主角：点谁，谁就走到中央，与他相关的人围成一圈。',
                       f'{len(NODES)} gods and mortals, {len(EDGES)} relationships, and no fixed hero: click anyone and they step into the center, with everyone connected to them gathered around.')}</p>
  <div class="legend">
    <div class="lg"><span class="lgt">{bi('小像边框', 'Border')}</span>
      <span class="lgi">{mini('zeus', 26, 'lgp')}{bi('神', 'God')} <b>{n_god}</b></span>
      <span class="lgi">{mini('achilles', 26, 'lgp')}{bi('半神（神与凡人之子）', 'Demigod (child of a god)')} <b>{n_demi}</b></span>
      <span class="lgi">{mini('priam', 26, 'lgp')}{bi('凡人', 'Mortal')} <b>{n_mor}</b></span>
      <span class="lgi"><span class="deadmark" aria-hidden="true">✕</span>{bi('死于本诗', 'Dies in the poem')} <b>{n_dead}</b></span>
    </div>
    <div class="lg" role="group" aria-label="按关系类型显示连线 / Show lines by type"><span class="lgt">{bi('连线', 'Lines')}</span>{toggles}</div>
  </div>
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
    <div class="mapscroll" id="mapscroll">{MAP}</div>
  </div>
  <aside class="panel" id="panel" aria-live="polite">{INTRO}</aside>
</section>

<section class="roster" id="roster">
  <h2>{bi('人物一览', 'All characters')}</h2>
  {roster}
</section>

<footer class="foot">
  <p>{bi('关系与细节依据荷马《伊利亚特》，“卷”指全诗二十四卷的分卷，各译本分卷一致。众神的阵营依卷二十的安排。',
         'Relationships and details follow Homer’s Iliad. “Book” refers to the poem’s 24 books, numbered the same in every translation. The gods’ sides follow the line-up in Book 20.')}</p>
  <p>{bi('小像是仿古希腊红绘陶瓶画的示意图，不是古代原作。', 'The portraits are illustrations in the manner of Greek red-figure vase painting, not copies of ancient works.')}</p>
</footer>
</div>
<script>const DATA = {json.dumps(DATA, ensure_ascii=False)};</script>
<script>const INTRO_HTML = {json.dumps(INTRO, ensure_ascii=False)};</script>
<script>{js}</script>
'''

size = SITE_MOD.write_page('iliad.html', '伊利亚特人物谱',
                           '荷马《伊利亚特》人物关系图，中英双语 · A bilingual, interactive character map of Homer’s Iliad.', css, body)
print('ok iliad', size // 1024, 'KB')
