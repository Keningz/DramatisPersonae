# -*- coding: utf-8 -*-
"""Shared pieces for every book page: book registry, top-left navigation, cross-book links,
embedded fonts and the two output variants (self-hosted site / claude.ai artifact)."""
import os, re, base64, importlib.util

SRC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))      # .../src
ROOT = os.path.dirname(SRC)                                               # project root
SITE_DIR = os.path.join(ROOT, 'site')
ART_DIR = os.path.join(ROOT, 'artifact')
FONT_DIR = os.path.join(SRC, 'common', 'fonts')

# Every book the site knows about, in navigation order. `people` points at the module that lists its characters.
BOOKS = [
    dict(id='odyssey', file='odyssey.html', zh='奥德赛', en='The Odyssey', en_short='Odyssey', en_in='the Odyssey',
         gr='ΟΔΥΣΣΕΙΑ', names='greek', people=('odyssey', 'data.py')),
    dict(id='iliad', file='iliad.html', zh='伊利亚特', en='The Iliad', en_short='Iliad', en_in='the Iliad',
         gr='ΙΛΙΑΣ', names='greek', people=('iliad', 'data_il.py')),
    dict(id='aeneid', file='aeneid.html', zh='埃涅阿斯纪', en='The Aeneid', en_short='Aeneid', en_in='the Aeneid',
         gr='AENEIS', names='roman', people=('aeneid', 'data_ae.py')),
    dict(id='journey', file='journey.html', zh='西游记', en='Journey to the West', en_short='Journey to the West',
         en_in='Journey to the West', gr='西遊記', gr_en='Xīyóu Jì', names='chinese', people=('journey', 'data_xy.py')),
    dict(id='sanguo', file='sanguo.html', zh='三国演义', en='Romance of the Three Kingdoms', en_short='Three Kingdoms',
         en_in='the Romance of the Three Kingdoms', gr='三國演義', gr_en='Sānguó Yǎnyì', names='chinese', people=('sanguo', 'data_sg.py')),
    dict(id='honglou', file='honglou.html', zh='红楼梦', en='Dream of the Red Chamber', en_short='Red Chamber',
         en_in='the Dream of the Red Chamber', gr='紅樓夢', gr_en='Hónglóu Mèng', names='chinese', people=('honglou', 'data_hl.py')),
    dict(id='got', file='got.html', zh='权力的游戏', en='Game of Thrones', en_short='Game of Thrones',
         en_in='Game of Thrones', gr='2011–2019', names='english', people=('got', 'data_got.py')),
]


def load_module(folder, filename, name):
    path = os.path.join(SRC, folder, filename)
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def people_of(book):
    mod = load_module(book['people'][0], book['people'][1], 'people_' + book['id'])
    return {n['id']: n for n in mod.NODES}


def canon(node):
    """The key that identifies a figure across books: Roman names point at the Greek id with `same_as`."""
    return node.get('same_as', node['id'])


def cross_for(current_id):
    """{person id here: [{book, file, zh, en_in, pid, name_zh, name_en, alias}, ...]} for people of the current
    book who also appear in other books. `pid` is their id in that book; `alias` is that book's naming tradition
    ('roman' / 'greek') when the name differs there (Zeus / Jupiter), else ''."""
    here = people_of(next(b for b in BOOKS if b['id'] == current_id))
    out = {}
    for b in BOOKS:
        if b['id'] == current_id:
            continue
        there = {canon(n): n for n in people_of(b).values()}
        for pid, n in here.items():
            m = there.get(canon(n))
            if m:
                out.setdefault(pid, []).append(dict(book=b['id'], file=b['file'], zh=b['zh'], en_in=b['en_in'],
                                                    pid=m['id'], name_zh=m['zh'], name_en=m['en'],
                                                    alias=(b['names'] if m['en'] != n['en'] else '')))
    return out


def xtags(entries):
    """Small “also in …” tags for roster cards."""
    out = ''
    for b in entries:
        zh = '也见《' + b['zh'] + '》' + ('·' + b['name_zh'] if b['alias'] else '')
        en = 'also in ' + b['en_in'] + (', as ' + b['name_en'] if b['alias'] else '')
        out += f'<span class="xtag">{bi(zh, en)}</span>'
    return out


