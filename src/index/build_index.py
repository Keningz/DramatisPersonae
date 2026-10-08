# -*- coding: utf-8 -*-
"""Landing page: the book shelf plus the people who appear in more than one book."""
import os, sys, json, html
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(SRC, 'common'))
sys.path.insert(0, os.path.join(SRC, 'odyssey'))
sys.path.insert(0, os.path.join(SRC, 'iliad'))
import dpsite as S  # noqa: E402
import portraits as OP  # noqa: E402  (Odyssey portraits)
import portraits_il as IP  # noqa: E402  (Iliad portraits)

esc = html.escape
bi = S.bi
sys.path.insert(0, os.path.join(SRC, 'aeneid'))
import portraits_ae as AP  # noqa: E402  (Aeneid portraits)
sys.path.insert(0, os.path.join(SRC, 'journey'))
import portraits_xy as XP  # noqa: E402  (Journey to the West portraits)
sys.path.insert(0, os.path.join(SRC, 'sanguo'))
import portraits_sg as SP  # noqa: E402  (Three Kingdoms opera-mask portraits)
sys.path.insert(0, os.path.join(SRC, 'honglou'))
import portraits_hl as HP  # noqa: E402  (Red Chamber gongbi portraits)

BK = {b['id']: b for b in S.BOOKS}
PEOPLE = {b['id']: S.people_of(b) for b in S.BOOKS}
OD, IL, AE, XY = PEOPLE['odyssey'], PEOPLE['iliad'], PEOPLE['aeneid'], PEOPLE['journey']
EDGE_COUNT = {'odyssey': len(S.load_module('odyssey', 'data.py', 'od_data').EDGES),
              'iliad': len(S.load_module('iliad', 'data_il.py', 'il_data').EDGES),
              'aeneid': len(S.load_module('aeneid', 'data_ae.py', 'ae_data').EDGES),
              'journey': len(S.load_module('journey', 'data_xy.py', 'xy_data').EDGES),
              'sanguo': len(S.load_module('sanguo', 'data_sg.py', 'sg_data').EDGES),
              'honglou': len(S.load_module('honglou', 'data_hl.py', 'hl_data').EDGES),
              'got': len(S.load_module('got', 'data_got.py', 'got_data').EDGES)}
GOT = S.load_module('got', 'data_got.py', 'got_data2')


def cat_of(book, pid):
    """Ring colour class: the god/mortal/monster category, for the Three Kingdoms the person's side, for the Red
    Chamber the household."""
    n = PEOPLE[book][pid]
    if book == 'honglou':
        return 'hl-' + n['camps'][0][1]
    if book == 'sanguo':
        return 'sg-' + (n['lane'] if n['lane'] != 'qun' else n['camps'][0][1])
    if book == 'got':
        return 'got-' + n['camps'][0][1]
    return n['cat']


def symbol(prefix, pid, markup):
    return (f'<symbol id="{prefix}-{pid}" viewBox="0 0 100 100"><clipPath id="{prefix}c-{pid}"><circle cx="50" cy="50" r="50"/></clipPath>'
            f'<g clip-path="url(#{prefix}c-{pid})">{markup}</g></symbol>')


def ring(cat, r=50, sw=6):
    if cat in ('demi', 'demimon'):
        half = 'ring-m' if cat == 'demi' else 'ring-x'
        return (f'<path class="ring ring-g" d="M{-r},0 A{r},{r} 0 0 1 {r},0" stroke-width="{sw}"/>'
                f'<path class="ring {half}" d="M{r},0 A{r},{r} 0 0 1 {-r},0" stroke-width="{sw}"/>')
    return f'<circle class="ring" r="{r}" stroke-width="{sw}"/>' + ('<circle class="halo" r="55.5"/>' if cat == 'god' else '')


