# -*- coding: utf-8 -*-
"""Builds the Aeneid page (aeneid.html) on the shared dynamic-map engine (src/common/dynamic.js)."""
import json, html, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.dirname(HERE)
COMMON = os.path.join(SRC, 'common')
os.chdir(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(SRC, 'odyssey'))
sys.path.insert(0, COMMON)
import dpsite as SITE_MOD  # noqa: E402
from data_ae import NODES, EDGES, EDGE_TYPES  # noqa: E402
from data_en import book_en  # noqa: E402
from portraits_ae import symbols  # noqa: E402

esc = html.escape
bi = SITE_MOD.bi
NODE = {n['id']: n for n in NODES}
OV = json.load(open('overview.json'))
W, H = 1150, 1020
CX, CY = 575, 520
R_OV = 30
HUB = 'aeneas'
K_HUB = 42 / 40


def roman(la):
    """Latin name in inscriptional capitals: Iuppiter -> IVPPITER."""
    return la.upper().replace('U', 'V')


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
    """Overview: everyone faces the middle of the map."""
    return 1 if OV[v][0] < CX else -1


def node_svg(v):
    n = NODE[v]
    x, y = OV[v]
    k = K_HUB if v == HUB else R_OV / 40
    s = (f'<g class="node cat-{n["cat"]} camp-{n["camp"]}" data-id="{v}" tabindex="0" role="button" '
         f'transform="translate({x} {y})" aria-label="{esc(n["zh"])}">')
    s += f'<g class="pt" transform="scale({k})"><circle class="hit" r="48"/>'
    s += f'<g class="flip" transform="scale({face(v)} 1)">' + use(v, ' x="-40" y="-40" width="80" height="80"') + '</g>'
    s += ring_markup(n['cat'])
    if n['dies']:
        s += DEAD
    s += '</g>'
    s += f'<text class="nm" y="{40 * k + 18}" text-anchor="middle" font-size="14">{esc(n["zh"])}</text>'
    s += f'<text class="sb" y="{40 * k + 32}" text-anchor="middle" font-size="12">{esc(n["sub"][0])}</text>'
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
    dead = '<g class="dead" transform="translate(36 36)"><circle r="12"/><path d="M-5,-5 L5,5 M5,-5 L-5,5"/></g>' if n['dies'] else ''
    return (f'<svg class="{cls} cat-{n["cat"]}" viewBox="-56 -56 112 112" width="{size}" height="{size}" aria-hidden="true">'
            f'{inner}{ring_markup(n["cat"], 50, sw)}{dead}</svg>')


def T(zh, en, x, y, cls='', anchor='start'):
    return f'<text class="{cls}" x="{x}" y="{y}" text-anchor="{anchor}" data-zh="{esc(zh)}" data-en="{esc(en)}">{esc(zh)}</text>'


deco = ('<g class="deco">'
        + T('众神', 'THE GODS', CX, 34, 'camp', 'middle') + T('DEI', 'DEI', CX, 52, 'gk', 'middle')
        + T('← 护佑埃涅阿斯的神', '← Gods who favor Aeneas', 70, 44, '', 'start')
        + T('阻挠特洛伊人的神 →', 'Powers against the Trojans →', 1080, 44, '', 'end')
        + '<line x1="70" y1="296" x2="1080" y2="296"/>'
        + T('特洛伊陷落', 'THE FALL OF TROY', 70, 334, 'camp', 'start') + T('TROIA · 卷二', 'TROIA · BOOK 2', 70, 352, 'gk', 'start')
        + T('意大利', 'ITALY', 1080, 334, 'camp', 'end') + T('ITALIA · 卷七至十二', 'ITALIA · BOOKS 7–12', 1080, 352, 'gk', 'end')
        + T('海上漂泊', 'THE VOYAGE', 70, 724, 'camp', 'start') + T('卷三、卷五', 'BOOKS 3, 5', 70, 742, 'gk', 'start')
        + T('迦太基与冥府', 'CARTHAGE & UNDERWORLD', 478, 770, 'camp', 'start')
        + T('CARTHAGO · 卷一、四、六', 'CARTHAGO · BOOKS 1, 4, 6', 478, 788, 'gk', 'start')
        + '</g>')