def bi(zh, en, tag='span'):
    return f'<{tag} class="l-zh" lang="zh-CN">{zh}</{tag}><{tag} class="l-en" lang="en">{en}</{tag}>'


def nav_html(current):
    links = ''
    for b in BOOKS:
        cur = ' aria-current="page"' if b['id'] == current else ''
        links += f'<a href="{b["file"]}" data-xhref="{b["file"]}"{cur}>{bi(b["zh"], b["en_short"])}</a>'
    home_cur = ' aria-current="page"' if current == 'index' else ''
    return (f'<nav class="booknav" aria-label="书目 / Books">'
            f'<a class="brand" href="index.html" data-xhref="index.html"{home_cur}>{bi("人物谱", "Dramatis Personae")}</a>'
            f'<span class="bn-sep" aria-hidden="true"></span>{links}</nav>')


NAV_CSS = """
.topbar{display:flex;justify-content:space-between;align-items:center;gap:10px 12px;flex-wrap:wrap}
.booknav{display:flex;align-items:center;gap:2px;flex-wrap:wrap;background:var(--paper);border:1px solid var(--hair);border-radius:999px;padding:3px;min-width:0}
.booknav a{font-size:13.5px;line-height:1;padding:7px 12px;border-radius:999px;color:var(--muted);text-decoration:none;white-space:nowrap}
.booknav a:hover{color:var(--ink)}
.booknav a[aria-current="page"]{background:var(--ink);color:var(--bg)}
.booknav .brand{font-family:var(--f-display);font-weight:700;color:var(--ink);letter-spacing:.06em}
.page[data-lang="en"] .booknav .brand{letter-spacing:0;font-size:15px}
.booknav .bn-sep{width:1px;height:16px;background:var(--hair);margin-inline:4px}
.booknav a:focus-visible{outline:2px solid var(--aid);outline-offset:1px}
.eyebrow{margin-top:14px!important}
.xbook{display:flex;flex-direction:column;gap:6px;margin:0 0 14px;padding:10px 12px;border:1px dashed var(--hair);border-radius:8px}
.xbook .xl{font-size:12px;color:var(--muted);letter-spacing:.08em}
.xbtn{font-size:14px;font-weight:600;color:var(--aid);text-decoration:none}
.xbtn:hover{text-decoration:underline}
.xtag{display:inline-block;font-size:11.5px;color:var(--muted);border:1px solid var(--hair);border-radius:999px;padding:0 7px;line-height:1.6;margin-left:4px;font-weight:400;font-family:var(--f-body)}
"""

# Keeps links pointing at the chosen language, so the next page opens the same way.
NAV_JS = """
window.dpCross = function (xs, lang) {
  if (!xs || !xs.length) return '';
  const esc = v => String(v).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const zh = lang === 'zh';
  const note = b => !b.alias ? '' : zh ? (b.alias === 'roman' ? '（罗马名）' : '（希腊名）')
                                        : (b.alias === 'roman' ? ' (Roman name)' : ' (Greek name)');
  const label = b => zh ? `《${b.zh}》中的${b.name_zh}${note(b)}` : `${b.name_en} in ${b.en_in}${note(b)}`;
  return `<div class="xbook"><span class="xl">${zh ? '也出现在' : 'Also appears in'}</span>` + xs.map(b =>
    `<a class="xbtn" href="${b.file}#${lang}.${b.pid}" data-xfile="${b.file}" data-xperson="${b.pid}">${esc(label(b))} →</a>`).join('') + '</div>';
};

window.dpLinks = function (lang) {
  document.querySelectorAll('a[data-xhref]').forEach(a => a.setAttribute('href', a.dataset.xhref + '#' + lang));
  document.querySelectorAll('a[data-xperson]').forEach(a => a.setAttribute('href', a.dataset.xfile + '#' + lang + '.' + a.dataset.xperson));
  // bilingual labels written as "中文 / English" keep only the chosen language (the language switcher keeps both)
  [['aria-label', 'al'], ['title', 'tl']].forEach(([attr, key]) => {
    document.querySelectorAll(`[${attr}*=" / "]`).forEach(el => {
      if (el.closest('.langsw')) return;
      if (!el.dataset[key]) el.dataset[key] = el.getAttribute(attr);
      const [zh, en] = el.dataset[key].split(' / ');
      el.setAttribute(attr, lang === 'zh' ? zh : en);
    });
  });
};
window.dpHash = function () {
  return (location.hash || '').replace('#', '').toLowerCase().split(/[.\\-_~]/).filter(Boolean);
};
window.dpStoredLang = function () { try { return localStorage.getItem('dp-lang'); } catch (e) { return null; } };
window.dpSaveLang = function (l) { try { localStorage.setItem('dp-lang', l); } catch (e) { /* storage unavailable */ } };
"""

