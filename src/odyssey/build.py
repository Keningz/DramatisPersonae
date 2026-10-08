# -*- coding: utf-8 -*-
"""Builds the bilingual page: odyssey.html (artifact body) and the standalone full document."""
import json, html, re, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'common'))
import dpsite as SITE_MOD  # noqa: E402  (src/common/dpsite.py)
from data import NODES, EDGES, EDGE_TYPES
from data_en import NODE_EN, EDGE_EN, TYPE_EN, book_en
from portraits import symbols
from layout import build_geometry, FONT, W, H, CX, CY, A, B

NODE = {n['id']: n for n in NODES}
styles = {n['id']: n['style'] for n in NODES}
esc = html.escape

GEO = {
    'zh': build_geometry('zh'),
    'en': build_geometry('en', lambda v: NODE[v]['en'], lambda v: NODE_EN[v][0], lambda i: EDGE_EN[i][0]),
}
POS = {g['id']: g for g in GEO['zh'][0]}
CAT = {'zh': {'god': '神', 'mortal': '凡人', 'monster': '怪物'},
       'en': {'god': 'God', 'mortal': 'Mortal', 'monster': 'Monster'}}


def name(v, L):
    return NODE[v]['zh'] if L == 'zh' else NODE[v]['en']


def sub(v, L):
    return NODE[v]['sub'] if L == 'zh' else NODE_EN[v][0]


def bi(zh, en, tag='span'):
    return f'<{tag} class="l-zh" lang="zh-CN">{zh}</{tag}><{tag} class="l-en" lang="en">{en}</{tag}>'


def use(pid, extra=''):
    return f'<use xlink:href="#pt-{pid}" href="#pt-{pid}"{extra}/>'


# ---------------------------------------------------------------- map svg
def node_svg(g):
    v = g['id']
    n = NODE[v]
    x, y, r = g['x'], g['y'], g['r']
    flip = g['face'] == 'left'
    tf = f'translate({x + r:.1f} {y - r:.1f}) scale(-1 1)' if flip else f'translate({x - r:.1f} {y - r:.1f})'
    ringw = 5 if v == 'odysseus' else 3.6
    s = (f'<g class="node cat-{n["cat"]}" data-id="{v}" tabindex="0" role="button" '
         f'aria-label="{esc(n["zh"])}，{CAT["zh"][n["cat"]]}，{esc(n["sub"])}">')
    s += f'<circle class="hit" cx="{x}" cy="{y}" r="{r + 8}"/>'
    if n['cat'] == 'god':
        s += f'<circle class="halo" cx="{x}" cy="{y}" r="{r + 6.5}"/>'
    s += use(v, f' width="{2 * r}" height="{2 * r}" transform="{tf}"')
    s += f'<circle class="ring" cx="{x}" cy="{y}" r="{r}" stroke-width="{ringw}"/>'
    for L in ('zh', 'en'):
        g2 = next(q for q in GEO[L][0] if q['id'] == v)
        lab = g2['lab']
        F = FONT[L]
        fs1, fs2 = (F['big_name'], F['big_sub']) if v == 'odysseus' else (F['name'], F['sub'])
        s += f'<g class="l-{L}">'
        s += (f'<text class="nm" x="{lab["x"]:.1f}" y="{lab["y"]:.1f}" text-anchor="{lab["anchor"]}" '
              f'font-size="{fs1}">{esc(name(v, L))}</text>')
        s += (f'<text class="sb" x="{lab["x"]:.1f}" y="{lab["y"] + fs1 - 1:.1f}" text-anchor="{lab["anchor"]}" '
              f'font-size="{fs2}">{esc(sub(v, L))}</text>')
        s += '</g>'
    return s + '</g>'


def edge_svg(i, e):
    return (f'<g class="edge t-{e["type"]}" data-e="{i}">'
            f'<path class="ln" d="{e["d"]}"/><path class="eh" d="{e["d"]}"/></g>')