def mini(prefix, pid, cat, size):
    if prefix == 'got':        # Game of Thrones: a seal in the house colours with the emblem of the person's first role
        n = PEOPLE['got'][pid]
        bg, ink = GOT.HOUSES[n['house']]
        en = n['en'].replace('The ', '')
        return (f'<svg class="mini cat-{cat}" viewBox="-56 -56 112 112" width="{size}" height="{size}" aria-hidden="true">'
                f'<circle class="bgc" r="56"/><circle r="50" fill="{bg}"/><circle r="42" fill="none" stroke="{ink}" stroke-width="1.6" opacity=".45"/>'
                f'<svg x="-36" y="-47" width="72" height="72" viewBox="0 0 100 100" color="{ink}">{GOT.GLYPHS[GOT.EMBLEMS[pid][0][1]][2]}</svg>'
                f'<text class="ini" y="31" dy=".36em" text-anchor="middle" fill="{ink}"><tspan class="l-zh" font-size="20">{esc(n["zh"][0])}</tspan>'
                f'<tspan class="l-en" font-size="21">{esc(en[0])}</tspan></text>{ring(cat)}</svg>')
    return (f'<svg class="mini cat-{cat}" viewBox="-56 -56 112 112" width="{size}" height="{size}" aria-hidden="true">'
            f'<circle class="bgc" r="56"/><use xlink:href="#{prefix}-{pid}" href="#{prefix}-{pid}" x="-50" y="-50" width="100" height="100"/>'
            f'{ring(cat)}</svg>')


PREFIX = {'odyssey': 'od', 'iliad': 'il', 'aeneid': 'ae', 'journey': 'xy', 'sanguo': 'sg', 'honglou': 'hl'}


def portrait(book, pid):
    if book == 'odyssey':
        return OP.build(pid, OD[pid]['style'])
    if book == 'iliad':
        return IP.build(pid)
    if book == 'aeneid':
        return AP.build(pid, AE[pid]['style'])
    if book == 'sanguo':
        return SP.build(pid)
    if book == 'honglou':
        return HP.build(pid)
    return XP.build(pid)


STRIPS = {'odyssey': ['odysseus', 'penelope', 'athena', 'telemachus', 'circe', 'polyphemus'],
          'iliad': ['achilles', 'hector', 'helen', 'priam', 'patroclus', 'andromache'],
          'aeneid': ['aeneas', 'dido', 'turnus', 'anchises', 'venus', 'camilla'],
          'journey': ['wukong', 'tangseng', 'bajie', 'shaseng', 'guanyin', 'bull'],
          'sanguo': ['caocao', 'liubei', 'guanyu', 'zhugeliang', 'sunquan', 'lvbu'],
          'honglou': ['baoyu', 'daiyu', 'baochai', 'xifeng', 'jiamu', 'liulaolao'],
          'got': ['jon', 'daenerys', 'tyrion', 'arya', 'cersei', 'sansa']}

# people who appear in more than one book, keyed by their Greek id (Roman names point there with same_as)
appear = {}
for b in S.BOOKS:
    for pid, n in PEOPLE[b['id']].items():
        appear.setdefault(S.canon(n), []).append((b['id'], pid))
ORDER = ['odysseus', 'athena', 'zeus', 'poseidon', 'hermes', 'aeneas', 'hera', 'aphrodite', 'hephaestus', 'apollo',
         'priam', 'hector', 'helen', 'andromache', 'diomedes', 'menelaus', 'nestor', 'polyphemus']
SHARED = [k for k in appear if len(appear[k]) > 1]
SHARED = [k for k in ORDER if k in SHARED] + sorted(k for k in SHARED if k not in ORDER)

