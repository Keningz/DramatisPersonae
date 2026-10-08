# -*- coding: utf-8 -*-
"""Builds the Journey to the West page (journey.html) on the shared dynamic-map engine (src/common/dynamic.js)."""
import json, html, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.dirname(HERE)
COMMON = os.path.join(SRC, 'common')
os.chdir(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, COMMON)
import dpsite as SITE_MOD  # noqa: E402
from data_xy import NODES, EDGES, EDGE_TYPES, ch_en  # noqa: E402
from portraits_xy import symbols  # noqa: E402

esc = html.escape
bi = SITE_MOD.bi
NODE = {n['id']: n for n in NODES}
OV = json.load(open('overview.json'))
W, H = 1200, 1070
CX, CY = 600, 540
R_OV = 30
HUB = 'wukong'
K_HUB = 42 / 40


def use(pid, extra=''):
    return f'<use xlink:href="#pt-{pid}" href="#pt-{pid}"{extra}/>'


def ring_markup(cat, r=40, sw=3.6):
    if cat in ('demi', 'demimon'):
        half = 'ring-m' if cat == 'demi' else 'ring-x'
        return (f'<path class="ring ring-g" d="M{-r},0 A{r},{r} 0 0 1 {r},0" stroke-width="{sw}"/>'
                f'<path class="ring {half}" d="M{r},0 A{r},{r} 0 0 1 {-r},0" stroke-width="{sw}"/>')
    s = f'<circle class="ring" r="{r}" stroke-width="{sw}"/>'
    if cat == 'god':
        s += f'<circle class="halo" r="{r + 6.5}"/>'
    return s


DEAD = '<g class="dead" transform="translate(29 29)"><circle r="9"/><path d="M-3.8,-3.8 L3.8,3.8 M3.8,-3.8 L-3.8,3.8"/></g>'


def face(v):
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
        + T('天庭与仙界', 'HEAVEN & THE IMMORTALS', 300, 36, 'camp', 'middle')
        + T('西天 · 灵山', 'THE WEST · VULTURE PEAK', 900, 36, 'camp', 'middle')
        + '<line x1="60" y1="294" x2="1140" y2="294"/>'
        + T('取经五众', 'THE PILGRIMS', CX, 322, 'camp', 'middle')
        + T('大闹天宫前后', 'BEFORE THE JOURNEY', 60, 330, 'camp', 'start') + T('第一至十四回', 'CHAPTERS 1–14', 60, 348, 'gk', 'start')
        + T('取经路 · 前段', 'THE ROAD · EARLY', 60, 566, 'camp', 'start') + T('第十六至四十三回', 'CHAPTERS 16–43', 60, 583, 'gk', 'start')
        + T('取经路 · 中段', 'THE ROAD · MIDDLE', 478, 716, 'camp', 'start') + T('第四十七至六十六回', 'CHAPTERS 47–66', 478, 734, 'gk', 'start')
        + T('取经路 · 后段', 'THE ROAD · LATE', 1140, 330, 'camp', 'end') + T('第六十八至九十五回', 'CHAPTERS 68–95', 1140, 348, 'gk', 'end')
        + '</g>')
rings = f'<g class="rings"><circle cx="{CX}" cy="{CY}" r="300"/><circle cx="{CX}" cy="{CY}" r="470"/></g>'
edges_svg = '<g class="edges">' + ''.join(edge_svg(i, e) for i, e in enumerate(EDGES)) + '</g>'
labels_svg = '<g class="labels">' + ''.join(label_svg(i, e) for i, e in enumerate(EDGES)) + '</g>'
nodes_svg = '<g class="nodes">' + ''.join(node_svg(n['id']) for n in NODES) + '</g>'
MAP = (f'<svg id="map" class="mode-ov" viewBox="0 0 {W} {H}" role="img" aria-label="西游记人物关系图 / Journey to the West character map" '
       f'xmlns:xlink="http://www.w3.org/1999/xlink">{deco}{rings}{edges_svg}{labels_svg}{nodes_svg}</svg>')