rings = f'<g class="rings"><circle cx="{CX}" cy="{CY}" r="300"/><circle cx="{CX}" cy="{CY}" r="455"/></g>'
edges_svg = '<g class="edges">' + ''.join(edge_svg(i, e) for i, e in enumerate(EDGES)) + '</g>'
labels_svg = '<g class="labels">' + ''.join(label_svg(i, e) for i, e in enumerate(EDGES)) + '</g>'
nodes_svg = '<g class="nodes">' + ''.join(node_svg(n['id']) for n in NODES) + '</g>'
MAP = (f'<svg id="map" class="mode-ov" viewBox="0 0 {W} {H}" role="img" aria-label="埃涅阿斯纪人物关系图 / Aeneid character map" '
       f'xmlns:xlink="http://www.w3.org/1999/xlink">{deco}{rings}{edges_svg}{labels_svg}{nodes_svg}</svg>')

# ---------------------------------------------------------------- roster
CAMP = {'pro': ('护佑埃涅阿斯', 'Favors Aeneas'), 'contra': ('阻挠特洛伊人', 'Against the Trojans'),
        'neutral': ('居中裁决', 'Above the fray'), 'troy': ('特洛伊人', 'Trojans'), 'greek': ('希腊人', 'Greeks'),
        'carthage': ('迦太基', 'Carthage'), 'cumae': ('库迈', 'Cumae'), 'arcadia': ('阿卡迪亚人 · 埃涅阿斯的盟友', 'Arcadians, allies of Aeneas'),
        'italy': ('意大利诸族', 'Peoples of Italy')}
groups = [
    ('gods', '众神', 'The gods', '朱诺与维纳斯各护一方，朱庇特执掌命运；罗马神名后标出对应的希腊神',
     'Juno and Venus each fight for their own, while Jupiter holds the scales of fate. Roman names; the Greek equivalents are linked',
     [n for n in NODES if n['cat'] == 'god']),
    ('troy', '特洛伊人', 'The Trojans', '埃涅阿斯一家、特洛伊城中的人，以及随他到意大利的同伴',
     'Aeneas and his family, the people of Troy, and the companions who follow him to Italy',
     [n for n in NODES if n['cat'] != 'god' and n['camp'] == 'troy']),
    ('greek', '希腊人', 'The Greeks', '攻陷特洛伊的人，和在路上遇到的希腊人', 'Those who sacked Troy, and Greeks met on the way',
     [n for n in NODES if n['camp'] == 'greek']),
    ('carthage', '迦太基与库迈', 'Carthage and Cumae', '狄多的城，与通往冥府的入口', 'Dido’s city, and the entrance to the underworld',
     [n for n in NODES if n['camp'] in ('carthage', 'cumae')]),
    ('italy', '意大利', 'Italy', '阿卡迪亚盟友，与拉丁人、鲁图利人、伊特鲁里亚人等对手', 'Arcadian allies, and the Latins, Rutulians, Etruscans and others who oppose Aeneas',
     [n for n in NODES if n['camp'] in ('arcadia', 'italy')]),
    ('monsters', '怪物', 'Monsters', '复仇女神、独眼巨人与鸟身女妖', 'A Fury, the Cyclops and the Harpy',
     [n for n in NODES if n['cat'] == 'monster']),
]
assert sum(len(g[5]) for g in groups) == len(NODES)
CROSS = SITE_MOD.cross_for('aeneid')


def xtags(v):
    return SITE_MOD.xtags(CROSS.get(v, []))


roster = ''
for key, zh, en, dzh, den, items in groups:
    roster += (f'<div class="rgroup"><h3>{bi(zh, en)}<span class="cnt">{len(items)}</span>'
               f'<span class="rdesc">{bi(dzh, den)}</span></h3><div class="rgrid">')
    for n in items:
        v = n['id']
        roster += (f'<button class="rcard" data-id="{v}" type="button">{mini(v, 64, "rp")}'
                   f'<span class="rtext"><span class="rname">{bi(esc(n["zh"]), esc(n["en"]))}<span class="rgr">{esc(roman(n["la"]))}</span>{xtags(v)}</span>'
                   f'<span class="rsub">{bi(esc(n["sub"][0]), esc(n["sub"][1]))}</span>'
                   f'<span class="rbio">{bi(esc(n["bio"][0]), esc(n["bio"][1]))}</span></span></button>')
    roster += '</div></div>'