NOTES = {
    'odysseus': ('在《伊利亚特》中是出使、夜袭的智将；在《奥德赛》中是漂泊十年的主角；在《埃涅阿斯纪》里，他是特洛伊人口中“残忍的尤利西斯”。',
                 'A cunning envoy and night raider in the Iliad; the wandering hero of the Odyssey; in the Aeneid, “cruel Ulysses” of the Trojans’ stories.'),
    'athena': ('在特洛伊战场上帮希腊人，在归乡路上护佑奥德修斯；罗马人称她密涅瓦，木马被说成献给她的祭品。',
               'Fights for the Greeks at Troy and guides Odysseus home; as Minerva, she is the goddess the wooden horse is supposedly offered to.'),
    'zeus': ('三部史诗里都是最终的裁决者；罗马人称他朱庇特，他许给埃涅阿斯的后代“没有尽头的统治”。',
             'The final arbiter in all three poems; as Jupiter he promises Aeneas’s descendants “empire without end”.'),
    'poseidon': ('在特洛伊帮希腊人，在海上与奥德修斯为敌；作为尼普顿，他又为埃涅阿斯平息风暴。',
                 'Helps the Greeks at Troy and hounds Odysseus at sea; as Neptune he calms the storm for Aeneas.'),
    'hermes': ('护送普里阿摩斯夜入敌营，为奥德修斯送来摩吕草；作为墨丘利，他催埃涅阿斯离开迦太基。',
               'Escorts Priam into the enemy camp and brings Odysseus the herb moly; as Mercury he orders Aeneas out of Carthage.'),
    'aeneas': ('在《伊利亚特》里，众神屡次把他救出战场，因为他命中注定要延续特洛伊王族；《埃涅阿斯纪》讲的正是这段命运。',
               'In the Iliad the gods keep rescuing him, because he is fated to carry on Troy’s royal line; the Aeneid tells that fate.'),
    'hera': ('在《伊利亚特》中与特洛伊势不两立；作为朱诺，她在《埃涅阿斯纪》里继续追击逃出来的特洛伊人。',
             'Troy’s implacable enemy in the Iliad; as Juno she goes on hounding the surviving Trojans in the Aeneid.'),
    'aphrodite': ('在《伊利亚特》中救儿子埃涅阿斯时受了伤；作为维纳斯，她一路护送儿子到意大利。',
                  'Wounded while rescuing her son Aeneas in the Iliad; as Venus she watches over him all the way to Italy.'),
    'hephaestus': ('为阿喀琉斯打造铠甲；作为伏尔甘，又为埃涅阿斯打造盾牌。', 'Forges armor for Achilles; as Vulcan, forges a shield for Aeneas.'),
    'apollo': ('《伊利亚特》里特洛伊的守护神；在《埃涅阿斯纪》里，他用神谕为特洛伊人指路。',
               'Troy’s protector in the Iliad; in the Aeneid his oracles show the Trojans the way.'),
    'priam': ('在《伊利亚特》末尾赎回赫克托尔的遗体；在《埃涅阿斯纪》里死于城破之夜。',
              'Ransoms Hector’s body at the end of the Iliad; in the Aeneid he dies on the night Troy falls.'),
    'hector': ('特洛伊的主将；在《埃涅阿斯纪》中以亡魂出现，把特洛伊托付给埃涅阿斯。',
               'Troy’s great defender; in the Aeneid, a ghost who entrusts Troy to Aeneas.'),
    'helen': ('特洛伊战争的起因；城破之夜，埃涅阿斯险些杀了她。', 'The cause of the war; on Troy’s last night Aeneas nearly kills her.'),
    'andromache': ('《伊利亚特》里为赫克托尔哭泣的妻子；《埃涅阿斯纪》里，她在异乡为他守着一座空坟。',
                   'Hector’s grieving wife in the Iliad; in the Aeneid she keeps an empty tomb for him in exile.'),
    'diomedes': ('在《伊利亚特》中刺伤了阿佛洛狄忒和埃涅阿斯；在《埃涅阿斯纪》里，他拒绝再与埃涅阿斯交战。',
                 'Wounds Aphrodite and Aeneas in the Iliad; in the Aeneid he refuses to fight Aeneas again.'),
    'menelaus': ('为夺回海伦而战；十年后在斯巴达款待忒勒马科斯。', 'Fights to win Helen back; years later hosts Telemachus in Sparta.'),
    'nestor': ('战场上的老谋士；战后在皮洛斯给忒勒马科斯讲众英雄的归途。', 'The old counselor at Troy; afterward tells Telemachus how the heroes came home.'),
    'polyphemus': ('被奥德修斯刺瞎的独眼巨人；埃涅阿斯的船队经过西西里时，他仍在摸索着追赶过往的船。',
                   'The Cyclops Odysseus blinded; when Aeneas’s fleet passes Sicily, he is still groping after passing ships.'),
}