# ---------------------------------------------------------------- the demons and their patrons
backed = [n for n in NODES if n['camp'] == 'backed']
wild = [n for n in NODES if n['camp'] == 'wild']
killed = [n for n in NODES if n['dies']]
assert not any(n['dies'] for n in backed) and all(n['camp'] == 'wild' for n in killed)
killed_zh = '、'.join(n['zh'] for n in killed)
killed_en = ', '.join(n['en'] for n in killed[:-1]) + ' and ' + killed[-1]['en']

# ---------------------------------------------------------------- roster
CAMP = {'pilgrim': ('取经人', 'Pilgrim'), 'buddha': ('佛门', 'Buddhist'), 'heaven': ('天庭与仙界', 'Heaven and the immortals'),
        'dragon': ('龙宫', 'Dragon palace'), 'tang': ('大唐', 'Tang China'), 'gao': ('高老庄', 'Gao Village'),
        'baoxiang': ('宝象国', 'Kingdom of Baoxiang'), 'wuji': ('乌鸡国', 'Kingdom of Wuji'), 'women': ('西梁女国', 'Kingdom of Women'),
        'backed': ('有靠山的妖怪', 'Demon with a patron'), 'wild': ('没靠山的妖怪', 'Demon on its own')}
groups = [
    ('pilgrim', '取经五众', 'The pilgrims', '唐僧和他的三个徒弟，加上驮他西行的白龙马，取经后都成了正果',
     'Tang Sanzang, his three disciples and the dragon horse that carries him; all five are made saints at the end',
     [n for n in NODES if n['camp'] == 'pilgrim']),
    ('buddha', '佛门', 'The Buddhist West', '灵山的佛祖与几位菩萨', 'The Buddha of Vulture Peak and the bodhisattvas',
     [n for n in NODES if n['camp'] == 'buddha']),
    ('heaven', '天庭与仙界', 'Heaven and the immortals', '玉帝的天庭、道家的神仙，以及地上的仙人',
     'The Jade Emperor’s court, the Daoist gods and the immortals who live on earth',
     [n for n in NODES if n['camp'] == 'heaven']),
    ('dragon', '龙宫', 'The dragon kings', '四海龙王中的两位', 'Two of the four dragon kings of the seas',
     [n for n in NODES if n['camp'] == 'dragon']),
    ('mortal', '人间', 'The human world', '皇帝、国王与百姓', 'Emperors, kings and ordinary people',
     [n for n in NODES if n['camp'] in ('tang', 'gao', 'baoxiang', 'wuji', 'women')]),
    ('backed', '有靠山的妖怪', 'Demons with a patron', '神佛的坐骑、童子、宠物、亲戚或下凡的星宿，最后都被领了回去',
     'Mounts, pages, pets and relatives of gods, or stars come down to earth; every one is taken home in the end', backed),
    ('wild', '没靠山的妖怪', 'Demons on their own', '牛魔王一家与山野中的妖精；被打死的妖怪都在这里',
     'The Bull Demon King’s family and the wild demons; every demon killed in the story is here', wild),
]
assert sum(len(g[5]) for g in groups) == len(NODES)
CROSS = SITE_MOD.cross_for('journey')

roster = ''
for key, zh, en, dzh, den, items in groups:
    roster += (f'<div class="rgroup"><h3>{bi(zh, en)}<span class="cnt">{len(items)}</span>'
               f'<span class="rdesc">{bi(dzh, den)}</span></h3><div class="rgrid">')
    for n in items:
        v = n['id']
        roster += (f'<button class="rcard" data-id="{v}" type="button">{mini(v, 64, "rp")}'
                   f'<span class="rtext"><span class="rname">{bi(esc(n["zh"]), esc(n["en"]))}'
                   f'<span class="rgr">{esc(n["py"])}</span>{SITE_MOD.xtags(CROSS.get(v, []))}</span>'
                   f'<span class="rsub">{bi(esc(n["sub"][0]), esc(n["sub"][1]))}</span>'
                   f'<span class="rbio">{bi(esc(n["bio"][0]), esc(n["bio"][1]))}</span></span></button>')
    roster += '</div></div>'