def label_svg(i, e, L):
    lb = e['lab']
    x0, y0 = lb['lx'] - lb['lw'] / 2, lb['ly'] - lb['lh'] / 2
    fs = FONT[L]['edge']
    a, b = name(e['s'], L), name(e['t'], L)
    aria = f'{a}与{b}：{lb["text"]}' if L == 'zh' else f'{a} and {b}: {lb["text"]}'
    return (f'<g class="elab t-{e["type"]}" data-e="{i}" tabindex="0" role="button" aria-label="{esc(aria)}">'
            f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{lb["lw"]:.1f}" height="{lb["lh"]}" rx="{lb["lh"] / 2}"/>'
            f'<text x="{lb["lx"]:.1f}" y="{lb["ly"] + 4.5:.1f}" text-anchor="middle" font-size="{fs}">{esc(lb["text"])}</text></g>')


def mini(pid, size, cls='mini'):
    n = NODE[pid]
    return (f'<svg class="{cls} cat-{n["cat"]}" viewBox="-6 -6 112 112" width="{size}" height="{size}" aria-hidden="true">'
            + use(pid, ' width="100" height="100"')
            + f'<circle class="ring" cx="50" cy="50" r="50" stroke-width="{7 if size < 50 else 5}"/>'
            + ('<circle class="halo" cx="50" cy="50" r="55.5"/>' if n['cat'] == 'god' else '')
            + '</svg>')


geo_edges = GEO['zh'][1]
parts = [f'<ellipse class="guide" cx="{CX}" cy="{CY}" rx="{A}" ry="{B}"/>',
         '<g class="edges">' + ''.join(edge_svg(i, e) for i, e in enumerate(geo_edges)) + '</g>']
for L in ('zh', 'en'):
    parts.append(f'<g class="labels l-{L}">' + ''.join(label_svg(i, e, L) for i, e in enumerate(GEO[L][1])) + '</g>')
parts.append('<g class="nodes">' + ''.join(node_svg(g) for g in GEO['zh'][0] if g['id'] != 'odysseus')
             + node_svg(POS['odysseus']) + '</g>')
MAP_SVG = (f'<svg id="map" viewBox="0 0 {W} {H}" role="img" aria-label="奥德赛人物关系图 / Odyssey character map" '
           f'xmlns:xlink="http://www.w3.org/1999/xlink">' + ''.join(parts) + '</svg>')

# ---------------------------------------------------------------- roster
groups = [('god', '神', 'Gods', '奥林波斯众神与海岛女神', 'Olympians and island goddesses'),
          ('mortal', '凡人', 'Mortals', '伊塔卡、费埃克斯、特洛伊老战友与冥府亡魂',
           'Ithaca, the Phaeacians, old comrades from Troy, and shades in Hades'),
          ('monster', '怪物', 'Monsters', '漂泊途中的海怪与巨人', 'Monsters and a giant met on the voyage')]
CROSS = SITE_MOD.cross_for('odyssey')


def xtags(v):
    return SITE_MOD.xtags(CROSS.get(v, []))


roster = ''
for cat, zh, en, dzh, den in groups:
    items = [n for n in NODES if n['cat'] == cat]
    roster += (f'<div class="rgroup"><h3><span class="swatch sw-{cat}"></span>{bi(zh, en)}<span class="cnt">{len(items)}</span>'
               f'<span class="rdesc">{bi(dzh, den)}</span></h3><div class="rgrid">')
    for n in items:
        v = n['id']
        roster += (f'<button class="rcard" data-id="{v}" type="button">{mini(v, 64, "rp")}'
                   f'<span class="rtext"><span class="rname">{bi(esc(n["zh"]), esc(n["en"]))}<span class="rgr">{esc(n["gr"])}</span>{xtags(v)}</span>'
                   f'<span class="rsub">{bi(esc(n["sub"]), esc(NODE_EN[v][0]))}</span>'
                   f'<span class="rbio">{bi(esc(n["bio"]), esc(NODE_EN[v][1]))}</span></span></button>')
    roster += '</div></div>'