need = {b: set(STRIPS[b]) for b in PREFIX}
for k in SHARED:
    b0, pid0 = appear[k][0]
    need[b0].add(pid0)
defs = ''.join(symbol(PREFIX[b], p, portrait(b, p)) for b in PREFIX for p in sorted(need[b]))

BLURB = {
    'odyssey': ('荷马', 'Homer', '二十四卷', '24 books',
                '奥德修斯的十年归乡：以他为圆心，神、人与怪物环绕一周，每条线写明一段关系。',
                'Odysseus’s ten-year voyage home, drawn as a ring of gods, mortals and monsters around him, every line labeled.'),
    'iliad': ('荷马', 'Homer', '二十四卷', '24 books',
              '特洛伊战争的第十年：众神在上，两军对垒。没有固定的主角，点谁，谁就走到中央。',
              'The tenth year of the Trojan War: gods above, two armies face to face. No fixed hero: click anyone to put them at the center.'),
    'aeneid': ('维吉尔', 'Virgil', '十二卷', '12 books',
               '特洛伊陷落之后：埃涅阿斯背着父亲逃出火城，经迦太基与冥府，到意大利打下罗马的根基。朱诺与维纳斯在天上各护一方。',
               'After the fall of Troy: Aeneas carries his father out of the burning city and, by way of Carthage and the underworld, reaches Italy to lay the foundations of Rome, while Juno and Venus fight over him above.'),
    'journey': ('明 · 吴承恩', 'Wu Cheng’en', '一百回', '100 chapters',
                '唐僧师徒西天取经，一路降妖。点谁，谁就走到中央；橙色的“主从”线标出哪些妖怪背后有神佛撑腰。',
                'Tang Sanzang and his disciples fight their way west for the scriptures. Click anyone to bring them to the center; orange master-and-servant lines show which demons have a god behind them.'),
    'sanguo': ('元末明初 · 罗贯中', 'Luo Guanzhong', '一百二十回', '120 chapters',
               '从桃园结义到三分归晋。拖动回目滑块，看人物登场、换阵营、结盟、反目、死去；小像仿京剧脸谱。',
               'From the oath in the peach garden to the fall of Wu. Drag the chapter slider to watch people enter, change sides, ally, turn on each other and die; the portraits are Peking-opera masks.'),
    'got': ('HBO 电视剧', 'HBO', '八季七十三集', '8 seasons, 73 episodes',
            '维斯特洛与厄索斯的群像，按地理排开、各家族自成家谱。拖到你看到的那一集，后面的死亡、背叛与真相都不会提前出现。',
            'Westeros and Essos laid out like the map, each great house a family tree in its own lands. Stop at the episode you have reached and no later death, betrayal or revelation is given away.'),
    'honglou': ('清 · 曹雪芹', 'Cao Xueqin', '一百二十回', '120 chapters',
                '贾史王薛四大家族的家谱：拖动回目看聚散生死，每段关系注明回目，金陵十二钗附判词与曲子；后四十回续书可开可关。',
                'A family tree of the four great houses: drag the chapters to watch them gather, love and scatter, with every relationship sourced to its chapter and the Twelve Beauties’ verses in their cards; the continuation’s last forty chapters can be switched on or off.'),
}
cards = ''
for b in S.BOOKS:
    bid = b['id']
    au_zh, au_en, bk_zh, bk_en, d_zh, d_en = BLURB[bid]
    nn, ne = len(PEOPLE[bid]), EDGE_COUNT[bid]
    strip = ''.join(mini(PREFIX.get(bid, bid), p, cat_of(bid, p), 46) for p in STRIPS[bid])
    meta_zh = f'<span class="l-zh" lang="zh-CN">{au_zh} · {bk_zh} · {nn} 位人物 · {ne} 段关系</span>'
    meta_en = f'<span class="l-en" lang="en">{au_en} · {bk_en} · {nn} people · {ne} relationships</span>'
    cards += (f'<a class="book" href="{b["file"]}" data-xhref="{b["file"]}">'
              f'<span class="gr{ {"roman": " la", "chinese": " cn", "english": " tv"}.get(b["names"], "") }">{bi(b["gr"], b["gr_en"]) if b.get("gr_en") else b["gr"]}</span>'
              f'<h2>{bi("《" + b["zh"] + "》", b["en"])}</h2>'
              f'<span class="meta">{meta_zh}{meta_en}</span>'
              f'<span class="strip">{strip}</span>'
              f'<p class="desc">{bi(d_zh, d_en)}</p>'
              f'<span class="go">{bi("打开人物谱 →", "Open the map →")}</span></a>')