LATIN = ('U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,'
         'U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD')


def _face(family, fname, weight, urange):
    b = base64.b64encode(open(os.path.join(FONT_DIR, fname), 'rb').read()).decode()
    return (f"@font-face{{font-family:'{family}';font-style:normal;font-weight:{weight};font-display:swap;"
            f"src:url(data:font/woff2;base64,{b}) format('woff2');unicode-range:{urange}}}")


FONTFACES = ''.join([_face('EB Garamond', f'eb-garamond-latin-{w}-normal.woff2', w, LATIN) for w in (500, 600, 700)]
                    + [_face('GFS Didot', 'gfs-didot-greek-400-normal.woff2', 400,
                             'U+0370-0377,U+037A-037F,U+0384-038A,U+038C,U+038E-03A1,U+03A3-03FF'),
                       _face('GFS Didot', 'gfs-didot-greek-ext-400-normal.woff2', 400, 'U+1F00-1FFF')])
# pinyin tone vowels (ā ǎ ē ě ī ǐ ō ǒ ū ǔ ǖ-ǜ) for the Chinese novels; only those pages include it
PINYIN_FACE = _face('EB Garamond', 'eb-garamond-pinyin-500-normal.woff2', 500,
                    'U+0100-0101,U+0112-0113,U+011A-011B,U+012A-012B,U+014C-014D,U+016A-016B,U+01CD-01DC')

# Only the claude.ai variant loads Noto Serif SC from Google Fonts (unreachable in mainland China).
GOOGLE_FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
                '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
                '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@500;700;900&display=swap">\n')

# Visit statistics for the GitHub Pages copy (site/ only, not the claude.ai variant). The script loads
# asynchronously, so pages work the same where Google is blocked; those visits just go uncounted.
# Set GA_ID = '' to build without it.
GA_ID = 'G-DTTJVF6E9D'
GA_SRC = f'https://www.googletagmanager.com/gtag/js?id={GA_ID}'


def ga_tag():
    if not GA_ID:
        return ''
    return f'''<!-- Google tag (gtag.js) -->
<script async src="{GA_SRC}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());

  gtag('config', '{GA_ID}');
</script>
'''


BASE_CSS = ":root{color-scheme:light}html{-webkit-text-size-adjust:100%}body{margin:0;font-size:14px}img{max-width:100%}[hidden]{display:none!important}"


def full_doc(title, desc, css, body, google, analytics=False):
    return f'''<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{ga_tag() if analytics else ''}<title>{title}</title>
<meta name="description" content="{desc}">
{GOOGLE_FONTS if google else ''}<style>{BASE_CSS}</style>
<style>{css}</style>
</head>
<body>
{body}
</body>
</html>
'''


def write_page(filename, title, desc, css, body):
    """Writes the self-hosted page (no external requests except the async analytics tag) and the claude.ai variant."""
    os.makedirs(SITE_DIR, exist_ok=True)
    os.makedirs(ART_DIR, exist_ok=True)
    site = full_doc(title, desc, css, body, google=False, analytics=True)
    assert not re.search(r'(?:src|href)="https?://', site.replace(f'src="{GA_SRC}"', '')), \
        'site page must not load external resources (other than the analytics tag)'
    open(os.path.join(SITE_DIR, filename), 'w', encoding='utf-8').write(site)
    open(os.path.join(ART_DIR, filename), 'w', encoding='utf-8').write(full_doc(title, desc, css, body, google=True))
    return len(site)