counts = {k: sum(1 for e in EDGES if e[2] == k) for k in EDGE_TYPES}
dash = {'kin': '', 'aid': '', 'foe': '7 5', 'tie': '1.5 4.5'}
toggles = ''
for k, v in EDGE_TYPES.items():
    toggles += (f'<button class="tog t-{k}" data-type="{k}" aria-pressed="true" type="button" title="{v["desc"]}">'
                f'<svg width="34" height="10" aria-hidden="true"><line x1="2" y1="5" x2="32" y2="5" '
                f'stroke-dasharray="{dash[k]}"/></svg>{bi(v["zh"], TYPE_EN[k][0])}<span class="tc">{counts[k]}</span></button>')

data_js = json.dumps({
    'nodes': {n['id']: dict(zh=n['zh'], gr=n['gr'], en=n['en'], cat=n['cat'],
                            sub=n['sub'], bio=n['bio'], icon=n['icon'],
                            sub_en=NODE_EN[n['id']][0], bio_en=NODE_EN[n['id']][1], icon_en=NODE_EN[n['id']][2],
                            x=POS[n['id']]['x']) for n in NODES},
    'edges': [dict(s=e[0], t=e[1], type=e[2], label=e[3], text=e[4], bk=e[5],
                   label_en=EDGE_EN[i][0], text_en=EDGE_EN[i][1], bk_en=book_en(e[5])) for i, e in enumerate(EDGES)],
    'types': {k: dict(zh=v['zh'], desc=v['desc'], en=TYPE_EN[k][0], desc_en=TYPE_EN[k][1]) for k, v in EDGE_TYPES.items()},
    'cat': CAT, 'cx': CX, 'w': W, 'cross': CROSS,
}, ensure_ascii=False)

css = SITE_MOD.FONTFACES + open('page.css', encoding='utf-8').read() + SITE_MOD.NAV_CSS
js = SITE_MOD.NAV_JS + open('page.js', encoding='utf-8').read()
n_god = sum(1 for n in NODES if n['cat'] == 'god')
n_mon = sum(1 for n in NODES if n['cat'] == 'monster')
n_mor = len(NODES) - n_god - n_mon

starts = ''.join(f'<button class="chipbtn" type="button" data-go="{v}">{mini(v, 26)}{bi(NODE[v]["zh"], NODE[v]["en"])}</button>'
                 for v in ['odysseus', 'penelope', 'athena', 'telemachus', 'polyphemus', 'circe'])
INTRO = f'''<div class="intro">
  <h2>{bi('怎么看这张图', 'How to read this map')}</h2>
  <ol class="howto">
    <li>{bi('奥德修斯居中，其余人物围成一圈：上方是众神，右边与下方是伊塔卡的家人、仆人和求婚者，左边是漂泊途中遇到的神怪，左下是冥府。',
            'Odysseus is at the center with everyone else in a ring: gods at the top, Ithaca’s family, servants and suitors on the right and along the bottom, the gods and monsters of the voyage on the left, and Hades at the lower left.')}</li>
    <li>{bi('把鼠标移到人物上，突出他的关系；点一下，这里显示他的介绍和全部关系。',
            'Hover over a person to highlight their relationships; click to see their profile and every relationship here.')}</li>
    <li>{bi('点连线上的字，看这段关系的原委和出处卷数；点图上空白处，回到全景。', 'Click a line label for the story behind it and the book it comes from; click an empty part of the map to return to the full view.')}</li>
  </ol>
  <p class="starts-t">{bi('从这些人开始：', 'Start with:')}</p>
  <div class="starts">{starts}</div>
</div>'''