xitems = ''
for k in SHARED:
    b0, pid0 = appear[k][0]
    n0 = PEOPLE[b0][pid0]
    greek = next(PEOPLE[b][p] for b, p in appear[k] if BK[b]['names'] == 'greek')
    roman = next((PEOPLE[b][p] for b, p in appear[k] if BK[b]['names'] == 'roman' and PEOPLE[b][p]['en'] != greek['en']), None)
    nm_zh = esc(greek['zh']) + (f'<span class="alt"> / {esc(roman["zh"])}</span>' if roman else '')
    nm_en = esc(greek['en']) + (f'<span class="alt"> / {esc(roman["en"])}</span>' if roman else '')
    links = ''
    for b, p in appear[k]:
        bk = BK[b]
        n = PEOPLE[b][p]
        as_zh = f'·{n["zh"]}' if n['en'] != greek['en'] else ''
        as_en = f' ({n["en"]})' if n['en'] != greek['en'] else ''
        links += (f'<a href="{bk["file"]}#zh.{p}" data-xfile="{bk["file"]}" data-xperson="{p}">'
                  f'{bi("《" + bk["zh"] + "》" + as_zh, bk["en_short"] + as_en)}</a>')
    note = NOTES.get(k, ('', ''))
    xitems += (f'<li>{mini(PREFIX[b0], pid0, cat_of(b0, pid0), 52)}<div class="who">'
               f'<span class="nm">{bi(nm_zh, nm_en)}<span class="gk">{esc(greek["gr"])}</span></span>'
               f'<span class="ln">{bi(note[0], note[1])}</span><span class="links">{links}</span></div></li>')

css = S.FONTFACES + S.PINYIN_FACE + open(os.path.join(HERE, 'index.css'), encoding='utf-8').read() + S.NAV_CSS
js = S.NAV_JS + '''
(() => {
  const app = document.getElementById('app');
  function setLang(l, save) {
    const lang = l === 'en' ? 'en' : 'zh';
    app.dataset.lang = lang;
    document.documentElement.lang = lang === 'zh' ? 'zh-CN' : 'en';
    document.title = 'Dramatis Personae';
    document.querySelectorAll('[data-setlang]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.setlang === lang)));
    window.dpLinks(lang);
    if (save) window.dpSaveLang(lang);
  }
  document.querySelectorAll('[data-setlang]').forEach(b => b.addEventListener('click', () => setLang(b.dataset.setlang, true)));
  const t = window.dpHash().find(x => x === 'en' || x === 'zh');
  const nav = (navigator.languages && navigator.languages[0]) || navigator.language || 'zh';
  setLang(t || window.dpStoredLang() || (/^zh/i.test(nav) ? 'zh' : 'en'), false);
})();
'''