counts = {k: sum(1 for e in EDGES if e[2] == k) for k in EDGE_TYPES}
dash = {'kin': '', 'aid': '', 'foe': '7 5', 'tie': '1.5 4.5'}
toggles = ''.join(
    f'<button class="tog t-{k}" data-type="{k}" aria-pressed="true" type="button" title="{v["desc"]}">'
    f'<svg width="34" height="10" aria-hidden="true"><line x1="2" y1="5" x2="32" y2="5" stroke-dasharray="{dash[k]}"/></svg>'
    f'{bi(v["zh"], v["en"])}<span class="tc">{counts[k]}</span></button>' for k, v in EDGE_TYPES.items())

n_cat = {c: sum(1 for n in NODES if n['cat'] == c) for c in ('god', 'demi', 'mortal', 'monster')}
n_dead = sum(1 for n in NODES if n['dies'])

DATA = {
    'nodes': {n['id']: dict(zh=n['zh'], en=n['en'], gr=roman(n['la']), cat=n['cat'], camp=n['camp'],
                            dies=n['dies'], dies_en=book_en(n['dies']) if n['dies'] else None,
                            sub=n['sub'][0], sub_en=n['sub'][1], bio=n['bio'][0], bio_en=n['bio'][1],
                            icon=n['icon'][0], icon_en=n['icon'][1], ox=OV[n['id']][0], oy=OV[n['id']][1],
                            f=face(n['id']), **({'ok': K_HUB} if n['id'] == HUB else {}))
              for n in NODES},
    'order': [n['id'] for n in NODES],
    'edges': [dict(s=e[0], t=e[1], type=e[2], label=e[3], text=e[4], label_en=e[5], text_en=e[6],
                   bk=e[7], bk_en=book_en(e[7])) for e in EDGES],
    'types': EDGE_TYPES,
    'camp': {k: dict(zh=v[0], en=v[1]) for k, v in CAMP.items()},
    'cat': {'zh': {'god': '神', 'demi': '半神', 'mortal': '凡人', 'monster': '怪物'},
            'en': {'god': 'God', 'demi': 'Demigod', 'mortal': 'Mortal', 'monster': 'Monster'}},
    'W': W, 'H': H, 'CX': CX, 'CY': CY, 'R_OV': R_OV, 'cross': CROSS, 'R1': [240, 380], 'R2': 455,
    'title': {'zh': '埃涅阿斯纪人物谱', 'en': 'Who’s Who in the Aeneid'},
}

starts = ''.join(f'<button class="chipbtn" type="button" data-go="{v}">{mini(v, 26, "mini")}{bi(NODE[v]["zh"], NODE[v]["en"])}</button>'
                 for v in ['aeneas', 'dido', 'turnus', 'juno', 'venus', 'anchises'])

INTRO = f'''<div class="intro">
  <h2>{bi('怎么看这张图', 'How to read this map')}</h2>
  <ol class="howto">
    <li>{bi('全景按故事排开：上方是众神，左边护佑埃涅阿斯、右边与他作对；下方从左到右是特洛伊陷落、海上漂泊、迦太基与冥府、意大利的战争，埃涅阿斯一家在中间。',
            'The overview follows the story: gods above, those who help Aeneas on the left and those against him on the right; below, from left to right, the fall of Troy, the voyage, Carthage and the underworld, and the war in Italy, with Aeneas and his family in the middle.')}</li>
    <li>{bi('点任何人，他就移到中央，与他有直接关系的人围成一圈，每条线写着关系；其余人物退到外圈，点一下即可换成主角。',
            'Click anyone and they move to the center, with everyone directly connected to them in a ring and each line labeled; everyone else moves to the outer ring, one click away.')}</li>
    <li>{bi('点连线上的字看这段关系的原委与卷数；点图上空白处或“全景”按钮，回到故事布局。维吉尔用罗马神名，人物卡里链接到荷马史诗中的同一位神。',
            'Click a line label for the story and the book it comes from; click an empty part of the map, or the Overview button, to return to the story layout. Virgil uses the Roman names of the gods; each card links to the same god in Homer.')}</li>
  </ol>
  <p class="l-zh" lang="zh-CN" style="color:var(--muted);font-size:13px">从这些人开始：</p><p class="l-en" lang="en" style="color:var(--muted);font-size:13px">Start with:</p>
  <div class="starts">{starts}</div>
</div>'''