body = f'''<svg width="0" height="0" style="position:absolute" aria-hidden="true" xmlns:xlink="http://www.w3.org/1999/xlink"><defs>{symbols(styles)}</defs></svg>
<div class="page" id="app" data-lang="zh">
<header class="top">
  <div class="topbar">
    {SITE_MOD.nav_html('odyssey')}
    <div class="langsw" role="group" aria-label="语言 / Language">
      <button type="button" data-setlang="zh" aria-pressed="true" lang="zh-CN">中文</button>
      <button type="button" data-setlang="en" aria-pressed="false" lang="en">English</button>
    </div>
  </div>
  <p class="eyebrow">{bi('荷马史诗', 'Homer')} <span class="gr">ΟΔΥΣΣΕΙΑ</span> {bi('二十四卷', '24 books')}</p>
  <h1>{bi('奥德赛人物谱', 'Who’s Who in the Odyssey')}</h1>
  <p class="lede">{bi(f'奥德修斯居中，{len(NODES) - 1} 位神、人与怪物环绕四周，{len(EDGES)} 条连线各写着一段关系。点人物或连线上的字，看详情与出处卷数。',
                       f'Odysseus stands at the center, ringed by {len(NODES) - 1} gods, mortals and monsters; each of the {len(EDGES)} lines names a relationship. Click a person or a line label for details and the book where it happens.')}</p>
  <div class="legend">
    <div class="lg"><span class="lgt">{bi('小像边框', 'Border')}</span>
      <span class="lgi">{mini('zeus', 26, 'lgp')}{bi('神', 'God')} <b>{n_god}</b></span>
      <span class="lgi">{mini('penelope', 26, 'lgp')}{bi('凡人', 'Mortal')} <b>{n_mor}</b></span>
      <span class="lgi">{mini('scylla', 26, 'lgp')}{bi('怪物', 'Monster')} <b>{n_mon}</b></span>
    </div>
    <div class="lg"><span class="lgt">{bi('画法', 'Style')}</span>
      <span class="lgi"><i class="chip-vase red"></i>{bi('红绘 · 神与凡人', 'Red-figure · gods, mortals')}</span>
      <span class="lgi"><i class="chip-vase black"></i>{bi('黑绘 · 怪物', 'Black-figure · monsters')}</span>
      <span class="lgi"><i class="chip-vase white"></i>{bi('白底 · 冥府亡魂', 'White-ground · the dead')}</span>
    </div>
    <div class="lg" role="group" aria-label="按关系类型显示连线 / Show lines by type"><span class="lgt">{bi('连线', 'Lines')}</span>{toggles}</div>
  </div>
</header>

<section class="stage" id="stage">
  <div class="mapcol">
    <div class="toolbar">
      <div class="grp" role="group" aria-label="缩放 / Zoom">
        <button type="button" data-z="-1" aria-label="缩小 / Zoom out">−</button>
        <button type="button" data-z="0" aria-label="适应宽度 / Fit">{bi('适应', 'Fit')}</button>
        <button type="button" data-z="1" aria-label="放大 / Zoom in">＋</button>
      </div>
      <p class="tbhint">{bi('移到人物上突出他的关系 · 点人物或连线上的字看详情 · 点空白处回到全景', 'Hover a person to highlight their links · click a person or a line label for details · empty space to reset')}</p>
    </div>
    <div class="mapscroll" id="mapscroll">{MAP_SVG}</div>
  </div>
  <aside class="card" id="card" aria-live="polite">{INTRO}</aside>
</section>

<section class="roster" id="roster">
  <h2>{bi('人物一览', 'All characters')}</h2>
  {roster}
</section>

<footer class="foot">
  <p>{bi('关系与细节依据荷马《奥德赛》，“卷”指全诗二十四卷的分卷，各中译本分卷一致，便于对照查阅。',
         'Relationships and details follow Homer’s Odyssey. “Book” refers to the poem’s 24 books, which are numbered the same in every translation.')}</p>
  <p>{bi('小像是仿古希腊陶瓶画的示意图：红绘（黑底陶红人物）画神与凡人，黑绘（陶红底黑色人物）画怪物，白底线描仿墓葬用的白底油瓶，画冥府中的亡魂。不是古代原作。',
         'The portraits are illustrations in the manner of Greek vase painting: red-figure (clay figures on black) for gods and mortals, black-figure (black figures on clay) for monsters, and white-ground line drawing, after the white oil flasks left at graves, for the dead in Hades. They are not copies of ancient works.')}</p>
</footer>
</div>
<script>const DATA = {data_js};</script>
<script>const INTRO_HTML = {json.dumps(INTRO, ensure_ascii=False)};</script>
<script>{js}</script>
'''

size = SITE_MOD.write_page('odyssey.html', '奥德赛人物谱',
                           '荷马《奥德赛》人物关系图，中英双语 · A bilingual character map of Homer’s Odyssey.', css, body)
print('ok odyssey', size // 1024, 'KB')