counts = {k: sum(1 for e in EDGES if e[2] == k) for k in EDGE_TYPES}
dash = {'kin': '', 'mas': '10 3 2 3', 'aid': '', 'foe': '7 5', 'tie': '1.5 4.5'}
toggles = ''.join(
    f'<button class="tog t-{k}" data-type="{k}" aria-pressed="true" type="button" title="{v["desc"]}">'
    f'<svg width="34" height="10" aria-hidden="true"><line x1="2" y1="5" x2="32" y2="5" stroke-dasharray="{dash[k]}"/></svg>'
    f'{bi(v["zh"], v["en"])}<span class="tc">{counts[k]}</span></button>' for k, v in EDGE_TYPES.items())

n_cat = {c: sum(1 for n in NODES if n['cat'] == c) for c in ('god', 'demi', 'demimon', 'mortal', 'monster')}

DATA = {
    'nodes': {n['id']: dict(zh=n['zh'], en=n['en'], gr=n['py'], cat=n['cat'], camp=n['camp'],
                            dies=n['dies'], dies_en=ch_en(n['dies']) if n['dies'] else None,
                            sub=n['sub'][0], sub_en=n['sub'][1], bio=n['bio'][0], bio_en=n['bio'][1],
                            icon=n['icon'][0], icon_en=n['icon'][1], ox=OV[n['id']][0], oy=OV[n['id']][1],
                            f=face(n['id']), **({'ok': K_HUB} if n['id'] == HUB else {}))
              for n in NODES},
    'order': [n['id'] for n in NODES],
    'edges': [dict(s=e[0], t=e[1], type=e[2], label=e[3], text=e[4], label_en=e[5], text_en=e[6],
                   bk=e[7], bk_en=ch_en(e[7])) for e in EDGES],
    'types': EDGE_TYPES,
    'camp': {k: dict(zh=v[0], en=v[1]) for k, v in CAMP.items()},
    'cat': {'zh': {'god': '神佛', 'demi': '神佛转世', 'demimon': '亦神亦妖', 'mortal': '凡人', 'monster': '妖魔'},
            'en': {'god': 'God or buddha', 'demi': 'Reborn deity', 'demimon': 'Between god and demon', 'mortal': 'Mortal', 'monster': 'Demon'}},
    'W': W, 'H': H, 'CX': CX, 'CY': CY, 'R_OV': R_OV, 'cross': CROSS, 'R1': [240, 390], 'R2': 470,
    'title': {'zh': '西游记人物谱', 'en': 'Who’s Who in Journey to the West'},
}

starts = ''.join(f'<button class="chipbtn" type="button" data-go="{v}">{mini(v, 26, "mini")}{bi(NODE[v]["zh"], NODE[v]["en"])}</button>'
                 for v in ['wukong', 'tangseng', 'guanyin', 'bull', 'laojun', 'bajie'])

INTRO = f'''<div class="intro">
  <h2>{bi('怎么看这张图', 'How to read this map')}</h2>
  <ol class="howto">
    <li>{bi('全景上方左边是天庭与仙界，右边是西天灵山；取经五众在中间，路上遇到的人和妖大致按回目从左到右排开。',
            'In the overview, Heaven and the immortals are at top left and the Buddhist West at top right; the five pilgrims are in the middle, and the people and demons met on the road run roughly by chapter from left to right.')}</li>
    <li>{bi('点任何人，他就移到中央，与他有直接关系的人围成一圈，每条线写着关系；其余人物退到外圈，点一下即可换成主角。',
            'Click anyone and they move to the center, with everyone directly connected to them in a ring and each line labeled; everyone else moves to the outer ring, one click away.')}</li>
    <li>{bi('点连线上的字看这段关系的原委与回目；点图上空白处或“全景”按钮，回到全景。',
            'Click a line label for the story and the chapter it comes from; click an empty part of the map, or the Overview button, to go back to the overview.')}</li>
    <li>{bi(f'橙色点划线是“主从”：神佛与他们的坐骑、童子、宠物。图中 {len(backed)} 个有靠山的妖怪，没有一个被打死，都被主人或亲戚领了回去；被打死的 {len(killed)} 个——{killed_zh}——都没有靠山。',
            f'The orange dash-dot lines are masters and servants: gods and their mounts, pages and pets. Of the {len(backed)} demons here with a patron in Heaven, not one is killed; each is taken home by its master or its family. The {len(killed)} who are killed, {killed_en}, have no patron at all.')}</li>
  </ol>
  <p class="l-zh" lang="zh-CN" style="color:var(--muted);font-size:13px">从这些人开始：</p><p class="l-en" lang="en" style="color:var(--muted);font-size:13px">Start with:</p>
  <div class="starts">{starts}</div>
</div>'''