css_raw = open(os.path.join(COMMON, 'dynamic.css'), encoding='utf-8').read() + open('page_ae.css', encoding='utf-8').read()
js = SITE_MOD.NAV_JS + open(os.path.join(COMMON, 'dynamic.js'), encoding='utf-8').read()
css = SITE_MOD.FONTFACES + css_raw + SITE_MOD.NAV_CSS

legend_items = (f'<span class="lgi">{mini("jupiter", 26, "lgp")}{bi("神", "God")} <b>{n_cat["god"]}</b></span>'
                f'<span class="lgi">{mini("aeneas", 26, "lgp")}{bi("半神（神或仙女之子）", "Demigod (child of a god or nymph)")} <b>{n_cat["demi"]}</b></span>'
                f'<span class="lgi">{mini("dido", 26, "lgp")}{bi("凡人", "Mortal")} <b>{n_cat["mortal"]}</b></span>'
                f'<span class="lgi">{mini("allecto", 26, "lgp")}{bi("怪物", "Monster")} <b>{n_cat["monster"]}</b></span>'
                f'<span class="lgi"><span class="deadmark" aria-hidden="true">✕</span>{bi("死于本诗", "Dies in the poem")} <b>{n_dead}</b></span>')

body = f'''<svg width="0" height="0" style="position:absolute" aria-hidden="true" xmlns:xlink="http://www.w3.org/1999/xlink"><defs>{symbols([(n['id'], n['style']) for n in NODES])}</defs></svg>
<div class="page" id="app" data-lang="zh">
<header class="top">
  <div class="topbar">
    {SITE_MOD.nav_html('aeneid')}
    <div class="langsw" role="group" aria-label="语言 / Language">
      <button type="button" data-setlang="zh" aria-pressed="true" lang="zh-CN">中文</button>
      <button type="button" data-setlang="en" aria-pressed="false" lang="en">English</button>
    </div>
  </div>
  <p class="eyebrow">{bi('维吉尔', 'Virgil')} <span class="gr">AENEIS</span> {bi('十二卷', '12 books')}</p>
  <h1>{bi('埃涅阿斯纪人物谱', 'Who’s Who in the Aeneid')}</h1>
  <p class="lede">{bi(f'{len(NODES)} 位神、凡人与怪物，{len(EDGES)} 段关系。从特洛伊的火光到拉丁姆的决斗：点谁，谁就走到中央，与他相关的人围成一圈。',
                       f'{len(NODES)} gods, mortals and monsters, {len(EDGES)} relationships, from the flames of Troy to the last duel in Latium. Click anyone and they step into the center, with everyone connected to them gathered around.')}</p>
  <div class="legend">
    <div class="lg"><span class="lgt">{bi('小像边框', 'Border')}</span>{legend_items}</div>
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
  <p>{bi('关系与细节依据维吉尔《埃涅阿斯纪》，“卷”指全诗十二卷的分卷，各译本分卷一致。卷二中海伦的一段（2.567–588）仅见于古代注疏，真伪存疑。',
         'Relationships and details follow Virgil’s Aeneid. “Book” refers to the poem’s twelve books, numbered the same in every translation. The Helen passage in Book 2 (2.567–588) survives only through an ancient commentator and may not be Virgil’s.')}</p>
  <p>{bi('小像是仿庞贝壁画风格的示意图，不是古代原作：神以庞贝红为底、带淡色光轮，凡人以绿为底，怪物以赭黄为底，亡魂以灰蓝淡彩绘出。',
         'The portraits are illustrations in the manner of Roman wall painting from Pompeii, not copies of ancient works: gods on Pompeian red with a pale nimbus, mortals on green, monsters on yellow ochre, and ghosts in pale grey-blue.')}</p>
</footer>
</div>
<script>const DATA = {json.dumps(DATA, ensure_ascii=False)};</script>
<script>const INTRO_HTML = {json.dumps(INTRO, ensure_ascii=False)};</script>
<script>{js}</script>
'''

size = SITE_MOD.write_page('aeneid.html', '埃涅阿斯纪人物谱',
                           '维吉尔《埃涅阿斯纪》人物关系图，中英双语 · A bilingual, interactive character map of Virgil’s Aeneid.', css, body)
print('ok aeneid', size // 1024, 'KB')