body = f'''<svg width="0" height="0" style="position:absolute" aria-hidden="true" xmlns:xlink="http://www.w3.org/1999/xlink"><defs>{defs}</defs></svg>
<div class="page" id="app" data-lang="zh">
<header>
  <div class="topbar">
    {S.nav_html('index')}
    <div class="langsw" role="group" aria-label="语言 / Language">
      <button type="button" data-setlang="zh" aria-pressed="true" lang="zh-CN">中文</button>
      <button type="button" data-setlang="en" aria-pressed="false" lang="en">English</button>
    </div>
  </div>
  <div class="hero">
    <p class="eyebrow">{bi('经典作品人物关系图', 'Character maps of classic stories')}</p>
    <h1>{bi('人物谱', 'Dramatis Personae')}</h1>
    <p class="lede">{bi('为经典作品画人物关系图：谁是谁，彼此什么关系，出自哪一卷、哪一回。每本书一张图；在几本书里都出现的人物，互相链接。',
                         'Relationship maps for classic stories: who is who, how they are connected, and where in the text it happens. One map per book, with people who appear in more than one book linked across them.')}</p>
  </div>
</header>
<main>
  <section class="books" aria-label="书目 / Books">{cards}</section>
  <section class="cross">
    <h2>{bi('在几部书里都出现的人', 'In more than one book')}</h2>
    <p class="sub">{bi('维吉尔用罗马神名：宙斯是朱庇特，赫拉是朱诺。点书名，直接打开他在那本书里的关系图。',
                       'Virgil uses the Roman names of the gods: Zeus is Jupiter, Hera is Juno. Click a title to open that person in that book’s map.')}</p>
    <ul class="xlist">{xitems}</ul>
  </section>
</main>
<footer class="foot">
  <p>{bi('目前收录荷马的两部史诗、维吉尔的《埃涅阿斯纪》、《西游记》、《三国演义》、《红楼梦》，以及电视剧《权力的游戏》。关系与细节依据原作，并注明卷数、回目或集数。', 'So far: Homer’s two epics, Virgil’s Aeneid, Journey to the West, the Romance of the Three Kingdoms, the Dream of the Red Chamber, and the television series Game of Thrones. Relationships follow the originals, with book, chapter or episode references.')}</p>
  <p>{bi('小像是示意图，不是古代原作：荷马的人物仿古希腊陶瓶画，维吉尔的人物仿庞贝壁画，西游记的人物仿明刊本木刻绣像，三国演义的人物仿京剧脸谱，红楼梦的人物仿清代孙温的工笔重彩。权力的游戏的人物和纹章属于剧集，所以只用家族颜色的印章代替肖像。', 'The portraits are illustrations, not copies of old works: Homer’s people in the manner of Greek vase painting, Virgil’s in the manner of Roman wall painting from Pompeii, Journey to the West in the manner of Ming woodblock prints, the Three Kingdoms as Peking-opera masks, and the Red Chamber in the gongbi manner of Sun Wen’s nineteenth-century album. The characters and sigils of Game of Thrones belong to the series, so its people are shown as seals in their house colours.')}</p>
</footer>
</div>
<script>{js}</script>
'''

size = S.write_page('index.html', 'Dramatis Personae',
                    '人物谱：经典作品人物关系图 · Character maps of classic stories.', css, body)
# claude.ai main page: body only (the publish step adds the document skeleton)
open(os.path.join(S.ART_DIR, 'index_body.html'), 'w', encoding='utf-8').write(
    f'<title>Dramatis Personae</title>\n{S.GOOGLE_FONTS}<style>{css}</style>\n{body}')
print('ok index', size // 1024, 'KB')