css_raw = open(os.path.join(COMMON, 'dynamic.css'), encoding='utf-8').read() + open('page_xy.css', encoding='utf-8').read()
js = SITE_MOD.NAV_JS + open(os.path.join(COMMON, 'dynamic.js'), encoding='utf-8').read()
css = SITE_MOD.FONTFACES + SITE_MOD.PINYIN_FACE + css_raw + SITE_MOD.NAV_CSS

legend_items = (f'<span class="lgi">{mini("rulai", 26, "lgp")}{bi("神佛", "God or buddha")} <b>{n_cat["god"]}</b></span>'
                f'<span class="lgi">{mini("tangseng", 26, "lgp")}{bi("神佛转世为人", "Deity reborn as a mortal")} <b>{n_cat["demi"]}</b></span>'
                f'<span class="lgi">{mini("wukong", 26, "lgp")}{bi("亦神亦妖", "Between god and demon")} <b>{n_cat["demimon"]}</b></span>'
                f'<span class="lgi">{mini("taizong", 26, "lgp")}{bi("凡人", "Mortal")} <b>{n_cat["mortal"]}</b></span>'
                f'<span class="lgi">{mini("bull", 26, "lgp")}{bi("妖魔", "Demon")} <b>{n_cat["monster"]}</b></span>'
                f'<span class="lgi"><span class="deadmark" aria-hidden="true">✕</span>{bi("被打死", "Killed")} <b>{len(killed)}</b></span>')

body = f'''<svg width="0" height="0" style="position:absolute" aria-hidden="true" xmlns:xlink="http://www.w3.org/1999/xlink"><defs>{symbols([n['id'] for n in NODES])}</defs></svg>
<div class="page" id="app" data-lang="zh">
<header class="top">
  <div class="topbar">
    {SITE_MOD.nav_html('journey')}
    <div class="langsw" role="group" aria-label="语言 / Language">
      <button type="button" data-setlang="zh" aria-pressed="true" lang="zh-CN">中文</button>
      <button type="button" data-setlang="en" aria-pressed="false" lang="en">English</button>
    </div>
  </div>
  <p class="eyebrow">{bi('明 · 吴承恩', 'Wu Cheng’en, Ming dynasty')} <span class="gr">{bi('西遊記', 'Xīyóu Jì')}</span> {bi('一百回', '100 chapters')}</p>
  <h1>{bi('西游记人物谱', 'Who’s Who in Journey to the West')}</h1>
  <p class="lede">{bi(f'{len(NODES)} 位神佛、凡人与妖魔，{len(EDGES)} 段关系。点谁，谁就走到中央；橙色的线告诉你，哪些妖怪背后有人。',
                       f'{len(NODES)} gods, mortals and demons, {len(EDGES)} relationships. Click anyone to bring them to the center; the orange lines show which demons have someone powerful behind them.')}</p>
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
  <p>{bi('关系与细节依据百回本《西游记》，“回”指全书一百回的回目。作者一般认为是明代的吴承恩。',
         'Relationships and details follow the standard 100-chapter text of Journey to the West; chapter numbers refer to its hundred chapters. The novel is usually attributed to Wu Cheng’en of the Ming dynasty.')}</p>
  <p>{bi('小像是仿明刊本木刻绣像的示意图，不是古代原作：墨线勾勒，米黄纸底，淡彩点染；神佛头后有圆光。',
         'The portraits are illustrations in the manner of Ming woodblock prints, not copies of old ones: ink outlines on aged paper with light hand-colored washes, and a round halo behind the gods.')}</p>
</footer>
</div>
<script>const DATA = {json.dumps(DATA, ensure_ascii=False)};</script>
<script>const INTRO_HTML = {json.dumps(INTRO, ensure_ascii=False)};</script>
<script>{js}</script>
'''

size = SITE_MOD.write_page('journey.html', '西游记人物谱',
                           '《西游记》人物关系图，中英双语 · A bilingual, interactive character map of Journey to the West.', css, body)
print('ok journey', size // 1024, 'KB')
