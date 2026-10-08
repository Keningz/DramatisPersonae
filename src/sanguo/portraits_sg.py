# -*- coding: utf-8 -*-
"""Romance of the Three Kingdoms portraits as Peking-opera face paintings (京剧脸谱).

Frontal busts in a 100x100 box. Painted faces follow the stage conventions where a character has a well-known
mask (关羽 red, 曹操 white, 张飞 black cross, ...); everyone else wears plain "handsome" make-up (俊扮) with rouge
round the eyes, and is told apart by beard (髯口), headgear (盔头) and costume (蟒、靠、官衣、褶子).
"""

INK = '#1d1815'
BG = '#ede3cf'
SKIN = '#f7e3d2'
DAN = '#fbefe7'
WHITE = '#f6f3ec'
C = dict(red='#b5322a', lred='#cf4a3a', pink='#e98a95', gold='#d8a93b', lgold='#efd27a', yellow='#e3b93a',
         green='#3f7a54', lgreen='#7fae7c', blue='#2f5f8f', lblue='#86a9c9', navy='#283a5c', purple='#6c3f7a',
         lpurple='#a07aae', black='#24201c', white='#f4f1ea', silver='#c9ccd0', grey='#8d8983', brown='#7a5032',
         orange='#d77a2c', teal='#2f7c78', flesh='#e9b79b', cream='#efe2c0', maroon='#7a2a2a')
BEARD = dict(black='#211c19', grey='#8e8a84', white='#f1efe9', purple='#5c3a66', red='#9c3626')


def P(d, fill='none', stroke=INK, w=1.0, extra=''):
    st = f' stroke="{stroke}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"' if stroke else ''
    return f'<path d="{d}" fill="{fill}"{st}{extra}/>'


def Cc(x, y, r, fill='none', stroke=INK, w=0.8, extra=''):
    st = f' stroke="{stroke}" stroke-width="{w}"' if stroke else ''
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"{st}{extra}/>'


def E_(x, y, rx, ry, fill, op=1.0, rot=0):
    tr = f' transform="rotate({rot} {x} {y})"' if rot else ''
    return f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{fill}" opacity="{op}"{tr}/>'


def mir(s):
    return f'<g transform="matrix(-1 0 0 1 100 0)">{s}</g>'


def both(s):
    return s + mir(s)


# ================================================================== face geometry (frontal, symmetric)
FACE = ("M50,27.5 C59.5,27.5 66.8,34 67.4,45 C67.9,54 66.2,62 61.4,68.4 C57.6,73.2 53.6,75.4 50,75.4 "
        "C46.4,75.4 42.4,73.2 38.6,68.4 C33.8,62 32.1,54 32.6,45 C33.2,34 40.5,27.5 50,27.5 Z")
FOREHEAD = "M32.9,43 C33.6,33.6 41,27.5 50,27.5 C59,27.5 66.4,33.6 67.1,43 C61.4,39.6 55.6,39.8 50,42 C44.4,39.8 38.6,39.6 32.9,43 Z"
EAR = "M33.4,46.4 C30.6,45.2 28.8,47.6 29.4,51 C30,54.6 31.8,56.8 34.2,56.6"


def face_base(col):
    return (P("M43.2,68 L43.2,80 L56.8,80 L56.8,68 Z", col, INK, 0.8)            # neck
            + both(P(EAR, col, INK, 0.8) + P("M31.6,48.6 C30.8,50 31.2,52.4 32.4,53.6", 'none', INK, 0.5))
            + P(FACE, col, INK, 0.9))


def eye(kind='almond', pupil=INK, white=WHITE, liner=INK, scale=1.0):
    """Left eye (viewer's left); mirrored for the right one."""
    if kind == 'phoenix':      # 丹凤眼: long, narrow, upswept
        s = P("M46.8,48.8 C43.8,46.8 39.6,45.6 36,46 C39.4,48 43.4,49.6 46.8,48.8 Z", white, liner, 0.9)
        s += Cc(42.6, 47.6, 1.05, pupil, None)
        s += P("M46.8,48.8 C43.8,46.8 39.6,45.6 36,46 L34.6,45", 'none', liner, 1.2)
        return s
    if kind == 'narrow':       # 细目 of the white-faced schemers
        s = P("M46.8,48.6 C44,47.2 40.4,46.6 37.2,47 C40,48.6 43.6,49.4 46.8,48.6 Z", white, liner, 0.8)
        s += Cc(43, 48, 0.95, pupil, None)
        s += P("M46.8,48.6 C44,47.2 40.4,46.6 37.2,47 L35.4,45.6", 'none', liner, 1.1)
        return s
    if kind == 'round':        # big round eyes of the painted warriors
        s = P("M47,48.8 C45.6,45.4 40.6,44.6 38,47.2 C39.6,50.6 44.6,51.4 47,48.8 Z", white, liner, 0.9)
        s += Cc(42.6, 48, 1.6, pupil, None)
        return s
    if kind == 'shut':         # 眇一目: one eye closed
        return P("M46.6,48.6 C43.6,50 40,49.8 37.4,48", 'none', liner, 1.1)
    if kind == 'small':        # clown's beady eyes
        return Cc(44.2, 49, 1.0, pupil, None) + P("M46,47.4 C44.6,46.8 43,46.8 41.8,47.6", 'none', liner, 0.6)
    # almond (默认): upswept outer corner, heavy upper liner
    s = P("M46.8,49.2 C44.6,46.4 40.4,45.8 37.8,47.2 C40.2,49.6 44,50.6 46.8,49.2 Z", white, liner, 0.8)
    s += Cc(42.7, 48.2, 1.35, pupil, None)
    s += P("M46.8,49.2 C44.6,46.4 40.4,45.8 37.8,47.2 L36.2,46", 'none', liner, 1.25)
    return s


def brow(kind='sword', col=INK):
    if kind == 'sword':        # 剑眉, swept up to the temple
        return P("M47.4,44.4 C43.8,43.8 39.4,41.8 34.6,37.4 C39.8,40 44,41.4 47.6,42.2 Z", col, col, 0.6)
    if kind == 'willow':       # 柳叶眉 for the female roles
        return P("M46.6,43.6 C43.6,41.6 40.2,41 36.4,42 C40,40.2 43.8,40.4 46.8,42.6 Z", col, col, 0.4)
    if kind == 'silkworm':     # 卧蚕眉 of Guan Yu
        return P("M47.6,45 C45.4,43.2 42.2,42.8 39.4,43.6 C37.4,44.2 35.6,43.4 34.6,41.6 C35.2,40 36.8,39.6 38.6,40.6 "
                 "C41.6,40 45.4,40.8 47.8,43.2 Z", col, col, 0.5)
    if kind == 'thin':         # long thin brows of the schemers
        return P("M47.4,43.6 C43.6,42.6 39.4,41.6 34.4,39.2", 'none', col, 1.2)
    if kind == 'frown':        # heavy, slanting down to the nose
        return P("M48,45.4 C44.6,42.6 40,40.4 34.8,39.4 C39.6,39.2 44.6,40.4 48.4,43.4 Z", col, col, 0.6)
    if kind == 'old':          # drooping white brows of old men
        return P("M47.2,43 C43.6,41.6 39.6,41.4 36.6,43 C35.2,43.8 34.4,45.6 34.6,47.4 C35.6,45.4 37.6,44.2 40.2,44 "
                 "C43,43.8 45.6,44.4 47.4,45.2 Z", col, INK, 0.5)
    return ''


def nose(col=INK):
    return P("M47.6,57.4 C48.6,58.6 51.4,58.6 52.4,57.4", 'none', col, 0.8) + both(P("M47.6,57.4 C47,56.6 47.2,55.6 47.8,55", 'none', col, 0.6))


def lips(col='#c23b3b', small=False):
    if small:
        return P("M48,63.4 C49,62.6 51,62.6 52,63.4 C51,64.6 49,64.6 48,63.4 Z", col, '#8a2a2a', 0.4)
    return P("M46.2,63.2 C48,62.2 52,62.2 53.8,63.2 C52,64.8 48,64.8 46.2,63.2 Z", col, '#7a2424', 0.5)


def rouge(col='#e8808e', strong=False):
    a, b = (0.5, 0.3) if strong else (0.36, 0.2)
    return both(E_(42.6, 50.6, 6.6, 8.6, col, a, -8) + E_(42.2, 55.4, 5.8, 7.4, col, b, -6)) + E_(50, 41.6, 2.4, 4.4, col, 0.18)


# ------------------------------------------------------------------ face painting templates
def paint_jun(sp):
    skin = sp.get('skin', SKIN)
    s = face_base(skin)
    if not sp.get('dark'):
        s += rouge(strong=not sp.get('beard') and not sp.get('old'),
                   col='#e8808e' if not sp.get('old') else '#e39a96')
    s += both(brow('sword', INK) + eye(sp.get('eye', 'almond'), pupil=sp.get('pupil', INK)))
    if sp.get('oneeye'):       # Zuo Ci, blind in one eye: cover the viewer's right eye
        s += mir(P("M46.8,49.2 C44.6,46.4 40.4,45.8 37.8,47.2 C40.2,49.6 44,50.6 46.8,49.2 Z", skin, None))
        s += mir(eye('shut'))
    s += nose('#8a5a48') + lips()
    if sp.get('old'):
        s += both(P("M36.8,51.6 C38.6,52.6 41,53 43.4,52.8", 'none', '#a67a66', 0.5)
                  + P("M45.4,58.4 C44.6,60.4 44.2,62 44.4,63.8", 'none', '#a67a66', 0.5))
        s += P("M44,36 C47,35 53,35 56,36 M45,38.4 C48,37.6 52,37.6 55,38.4", 'none', '#a67a66', 0.45)
    return s


def paint_dan(sp):
    s = face_base(DAN) + rouge('#ec7a94', strong=True)
    s += both(brow('willow') + eye('almond'))
    s += nose('#c08a7a') + lips('#d22f45', small=True)
    return s


def paint_zheng(sp):
    """整脸: the whole face one colour, features painted on top."""
    col = sp['col']
    s = face_base(col)
    mode = sp.get('mode')
    if mode == 'guan':                  # red face, silkworm brows, phoenix eyes, a mole
        s += both(brow('silkworm') + eye('phoenix'))
        s += P("M50,41.4 L50,30 M47.6,41 C46.6,37 46.6,33 47.4,29.6 M52.4,41 C53.4,37 53.4,33 52.6,29.6", 'none', INK, 0.55)
        s += both(P("M36.2,52 C38.4,54.6 41.6,55.6 44.6,55", 'none', '#7d1d18', 0.6))
        s += Cc(44.2, 53.2, 0.95, INK, None)              # 痣
        s += nose('#5a1410') + lips('#8f1f1a')
    elif mode == 'white':               # 水白脸: thin brows, narrow eyes, fine lines
        heavy = sp.get('heavy')
        s += both(brow('frown' if heavy else 'thin') + eye('narrow'))
        s += P("M49,42.6 L48.6,36.6 M51,42.6 L51.4,36.6", 'none', INK, 0.6)                 # 眉心纹
        s += P("M42,34.6 C46,33.4 54,33.4 58,34.6 M43,37 C46,36.2 54,36.2 57,37", 'none', INK, 0.4)
        s += both(P("M46.6,55.6 C44.4,58.6 43.2,61.4 43.6,65.2", 'none', INK, 0.6)        # 法令纹
                  + P("M37.4,50.6 C39.6,52.2 42.4,52.6 45,52", 'none', INK, 0.45))
        if heavy:
            s += both(P("M38.8,57 C39.6,60.4 41.4,63 43.2,64.6", 'none', INK, 0.5))
            s += E_(50, 47.4, 2.2, 1.6, '#c0392b', 0.8)
        s += nose(INK) + P("M46,63.6 C48,62.8 52,62.8 54,63.6 C52,64.8 48,64.8 46,63.6 Z", '#9a2a2a', INK, 0.4)
    elif mode == 'black':               # 黑整脸 with white-rimmed eyes
        s += both(P("M47.6,50.4 C46.4,44.6 39.6,43.2 36.4,47.4 C38.4,52.4 45.4,53.6 47.6,50.4 Z", WHITE, None)
                  + eye('round', white=WHITE, liner=INK)
                  + P("M47.4,43.6 C44,39.6 39,38.4 34.6,40 C36,37.4 39.6,36.2 43.2,37 C45.8,37.8 47.8,40.4 47.4,43.6 Z", WHITE, None))
        s += P("M50,29.4 C48.6,32 48.8,35 50,37.6 C51.2,35 51.4,32 50,29.4 Z", WHITE, None)
        s += P("M44.4,61 C47,66 53,66 55.6,61 C53,62.8 47,62.8 44.4,61 Z", WHITE, None)
        s += nose(WHITE) + lips('#c23b3b')
    return s


def socket_shape():
    return ("M48.2,52.4 C47.8,47.4 46.8,44 45.4,41.2 C42,36.8 37.4,34.4 33.8,33.8 C34,38.4 35.4,42.6 37,45.8 "
            "C37.6,49.2 39.4,52.4 42.4,53.4 C45,54.2 47.6,53.8 48.2,52.4 Z")


def paint_sankuaiwa(sp):
    """三块瓦: forehead and both cheeks in the main colour, divided by dark brow-and-eye sockets."""
    col, sock = sp['col'], sp.get('sock', C['black'])
    s = face_base(col)
    s += both(P(socket_shape(), sock, WHITE, 0.9) + eye('round', white=WHITE, liner=sock))
    s += P("M47,55 C47.4,59 48.6,60.2 50,60.2 C51.4,60.2 52.6,59 53,55 C51.6,56.4 48.4,56.4 47,55 Z", sock, WHITE, 0.6)
    s += P("M42.6,61.6 C44.6,66.8 55.4,66.8 57.4,61.6 C55,64 45,64 42.6,61.6 Z", sock, WHITE, 0.6)
    s += lips('#c23b3b')
    mark = sp.get('mark')
    if mark == 'taiji':                 # Jiang Wei's yin-yang on the brow
        s += Cc(50, 36.4, 3.4, WHITE, INK, 0.6)
        s += P("M50,33 A3.4,3.4 0 0 1 50,39.8 A1.7,1.7 0 0 1 50,36.4 A1.7,1.7 0 0 0 50,33 Z", INK, None)
        s += Cc(50, 34.7, 0.5, WHITE, None) + Cc(50, 38.1, 0.5, INK, None)
    elif mark == 'line':
        s += P("M50,30 L50,40", 'none', sock, 1.4)
    elif mark == 'flame':
        s += P("M50,30 C48.4,33 48.6,36 50,39.4 C51.4,36 51.6,33 50,30 Z", sock, WHITE, 0.5)
    return s


def paint_shizimen(sp):
    """十字门: a stripe down the brow crossing the eye sockets; Zhang Fei's is the black-and-white butterfly."""
    col, cross = sp['col'], sp.get('cross', C['black'])
    s = face_base(col)
    s += P("M47.4,27.8 C47.6,36 47.8,44 48.2,52 L51.8,52 C52.2,44 52.4,36 52.6,27.8 C51,27.5 49,27.5 47.4,27.8 Z", cross, None)
    wing = ("M48.6,51 C46.4,53.4 41.4,54.6 37.8,52.8 C34.4,51.2 32.8,46.6 33,41.4 C35.6,44 38.4,45 41.2,44.4 "
            "C43.4,43.8 45.6,42.6 47.2,40.8 C47.8,44.2 48.4,47.6 48.6,51 Z")
    curl = ("M47.2,41.4 C44.4,36.6 40,34.2 35.2,35 C37.2,32.4 42,31 45.8,32.8 C48,34 48.6,37.8 47.2,41.4 Z")
    s += both(P(wing, cross, WHITE, 0.8) + P(curl, cross, WHITE, 0.8) + eye('round', white=WHITE, liner=cross))
    s += P("M46.8,55 C47.4,59.2 48.6,60.4 50,60.4 C51.4,60.4 52.6,59.2 53.2,55 C51.6,56.6 48.4,56.6 46.8,55 Z", cross, None)
    if sp.get('smile'):
        s += P("M40.6,60.2 C43.6,67 56.4,67 59.4,60.2 C56,63.6 44,63.6 40.6,60.2 Z", cross, None)
        s += both(P("M37,58 C36.2,60.4 36.6,62.8 38.4,64", 'none', cross, 1.0))
    else:
        s += P("M42.6,61.6 C44.6,66.4 55.4,66.4 57.4,61.6 C55,63.8 45,63.8 42.6,61.6 Z", cross, None)
    s += lips('#c23b3b')
    return s


def paint_liufen(sp):
    """六分脸: the lower face in the main colour, a pale forehead and long drooping white brows (old warriors)."""
    s = face_base(sp['col'])
    s += P(FOREHEAD, WHITE, INK, 0.5)
    s += P("M50,30 C48.8,33.6 49,37 50,40 C51,37 51.2,33.6 50,30 Z", sp['col'], None)
    s += both(P("M47.8,51.4 C46.8,47 41.6,45.6 38.4,48 C39.6,52.2 45,53.6 47.8,51.4 Z", C['black'], None)
              + eye('almond', white=WHITE) + brow('old', WHITE))
    s += nose(INK) + lips('#7a1d1a')
    return s


def paint_yuanbao(sp):
    """元宝脸: forehead flesh-coloured, the rest of the face dark, joined at a curve through the brows."""
    s = face_base(sp['col'])
    s += P("M32.9,45 C33.6,33.6 41,27.5 50,27.5 C59,27.5 66.4,33.6 67.1,45 C63,41 58.6,40.6 55,42.6 "
           "C53,43.8 51.2,44 50,44 C48.8,44 47,43.8 45,42.6 C41.4,40.6 37,41 32.9,45 Z", C['flesh'], INK, 0.5)
    s += both(P("M47.6,50.8 C46.4,45.4 39.8,44 36.6,48 C38.6,52.8 45.4,53.8 47.6,50.8 Z", WHITE, None) + eye('round')
              + P("M47.6,43.4 C44.6,40.8 40,40.4 35.4,42.6 C39.4,39.4 44.4,39 47.8,41.6 Z", INK, None))
    s += nose(WHITE) + P("M44.4,61 C47,66 53,66 55.6,61 C53,62.8 47,62.8 44.4,61 Z", WHITE, None) + lips('#c23b3b')
    return s


def paint_chou(sp):
    """文丑: a white 'tofu block' over the eyes and nose."""
    s = face_base(SKIN)
    s += P("M41.4,43 C45,42 55,42 58.6,43 L57.8,57.4 C55,58.8 45,58.8 42.2,57.4 Z", WHITE, INK, 0.5)
    s += both(eye('small') + P("M46.4,45 C44.6,44 42.6,44 41.6,45", 'none', INK, 0.9))
    s += P("M48.4,55.4 C49.4,56.4 50.6,56.4 51.6,55.4", 'none', INK, 0.6)
    s += lips('#b8433b', small=True)
    return s


PAINT = dict(jun=paint_jun, dan=paint_dan, zheng=paint_zheng, sankuaiwa=paint_sankuaiwa, shizimen=paint_shizimen,
             liufen=paint_liufen, yuanbao=paint_yuanbao, chou=paint_chou)


# ================================================================== beards (髯口)
def strands(d, col, n=4):
    hl = '#55504a' if col == BEARD['black'] else ('#c9c6bf' if col == BEARD['white'] else '#00000033')
    return P(d, col, INK if col != BEARD['black'] else '#0d0b0a', 0.6) + n * ''  # texture added separately


def beard(kind, colname):
    col = BEARD[colname]
    edge = '#0d0b0a' if colname == 'black' else INK
    tex = '#5a554f' if colname == 'black' else ('#bdb9b1' if colname == 'white' else '#00000040')
    s = ''
    if kind == 'san':
        mid = "M44.8,59.4 C46.6,60.6 53.4,60.6 55.2,59.4 C56.2,70 54,83 50,97 C46,83 43.8,70 44.8,59.4 Z"
        side = "M37.4,56.6 C39.2,58.4 41.8,59 43.4,58.6 C43.6,68.6 41.8,80 38.4,92 C35.8,81 35.6,68 37.4,56.6 Z"
        s += P(mid, col, edge, 0.6) + both(P(side, col, edge, 0.6))
        s += P("M48.4,62 C48,72 48.6,84 49.6,94 M51.6,62 C52,72 51.4,84 50.4,94", 'none', tex, 0.4)
        s += both(P("M40.2,60 C40.4,70 39.8,80 38.8,88", 'none', tex, 0.4))
    elif kind == 'wuliu':       # Guan Yu's five long strands
        mid = "M45.4,59.4 C47,60.6 53,60.6 54.6,59.4 C56.4,72 54.6,88 50,104 C45.4,88 43.6,72 45.4,59.4 Z"
        inner = "M40.8,58.6 C42.2,59.8 44,60.2 45.2,60 C45.8,72 44.2,86 41,99 C38.6,86 39,72 40.8,58.6 Z"
        outer = "M35.6,55.4 C36.8,57 38.4,58 39.8,58.2 C40,67 38.6,77 35.6,87 C33.6,77 33.6,66 35.6,55.4 Z"
        s += both(P(outer, col, edge, 0.6) + P(inner, col, edge, 0.6)) + P(mid, col, edge, 0.6)
        s += P("M49,62 C48.6,76 49,90 49.8,100 M51,62 C51.4,76 51,90 50.2,100", 'none', tex, 0.4)
        s += both(P("M42.8,62 C42.6,74 41.8,86 40.8,96", 'none', tex, 0.4))
    elif kind == 'man':          # full curtain covering the mouth
        d = ("M35.2,55.6 C40,58.6 46,59.2 50,58.8 C54,59.2 60,58.6 64.8,55.6 C66.6,68 65,84 58.4,95.4 "
             "C55.4,98.4 44.6,98.4 41.6,95.4 C35,84 33.4,68 35.2,55.6 Z")
        s += P(d, col, edge, 0.6)
        s += P("M42,62 C41.6,74 42.6,86 44.6,94 M46,62 C45.8,74 46.4,86 47.4,96 M50,62 L50,97 "
               "M54,62 C54.2,74 53.6,86 52.6,96 M58,62 C58.4,74 57.4,86 55.4,94", 'none', tex, 0.4)
    elif kind == 'zha':          # bristling, with the mouth showing
        d = ("M35,55.6 L35.6,61.4 L34,65 L37,68.6 L36.4,73.6 L40.2,75.4 L40.8,80.6 L44.8,78.6 L47.2,83.4 L50,79.6 "
             "L52.8,83.4 L55.2,78.6 L59.2,80.6 L59.8,75.4 L63.6,73.6 L63,68.6 L66,65 L64.4,61.4 L65,55.6 "
             "C61,58.4 57.4,60 55.4,60.6 L55.6,65.8 C53.6,67.8 46.4,67.8 44.4,65.8 L44.6,60.6 C42.6,60 39,58.4 34.4,55.2 Z")
        s += P(d, col, edge, 0.6)
        s += P("M44,60.2 C46.6,59.2 49,59.4 50,60.4 C51,59.4 53.4,59.2 56,60.2 C53.6,61.6 51.6,61.6 50,61.2 "
               "C48.4,61.6 46.4,61.6 44,60.2 Z", col, edge, 0.5)
        s += P("M38.4,63.6 L40.6,68.6 M41.8,69 L43,74.6 M58.2,69 L57,74.6 M61.6,63.6 L59.4,68.6 M50,69.6 L50,76.6", 'none', tex, 0.45)
    elif kind == 'duan':         # short beard round the chin
        s += P("M40.2,61.4 C42.4,68.2 46.4,71.6 50,71.6 C53.6,71.6 57.6,68.2 59.8,61.4 C61,70.4 57.2,80 50,82.4 "
               "C42.8,80 39,70.4 40.2,61.4 Z", col, edge, 0.6)
        s += P("M44.4,60.6 C46.8,59.6 49,59.8 50,60.8 C51,59.8 53.2,59.6 55.6,60.6 C53.4,61.8 51.4,61.8 50,61.4 "
               "C48.6,61.8 46.6,61.8 44.4,60.6 Z", col, edge, 0.5)
    elif kind == 'chou':         # a clown's little moustache and tuft
        s += both(P("M49.4,60.4 C47.6,59.6 45.4,60 43.8,61.6", 'none', col, 1.3))
        s += P("M50,66.6 C49.4,69 49.6,71 50,72.4 C50.4,71 50.6,69 50,66.6 Z", col, edge, 0.4)
    return s


# ================================================================== headgear (盔头)
NET = {'col': INK}


def net():
    """网子 band at the hairline and the temple hair (Sun Jian's is his red headcloth, 赤帻)."""
    return (P("M33.4,40 C35,31.6 42,28.4 50,28.4 C58,28.4 65,31.6 66.6,40 L65.6,41 C63.6,35 57.4,32.4 50,32.4 "
              "C42.6,32.4 36.4,35 34.4,41 Z", NET['col'], None)
            + both(P("M33.2,40 C32.4,43.4 32.6,46.6 33.6,49 L35.2,45.2 C34.8,43.4 35,41.6 35.6,39.6 Z", INK, None)))


def pompom(x, y, r=2.2, col=None):
    col = col or C['red']
    return Cc(x, y, r, col, INK, 0.5) + Cc(x - r * 0.3, y - r * 0.3, r * 0.35, '#ffffff', None, 0, ' opacity=".45"')


def pearls(pts, r=0.9):
    return ''.join(Cc(x, y, r, '#fbf8f0', INK, 0.35) for x, y in pts)


def hat_wangmao(col=None):
    col = col or C['gold']
    s = both(P("M35,34 C33.6,40 32.6,50 33,62 L30.8,62 C30.2,50 31,40 32.4,33 Z", C['yellow'], INK, 0.5))  # side tassels
    s += both(P("M38.6,22.6 L33.4,13.4 C32,11 33.6,8.4 36.4,9.2 C38.6,9.8 39.6,12 40.4,14.4 L42,20 Z", col, INK, 0.7)
              + P("M35.8,11.6 L39.6,19.4", 'none', C['red'], 0.6))                                                   # 朝天翅
    s += P("M32.4,35 C33,24 40,14.6 50,14.6 C60,14.6 67,24 67.6,35 C61,31 56,30 50,30 C44,30 39,31 32.4,35 Z", col, INK, 0.9)
    s += P("M32.4,35 C39,31 44,30 50,30 C56,30 61,31 67.6,35 L67.2,38.4 C61,34.6 56,33.6 50,33.6 C44,33.6 39,34.6 32.8,38.4 Z", C['red'], INK, 0.6)
    s += pearls([(38, 33.6), (42, 32.4), (46, 31.8), (50, 31.6), (54, 31.8), (58, 32.4), (62, 33.6)])
    s += P("M50,16 C47,19 46.4,24 50,28 C53.6,24 53,19 50,16 Z", C['lgold'], INK, 0.5) + Cc(50, 22.6, 1.6, C['red'], INK, 0.4)
    s += pompom(50, 12.6, 2.6) + pompom(39.6, 18.4, 1.8) + pompom(60.4, 18.4, 1.8)
    s += both(P("M36,27 C38,24 41,22.4 44,22", 'none', INK, 0.4))
    return s


def hat_xiangdiao(col=None):
    col = col or C['black']
    s = both(P("M36.6,19.6 L29.6,15.4 C26.6,13.6 24.2,15.6 25.4,18.6 L27.4,22.6 C28.4,24.6 30.6,25 32.6,24 L37,22 Z", col, C['gold'], 0.8))   # 貂 flaps
    s += P("M36,30 C36,20 40.6,12.6 50,12.6 C59.4,12.6 64,20 64,30 Z", col, '#6a5a3a', 0.7)                 # tall back
    s += P("M32.4,36 C33,29 39.6,25.4 50,25.4 C60.4,25.4 67,29 67.6,36 C61,33 56,32.4 50,32.4 C44,32.4 39,33 32.4,36 Z", col, '#6a5a3a', 0.7)
    s += P("M33.6,33 C40,30 45,29.4 50,29.4 C55,29.4 60,30 66.4,33", 'none', C['gold'], 1.0)
    s += Cc(50, 28.4, 1.8, C['gold'], INK, 0.4) + pearls([(42.6, 30.4), (57.4, 30.4)], 0.8)
    s += P("M41,20 C44,17.6 56,17.6 59,20", 'none', C['gold'], 0.8)
    return s


def hat_shamao(col=None):
    col = col or C['black']
    s = both(P("M34.6,26.2 C26,24 17,23.6 11,25.4 C12.6,28.4 22,29.2 34.2,29.4 Z", col, '#6a5a3a', 0.7))   # 帽翅
    s += P("M38.4,28 C38.4,21 43,17.6 50,17.6 C57,17.6 61.6,21 61.6,28 Z", col, '#6a5a3a', 0.7)
    s += P("M32.6,36.4 C33,29.6 40,25.6 50,25.6 C60,25.6 67,29.6 67.4,36.4 C61,33.4 56,32.6 50,32.6 C44,32.6 39,33.4 32.6,36.4 Z", col, '#6a5a3a', 0.7)
    s += P("M34,33.2 C40,30.4 45,29.8 50,29.8 C55,29.8 60,30.4 66,33.2", 'none', '#6a5a3a', 0.6)
    return s


def feathers():
    """翎子: two long pheasant plumes arching out of the frame."""
    s = ''
    for side in (0, 1):
        d = "M46,20 C41,15 33,14 26,17 C19,20 16,27 17,35"
        band = P(d, 'none', '#5a3c18', 3.6) + P(d, 'none', C['cream'], 2.3, ' stroke-dasharray="2.4 2"')
        s += band if side == 0 else mir(band)
    return s


def hat_zijinguan(col=None, foxtail=False):
    col = col or C['gold']
    s = feathers()
    if foxtail:
        s += both(P("M35,34 C30,42 28.4,54 29.4,68 C31.4,64 33.4,62 35.4,62 C34.4,52 35,43 37.6,37 Z", WHITE, INK, 0.5)
                  + P("M31,52 C31.4,58 32,62 33,64", 'none', '#bdb7aa', 0.4))
    s += net()
    s += P("M40.6,30 C40,22 44,16.4 50,16.4 C56,16.4 60,22 59.4,30 Z", col, INK, 0.8)
    s += P("M38.6,31.6 C42,28.4 58,28.4 61.4,31.6 C56,30.2 44,30.2 38.6,31.6 Z", C['red'], INK, 0.5)
    s += P("M50,17.6 C47.6,20.4 47.4,24.6 50,27.4 C52.6,24.6 52.4,20.4 50,17.6 Z", C['red'], INK, 0.5)
    s += pearls([(43.6, 24), (56.4, 24), (45, 20), (55, 20)], 0.8) + pompom(50, 14.4, 2.0)
    s += both(pompom(38.4, 33.6, 1.6, C['red']))
    return s


def hat_shuaikui(col=None, tassel=None):
    col = col or C['gold']
    s = net()
    s += both(P("M33.6,36 C30.6,40 29.6,46 30.4,52 L33.4,50 C33,45.6 33.4,41 35,37.4 Z", col, INK, 0.6))   # ear guards
    s += P("M32.8,37 C32.6,24 40,15 50,15 C60,15 67.4,24 67.2,37 C61,33.4 56,32.6 50,32.6 C44,32.6 39,33.4 32.8,37 Z", col, INK, 0.9)
    s += P("M50,15.6 L50,32 M41.4,18.6 C39.6,24 39,29 39.4,33.6 M58.6,18.6 C60.4,24 61,29 60.6,33.6", 'none', '#8a6a2a', 0.6)
    s += P("M47.6,15.6 L48.4,8.6 L51.6,8.6 L52.4,15.6 Z", col, INK, 0.6)
    s += P("M50,9.6 C45,6 44,1 46,-2 C48,1 52,1 54,-2 C56,1 55,6 50,9.6 Z", tassel or C['red'], INK, 0.5)
    s += Cc(50, 26, 2.2, C['red'], INK, 0.5) + pearls([(44, 28.6), (56, 28.6)], 0.8)
    return s


def hat_fuzikui(col=None, ball=None):
    col, ball = col or C['green'], ball or C['red']
    s = net()
    s += P("M33,37 C33,28 37,22 41,20 L41,14 C44,10 56,10 59,14 L59,20 C63,22 67,28 67,37 "
           "C61,33.6 56,32.8 50,32.8 C44,32.8 39,33.6 33,37 Z", col, INK, 0.9)
    s += P("M33.6,33.6 C40,30.6 45,30 50,30 C55,30 60,30.6 66.4,33.6", 'none', C['gold'], 1.2)
    s += P("M41,20 C46,18.4 54,18.4 59,20", 'none', C['gold'], 0.9)
    s += pompom(50, 8.6, 2.4, ball) + pompom(44, 16.6, 1.6, ball) + pompom(56, 16.6, 1.6, ball)
    s += pompom(50, 25, 2.0, ball) + pompom(38.4, 27.4, 1.6, ball) + pompom(61.6, 27.4, 1.6, ball)
    s += both(P("M33,37 C30,42 29.6,48 30.6,54", 'none', C['gold'], 0.9))
    return s


def hat_daoying(col=None):
    col = col or C['silver']
    s = net()
    s += P("M33,37 C32.8,25 40,16 50,16 C60,16 67.2,25 67,37 C61,33.4 56,32.6 50,32.6 C44,32.6 39,33.4 33,37 Z", col, INK, 0.9)
    s += P("M50,16 C56,10 66,10 72,16 C78,22 82,34 80,48 C76,40 72,32 66,28 C62,24 56,20 50,16 Z", C['red'], INK, 0.6)  # 倒缨
    s += P("M56,16 C64,16 72,24 76,36 M60,20 C66,22 71,28 74,38", 'none', '#8a1e1a', 0.5)
    s += Cc(50, 26, 2.0, C['blue'], INK, 0.5) + pearls([(44, 29), (56, 29)], 0.8)
    return s


def hat_zhajin(col=None, ball=None):
    col = col or C['black']
    s = net()
    s += both(P("M35,30 C30,34 26,40 24.6,48 C28,44 31,40 35.4,36 Z", col, INK, 0.6))                     # ribbons
    s += P("M33,37.6 C33.4,27 41,20.4 50,20.4 C59,20.4 66.6,27 67,37.6 C61,33.6 56,32.8 50,32.8 C44,32.8 39,33.6 33,37.6 Z", col, INK, 0.8)
    s += P("M34,34 C40,31 45,30.4 50,30.4 C55,30.4 60,31 66,34", 'none', C['gold'], 1.2)
    s += P("M50,21 C46.6,24 46.4,28.4 50,31 C53.6,28.4 53.4,24 50,21 Z", C['gold'], INK, 0.5)
    s += pompom(50, 18.6, 2.4, ball or C['red'])
    return s


def hat_hutou(col=None):
    col = col or C['gold']
    s = net()
    s += both(P("M37.6,20 C35.6,14 36.6,10 40,9 C42,11 42.6,14.6 42,18.6 Z", col, INK, 0.6))               # ears
    s += P("M32.6,37 C32.4,24 40,15.4 50,15.4 C60,15.4 67.6,24 67.4,37 C61,33.4 56,32.6 50,32.6 C44,32.6 39,33.4 32.6,37 Z", col, INK, 0.9)
    s += both(P("M43.6,24.6 C42,22.4 39,22.4 37.6,24.8 C39.4,26.6 42,26.6 43.6,24.6 Z", WHITE, INK, 0.5) + Cc(40.6, 24.4, 0.9, INK, None))
    s += P("M46,19 L54,19 M46.4,21.4 L53.6,21.4 M50,18 L50,22.6 M45.6,22.6 L54.4,22.6", 'none', INK, 0.8)  # 王
    s += P("M46,28 C48,29.6 52,29.6 54,28 C52,31.4 48,31.4 46,28 Z", C['red'], INK, 0.5)
    s += both(P("M36,30 L33,29 M36.4,31.6 L33.4,31.8", 'none', INK, 0.5))
    return s


def hat_caowang(col=None, plumes=False):
    col = col or C['gold']
    s = feathers() if plumes else ''
    if plumes:      # fox tails hanging at the sides
        s += both(P("M34,33 C28,40 26,52 27,66 C29,62 31,60 33,60 C32,50 33,42 36.6,36 Z", WHITE, INK, 0.5))
    s += net()
    s += P("M33,37 C33,26 40,17.6 50,17.6 C60,17.6 67,26 67,37 C61,33.4 56,32.6 50,32.6 C44,32.6 39,33.4 33,37 Z", col, INK, 0.9)
    for x in (38, 44, 50, 56, 62):
        s += pompom(x, 21 if x == 50 else 23.6, 1.7, C['red'] if x != 50 else C['blue'])
    s += P("M34,33.4 C40,30.4 45,29.8 50,29.8 C55,29.8 60,30.4 66,33.4", 'none', C['red'], 1.4)
    s += pompom(50, 14.6, 2.4)
    return s


def hat_bagua(col=None):
    col = col or C['navy']
    s = both(P("M36.6,26 C32,30 29,38 28.4,48 C31,42 34,38 37.4,34 Z", col, INK, 0.6))
    s += P("M35,34.6 L37.6,12 C42,9.6 58,9.6 62.4,12 L65,34.6 C60,32.6 55,32 50,32 C45,32 40,32.6 35,34.6 Z", col, INK, 0.9)
    s += P("M37.6,12 C42,14.4 58,14.4 62.4,12", 'none', INK, 0.6)
    for (x, y, k) in ((44, 21, '111'), (56, 21, '010'), (50, 27.2, '101')):
        for i, bit in enumerate(k):
            yy = y - 2 + i * 1.6
            if bit == '1':
                s += P(f"M{x-2.6},{yy} L{x+2.6},{yy}", 'none', C['lgold'], 0.8)
            else:
                s += P(f"M{x-2.6},{yy} L{x-0.6},{yy} M{x+0.6},{yy} L{x+2.6},{yy}", 'none', C['lgold'], 0.8)
    s += P("M35.6,32 C40,30.2 60,30.2 64.4,32", 'none', C['lgold'], 0.8)
    s += net()
    return s


def hat_fangjin(col=None):
    col = col or C['navy']
    s = both(P("M38,24 C33,28 30.6,36 30.4,44 C33,40 35.4,36 38.8,32 Z", col, INK, 0.6))                    # 飘带
    s += P("M34.6,35.4 L36.4,20 C38,16.6 62,16.6 63.6,20 L65.4,35.4 C60,33 55,32.4 50,32.4 C45,32.4 40,33 34.6,35.4 Z", col, INK, 0.8)
    s += P("M36.4,20 L50,24.6 L63.6,20 M50,24.6 L50,32.4", 'none', INK, 0.5)
    s += Cc(50, 28.6, 1.7, C['white'], INK, 0.4)
    s += net()
    return s


def hat_daoguan(col=None):
    col = col or C['gold']
    s = net()
    s += P("M36,33.6 C37,27 42.6,24.4 50,24.4 C57.4,24.4 63,27 64,33.6 C59,31.4 55,30.8 50,30.8 C45,30.8 41,31.4 36,33.6 Z", INK, None)
    s += P("M40.4,27 C39.6,19 44,13.6 50,13.6 C56,13.6 60.4,19 59.6,27 Z", INK, None)                 # bun
    s += P("M41.6,25.6 C41,19.6 43.6,14.6 46,13 C46.6,16 48,17.4 50,17.4 C52,17.4 53.4,16 54,13 C56.4,14.6 59,19.6 58.4,25.6 Z", col, INK, 0.8)
    s += P("M50,17.4 L50,25.4 M45.4,16.4 C44.4,19.6 44.2,22.6 44.8,25.4 M54.6,16.4 C55.6,19.6 55.8,22.6 55.2,25.4", 'none', INK, 0.45)
    s += P("M30,20.6 L70,20.6", 'none', C['cream'], 1.5) + Cc(30, 20.6, 1.5, C['cream'], INK, 0.4) + Cc(70, 20.6, 1.0, C['cream'], INK, 0.4)
    return s


def hat_tengguan():
    """左慈's white rattan cap."""
    s = net()
    s += P("M35,34.6 C34,24 40,15.6 50,15.6 C60,15.6 66,24 65,34.6 C60,32.6 55,32 50,32 C45,32 40,32.6 35,34.6 Z", WHITE, INK, 0.8)
    for k in range(-3, 4):
        x = 50 + k * 4.4
        s += P(f"M{x-2},17.6 C{x-3},24 {x-2.6},29 {x-1.6},32.6 M{x+2},17.6 C{x+1},24 {x+1.4},29 {x+2.4},32.6", 'none', '#b9b1a0', 0.45)
    return s


def hat_huangjin():
    col = C['yellow']
    s = net()
    s += P("M33,38 C33,26 40,19 50,19 C60,19 67,26 67,38 C61,34 56,33 50,33 C44,33 39,34 33,38 Z", col, INK, 0.8)
    s += P("M34,34 C40,31 45,30.4 50,30.4 C55,30.4 60,31 66,34", 'none', '#a77f18', 0.8)
    s += P("M63,31 C70,30 76,33 80,38 C75,36 71,36 66.6,36.6 Z M64,34.6 C70,36 74,41 76,47 C71,42 67,40 63.6,38.4 Z", col, INK, 0.6)
    s += P("M41,24 C45,22 55,22 59,24", 'none', '#a77f18', 0.6)
    return s


def hat_toumian(flower=None):
    """旦角头面: a black hair mass, pearl studs, a flower and a phoenix pin; hair panels (片子) on the cheeks."""
    fl = flower or C['pink']
    s = both(P("M33.6,38 C31.6,47 32.2,59 36.8,67.6 C36,59 36.2,50.6 38.8,44 C37,42 35.6,40 33.6,38 Z", INK, None)
             + P("M36.6,40.2 C35.4,44 35.2,48 35.8,52", 'none', '#4a443e', 0.4))
    s += P("M32,40 C31,24 39,13 50,13 C61,13 69,24 68,40 C64,35 58,32.6 50,32.6 C42,32.6 36,35 32,40 Z", INK, None)
    for k in range(9):           # little forehead curls (小弯)
        x = 37 + k * 3.25
        s += Cc(x, 33.4 - (abs(k - 4) * -0.25), 1.15, INK, None)
    s += pearls([(39, 26), (43, 22.6), (47, 21), (53, 21), (57, 22.6), (61, 26), (50, 27.4), (44.6, 28.6), (55.4, 28.6)], 1.15)
    s += Cc(36.4, 21.6, 3.2, fl, INK, 0.5) + Cc(36.4, 21.6, 1.2, C['yellow'], None)
    s += Cc(63.6, 21.6, 3.2, fl, INK, 0.5) + Cc(63.6, 21.6, 1.2, C['yellow'], None)
    s += P("M50,13.6 C47,10 47,6 50,4 C53,6 53,10 50,13.6 Z", C['gold'], INK, 0.5) + pompom(50, 17.2, 1.8, C['red'])
    s += both(P("M33,30 C31.4,36 31,42 31.4,50", 'none', '#e9e2cf', 0.7, ' stroke-dasharray="0.4 1.4"'))  # 流苏
    return s


HATS = dict(wangmao=hat_wangmao, xiangdiao=hat_xiangdiao, shamao=hat_shamao, zijinguan=hat_zijinguan,
            shuaikui=hat_shuaikui, fuzikui=hat_fuzikui, daoying=hat_daoying, zhajin=hat_zhajin, hutou=hat_hutou,
            caowang=hat_caowang, bagua=hat_bagua, fangjin=hat_fangjin, daoguan=hat_daoguan, tengguan=hat_tengguan,
            huangjin=hat_huangjin, toumian=hat_toumian)


# ================================================================== costume
BODY = ("M4,104 C6,91 12,84.4 22,81.4 C30,79 37,77.4 43,76.6 L57,76.6 C63,77.4 70,79 78,81.4 "
        "C88,84.4 94,91 96,104 Z")


def flags(col):
    """靠旗: the four pennants a general wears on his back, fanned out behind his shoulders."""
    s = ''
    for d in ("M26,84 L33,82 L6,26 Z", "M30,82 L36.6,81 L20,14 Z"):
        f = P(d, col, INK, 0.7)
        s += f + mir(f)
    for d in ("M14,46 L22,44 M20,32 L26,30", ):
        s += both(P(d, 'none', C['gold'], 0.8))
    return s


def robe(kind, col, trim=None):
    trim = trim or C['gold']
    s = P(BODY, col, INK, 0.9)
    if kind in ('mang', 'guanyi', 'nv'):
        s += P("M40.6,76.6 C42.4,84.8 57.6,84.8 59.4,76.6 L56.4,76.6 C55.4,81 44.6,81 43.6,76.6 Z", WHITE, INK, 0.6)
        s += P("M38.6,77.2 C40.6,88 59.4,88 61.4,77.2", 'none', trim, 1.4)
        if kind == 'mang':      # a hint of the dragon roundel and waves
            s += both(P("M22,92 C24,88 28,88 29,91 C30,94 34,94 35,90", 'none', trim, 0.9)
                      + P("M12,99 C15,96 18,96 20,99 C22,96 25,96 27,99", 'none', trim, 0.8))
            s += Cc(50, 96, 5.4, 'none', trim, 1.0)
        elif kind == 'guanyi':  # rank badge
            s += P("M43,88 L57,88 L57,100 L43,100 Z", C['cream'], INK, 0.5) + Cc(50, 94, 2.6, 'none', trim, 0.8)
        else:
            s += both(P("M32,80 C34,88 34,96 33,104", 'none', trim, 1.6))
    elif kind in ('zhezi', 'dao', 'bagua', 'plain'):
        s += P("M41,76.6 L50,94 L59,76.6 L55.4,76.6 L50,88 L44.6,76.6 Z", WHITE if kind != 'dao' else C['cream'], INK, 0.6)
        s += P("M44.6,76.6 L50,88 L55.4,76.6", 'none', INK, 0.4)
        if kind == 'bagua':
            for (x, y) in ((24, 92), (76, 92)):
                for i, bit in enumerate('101'):
                    yy = y + i * 1.8
                    s += (P(f"M{x-3},{yy} L{x+3},{yy}", 'none', C['lgold'], 0.9) if bit == '1'
                          else P(f"M{x-3},{yy} L{x-0.8},{yy} M{x+0.8},{yy} L{x+3},{yy}", 'none', C['lgold'], 0.9))
            s += Cc(50, 99, 3.2, C['white'], INK, 0.5)
            s += P("M50,95.8 A3.2,3.2 0 0 1 50,102.2 A1.6,1.6 0 0 1 50,99 A1.6,1.6 0 0 0 50,95.8 Z", INK, None)
        if kind == 'dao':
            s += both(P("M30,82 C31,90 30.6,97 29,104", 'none', C['cream'], 1.2))
    elif kind == 'kao':          # armour: scale pattern, mirror, shoulder pieces
        d = ''
        for row in range(5):
            y = round(84 + row * 3.6, 1)
            for k in range(-6, 7):
                x = 50 + k * 6 + (3 if row % 2 else 0)
                d += f"M{x-3},{y}q3,3 6,0"
        s += P(d, 'none', '#00000055', 0.55)
        s += P("M40.6,76.6 C42.4,82 57.6,82 59.4,76.6", 'none', trim, 1.4)
        s += Cc(50, 91, 4.8, C['silver'], INK, 0.7) + Cc(50, 91, 2.6, 'none', '#ffffff', 0.6)
        s += both(P("M14,92 C14,84 20,79.6 28,80 C33,80.6 35,85 33,89 C30,86.6 24,87 20,92 Z", trim, INK, 0.7)
                  + Cc(24.6, 85, 1.4, C['red'], INK, 0.4))
    elif kind == 'felt':          # Deng Ai wrapped in felt
        s += P("M10,104 C12,90 22,82 36,78.4 C44,76.6 56,76.6 64,78.4 C78,82 88,90 90,104 Z", '#8c6c48', INK, 0.9)
        s += P("M20,86 L80,98 M18,96 L62,84 M40,79 L70,100", 'none', '#6a4e30', 0.7)
        s += P("M36,78.4 C42,82 58,82 64,78.4", 'none', INK, 0.6)
    return s


# ================================================================== props (道具)
def prop(name):
    if name == 'blade':          # 青龙偃月刀 at the viewer's left
        s = P("M15,104 L19,30", 'none', C['brown'], 2.2)
        s += P("M19,32 C12,28 9,18 11,8 C13.6,4 18,3 21,4 C19,10 20,18 23,24 C22,28 21,31 19,32 Z", C['silver'], INK, 0.8)
        s += P("M12.6,12 C15,14 17,18 18.6,24", 'none', C['green'], 1.2) + Cc(19.4, 31.6, 1.8, C['green'], INK, 0.5)
        return s
    if name == 'spear_snake':    # 丈八蛇矛
        s = P("M85,104 L81,22", 'none', C['brown'], 2.0)
        s += P("M81,24 C79,20 83,17 81,13 C79.4,10 82.6,7 81.4,2 C84,6 85.6,9 84,13 C82.6,16.6 85.4,19.6 83.4,24 Z", C['silver'], INK, 0.7)
        s += P("M78.6,26 C81,28.4 84,28.4 86,26 C84,30 80,30 78.6,26 Z", C['red'], INK, 0.4)
        return s
    if name == 'spear':          # silver spear with red tassel
        s = P("M85,104 L81.6,16", 'none', C['silver'], 2.0)
        s += P("M81.6,16 L79.6,8 L81.2,1 L83,8 Z", C['silver'], INK, 0.6)
        s += P("M79,17 C80,21 83.6,21 84.6,17 C85,22 83,26 81.8,27 C80.6,26 78.4,22 79,17 Z", C['red'], INK, 0.4)
        return s
    if name == 'halberd':        # 方天画戟
        s = P("M85,104 L81.4,14", 'none', C['brown'], 2.0)
        s += P("M81.4,14 L79.8,5 L81.2,-1 L83,5 Z", C['silver'], INK, 0.6)
        s += both_side_crescent()
        s += P("M79,22 C80,25 83.4,25 84.6,22 C84.6,27 82,29 81.8,30 C80.6,29 78.6,26 79,22 Z", C['red'], INK, 0.4)
        return s
    if name == 'fan':            # 羽扇
        s = P("M77,104 L74,84", 'none', C['brown'], 1.6)
        s += P("M74,85 C66,82 62,72 64,62 C66,56 72,53 78,54 C86,55 92,62 91,72 C90,80 82,86 74,85 Z", WHITE, INK, 0.8)
        for k in range(-3, 4):
            s += P(f"M74,84 L{77 + k * 4.2},{56 + abs(k) * 2.2}", 'none', '#a9a49a', 0.5)
        s += P("M70,84 C72,86 76,86 78,84", 'none', C['navy'], 1.4)
        return s
    if name == 'saber':          # 金刀
        s = P("M15,104 L20,40", 'none', C['red'], 2.0)
        s += P("M20,42 C15,36 13,26 15,16 C18,14 22,15 24,18 C23,26 23,34 22,42 Z", C['lgold'], INK, 0.8)
        return s
    if name == 'axe':
        s = P("M16,104 L21,20", 'none', C['brown'], 2.2)
        s += P("M21,24 C14,22 9,28 9,36 C14,34 18,36 20.4,40 Z", C['silver'], INK, 0.8)
        s += P("M21,24 C26,20 30,22 31,28 C27,28 24,31 21.4,34 Z", C['silver'], INK, 0.8)
        return s
    if name == 'coffin':         # 庞德 carries his coffin
        return (P("M64,60 L66,50 C76,44 88,40 100,37 L100,58 C88,58 76,60 64,60 Z", C['maroon'], INK, 0.8)
                + P("M66,50 C76,47 88,44 100,42", 'none', '#3a1010', 0.8)
                + P("M64,60 L66,50 L69.6,49 L68,60 Z", '#5a1c1c', INK, 0.6)
                + Cc(84, 51, 2.2, 'none', C['gold'], 0.8))
    if name == 'whip':           # 铁鞭
        s = P("M16,104 L22,30", 'none', '#55524e', 2.6)
        for k in range(8):
            y = 34 + k * 8
            x = 21.6 - k * 0.75
            s += P(f"M{x-2},{y} L{x+2},{y}", 'none', INK, 0.9)
        return s + Cc(22, 29, 1.8, '#55524e', INK, 0.5)
    if name == 'twinji':         # 典韦's twin halberds
        s = ''
        for (x0, x1) in ((12, 26), (88, 74)):
            s += P(f"M{x0},104 L{x1},28", 'none', C['brown'], 1.8)
            s += P(f"M{x1},28 L{x1 + (2 if x1 < 50 else -2)},18", 'none', C['silver'], 2.0)
            s += Cc(x1 + (-2.6 if x1 < 50 else 2.6), 30, 3.2, 'none', C['silver'], 1.4)
        return s
    if name == 'sword':
        return (P("M80,104 L88,56", 'none', '#3a3a3a', 1.6) + P("M84.6,62 L91,64", 'none', C['gold'], 2.2)
                + P("M88,56 L89,48", 'none', C['red'], 1.2))
    if name == 'twinswords':
        return (P("M80,104 L86,56", 'none', '#3a3a3a', 1.6) + P("M83,62 L89,63.6", 'none', C['gold'], 2.0)
                + P("M86,104 L90,58", 'none', '#3a3a3a', 1.6) + P("M87.4,64 L93,65.6", 'none', C['gold'], 2.0))
    if name == 'bow':
        return P("M84,30 C96,46 96,70 84,88", 'none', C['brown'], 1.8) + P("M84,30 L84,88", 'none', INK, 0.4)
    if name == 'gourd':
        return (Cc(84, 66, 5, C['orange'], INK, 0.7) + Cc(84, 58, 3.4, C['orange'], INK, 0.7)
                + P("M84,54.6 L84,52", 'none', INK, 0.8) + P("M80,62 C82,63 86,63 88,62", 'none', C['red'], 1.0))
    if name == 'whisk':
        return (P("M86,104 L82,70", 'none', C['brown'], 1.4)
                + P("M82,70 C78,62 78,50 82,40 C84,50 86,62 82,70 Z", WHITE, INK, 0.6))
    if name == 'bells':          # 甘宁's bells
        s = ''
        for (x, y) in ((25, 58), (75, 58)):
            s += P(f"M{x},{y-4} L{x},{y-16}", 'none', C['red'], 1.0)
            s += P(f"M{x-3.4},{y+3.4} C{x-3.6},{y-3.4} {x+3.6},{y-3.4} {x+3.4},{y+3.4} Z", C['gold'], INK, 0.6)
            s += Cc(x, y + 4.2, 1.1, INK, None) + P(f"M{x-2},{y-0.6} L{x+2},{y-0.6}", 'none', '#8a6a2a', 0.5)
        return s
    if name == 'yellowscroll':   # 张角's book
        return P("M74,72 L90,66 L94,80 L78,86 Z", C['yellow'], INK, 0.7) + P("M78,74 L90,70 M79,78 L91,74", 'none', INK, 0.5)
    return ''


def both_side_crescent():
    return (P("M81.6,10.6 C76,10 74,14.6 75.6,18.4 C77,16 79,15 81.6,15.4 Z", C['silver'], INK, 0.5)
            + P("M81.6,10.6 C87,10 89,14.6 87.4,18.4 C86,16 84,15 81.6,15.4 Z", C['silver'], INK, 0.5))


# ================================================================== who wears what
S = lambda **k: k

SPEC = {
  # ---- Han court and warlords
  'xiandi':     S(face='jun', beard=('san', 'black'), hat='wangmao', robe=('mang', C['yellow'])),
  'zhangjiao':  S(face='jun', old=True, beard=('san', 'black'), hat='huangjin', robe=('dao', C['yellow']), prop='yellowscroll'),
  'dongzhuo':   S(face='zheng', col=WHITE, mode='white', heavy=True, beard=('man', 'black'), hat='xiangdiao', robe=('mang', C['red'])),
  'lvbu':       S(face='jun', hat='zijinguan', foxtail=True, robe=('kao', '#e7b7c0'), flags='#e7b7c0', prop='halberd'),
  'dingyuan':   S(face='jun', old=True, beard=('man', 'grey'), hat='shuaikui', robe=('kao', C['blue']), flags=C['blue']),
  'diaochan':   S(face='dan', hat='toumian', robe=('nv', '#f2a8b8')),
  'wangyun':    S(face='jun', old=True, beard=('man', 'white'), hat='xiangdiao', robe=('mang', C['red'])),
  'yuanshao':   S(face='jun', beard=('man', 'black'), hat='shuaikui', robe=('kao', C['yellow']), flags=C['yellow']),
  'yuanshu':    S(face='jun', beard=('man', 'black'), hat='wangmao', robe=('mang', C['orange'])),
  'gongsunzan': S(face='jun', beard=('san', 'black'), hat='shuaikui', hatcol=C['silver'], robe=('kao', C['white']), flags=C['white'], prop='spear'),
  'chengong':   S(face='jun', beard=('san', 'black'), hat='shamao', robe=('guanyi', C['blue'])),
  'liubiao':    S(face='jun', old=True, beard=('san', 'white'), hat='shamao', robe=('mang', C['lblue'])),
  'mateng':     S(face='jun', old=True, beard=('man', 'white'), hat='shuaikui', robe=('kao', C['green']), flags=C['green']),
  'zhanglu':    S(face='jun', beard=('san', 'black'), hat='daoguan', robe=('dao', C['navy'])),
  'liuzhang':   S(face='jun', beard=('san', 'black'), hat='shamao', robe=('mang', C['lgreen'])),
  'menghuo':    S(face='sankuaiwa', col='#4f8a5a', hat='caowang', plumes=True, beard=('zha', 'red'), robe=('kao', C['orange']), flags=C['orange']),
  'zuoci':      S(face='jun', old=True, oneeye=True, beard=('san', 'white'), hat='tengguan', robe=('dao', C['teal']), prop='whisk'),
  'huatuo':     S(face='jun', old=True, beard=('san', 'white'), hat='fangjin', hatcol=C['brown'], robe=('zhezi', C['cream']), prop='gourd'),
  'yuji':       S(face='jun', old=True, beard=('man', 'white'), hat='daoguan', hatcol=C['silver'], robe=('dao', C['grey']), prop='whisk'),
  # ---- Wei
  'caocao':     S(face='zheng', col=WHITE, mode='white', beard=('san', 'black'), hat='xiangdiao', robe=('mang', C['red'])),
  'caopi':      S(face='jun', beard=('san', 'black'), hat='wangmao', robe=('mang', C['red'])),
  'caozhi':     S(face='jun', hat='fangjin', hatcol=C['lblue'], robe=('zhezi', C['lblue'])),
  'xiahoudun':  S(face='sankuaiwa', col='#4a76b0', beard=('zha', 'black'), hat='shuaikui', robe=('kao', C['blue']), flags=C['blue']),
  'xiahouyuan': S(face='sankuaiwa', col='#a8743e', mark='line', beard=('man', 'black'), hat='shuaikui', robe=('kao', C['red']), flags=C['red']),
  'dianwei':    S(face='sankuaiwa', col='#e0b23c', mark='flame', beard=('zha', 'red'), hat='hutou', robe=('kao', C['yellow']), prop='twinji'),
  'xuchu':      S(face='zheng', col=C['black'], mode='black', beard=('zha', 'black'), hat='hutou', robe=('kao', C['black'])),
  'zhangliao':  S(face='jun', beard=('san', 'black'), hat='shuaikui', robe=('kao', C['blue']), flags=C['blue']),
  'xunyu':      S(face='jun', beard=('san', 'black'), hat='xiangdiao', robe=('mang', C['purple'])),
  'guojia':     S(face='jun', beard=('san', 'black'), hat='fangjin', robe=('zhezi', C['navy'])),
  'simayi':     S(face='zheng', col=WHITE, mode='white', beard=('san', 'black'), hat='xiangdiao', robe=('mang', C['purple'])),
  'zhanghe':    S(face='sankuaiwa', col='#8a4c9a', beard=('zha', 'black'), hat='shuaikui', robe=('kao', C['purple']), flags=C['purple']),
  'xuhuang':    S(face='jun', beard=('man', 'black'), hat='shuaikui', robe=('kao', C['teal']), prop='axe'),
  'pangde':     S(face='jun', beard=('man', 'black'), hat='shuaikui', hatcol=C['silver'], robe=('kao', C['white']), prop='coffin'),
  'dengai':     S(face='jun', beard=('san', 'black'), hat='shuaikui', robe=('felt', '#8c6c48')),
  'zhonghui':   S(face='jun', beard=('san', 'black'), hat='shuaikui', robe=('kao', C['white']), flags=C['white']),
  'simazhao':   S(face='zheng', col=WHITE, mode='white', beard=('san', 'black'), hat='xiangdiao', robe=('mang', C['red'])),
  'simayan':    S(face='jun', beard=('san', 'black'), hat='wangmao', robe=('mang', C['yellow'])),
  'caoshuang':  S(face='jun', beard=('san', 'black'), hat='xiangdiao', robe=('mang', C['green'])),
  'jianggan':   S(face='chou', beard=('chou', 'black'), hat='fangjin', hatcol=C['black'], robe=('zhezi', C['lblue'])),
  'zhangxiu':   S(face='jun', hat='shuaikui', robe=('kao', C['green']), flags=C['green'], prop='spear'),
  'jiaxu':      S(face='jun', old=True, beard=('san', 'white'), hat='xiangdiao', robe=('guanyi', C['purple'])),
  # ---- Shu
  'liubei':     S(face='jun', beard=('san', 'black'), hat='wangmao', robe=('mang', C['red']), prop='twinswords'),
  'guanyu':     S(face='zheng', col='#b02c25', mode='guan', beard=('wuliu', 'black'), hat='fuzikui', robe=('mang', C['green']), prop='blade'),
  'zhangfei':   S(face='shizimen', col='#ece6dc', smile=True, beard=('zha', 'black'), hat='zhajin', robe=('kao', C['black']), flags=C['black'], prop='spear_snake'),
  'zhugeliang': S(face='jun', beard=('san', 'grey'), hat='bagua', robe=('bagua', C['purple']), prop='fan'),
  'zhaoyun':    S(face='jun', hat='fuzikui', hatcol=C['white'], ball=C['red'], robe=('kao', C['white']), flags=C['white'], prop='spear'),
  'machao':     S(face='jun', hat='daoying', robe=('kao', C['white']), flags=C['white'], prop='spear'),
  'huangzhong': S(face='jun', old=True, beard=('san', 'white'), hat='zhajin', hatcol=C['yellow'], robe=('kao', C['yellow']), flags=C['yellow'], prop='saber'),
  'weiyan':     S(face='shizimen', col='#c4452f', beard=('zha', 'black'), hat='shuaikui', robe=('kao', C['red']), flags=C['red']),
  'pangtong':   S(face='jun', skin='#c99b7a', beard=('duan', 'black'), hat='bagua', hatcol=C['black'], robe=('zhezi', C['navy'])),
  'jiangwei':   S(face='sankuaiwa', col='#c23a2c', mark='taiji', beard=('man', 'black'), hat='shuaikui', robe=('kao', C['green']), flags=C['green']),
  'liushan':    S(face='jun', hat='wangmao', robe=('mang', C['yellow'])),
  'masu':       S(face='sankuaiwa', col=WHITE, sock=C['black'], beard=('zha', 'black'), hat='shamao', robe=('guanyi', C['blue'])),
  'guanping':   S(face='jun', hat='zhajin', hatcol=C['green'], robe=('kao', C['white']), flags=C['white']),
  'zhoucang':   S(face='yuanbao', col=C['black'], beard=('zha', 'black'), hat='zhajin', robe=('kao', C['black']), prop='blade'),
  'mifuren':    S(face='dan', hat='toumian', flower=C['lblue'], robe=('nv', C['lblue'])),
  'xushu':      S(face='jun', beard=('san', 'black'), hat='fangjin', robe=('zhezi', C['blue']), prop='sword'),
  # ---- Wu
  'sunjian':    S(face='jun', beard=('man', 'black'), hat='shuaikui', netcol=C['red'], robe=('kao', C['red']), flags=C['red']),
  'sunce':      S(face='jun', hat='zijinguan', robe=('kao', C['red']), flags=C['red'], prop='spear'),
  'sunquan':    S(face='jun', pupil='#2f7c58', beard=('man', 'purple'), hat='caowang', robe=('mang', C['purple'])),
  'zhouyu':     S(face='jun', hat='zijinguan', robe=('mang', C['white']), prop='sword'),
  'lusu':       S(face='jun', beard=('san', 'black'), hat='shamao', robe=('guanyi', C['purple'])),
  'lvmeng':     S(face='jun', beard=('san', 'black'), hat='zhajin', hatcol=C['white'], robe=('plain', C['white'])),
  'luxun':      S(face='jun', hat='fangjin', hatcol=C['blue'], robe=('zhezi', C['white']), prop='sword'),
  'huanggai':   S(face='liufen', col='#b5322a', beard=('man', 'white'), hat='zhajin', robe=('kao', C['red']), prop='whip'),
  'ganning':    S(face='jun', beard=('man', 'black'), hat='zhajin', hatcol=C['teal'], robe=('kao', C['teal']), prop='bells'),
  'taishici':   S(face='jun', beard=('san', 'black'), hat='zhajin', hatcol=C['green'], robe=('kao', C['green']), prop='bow'),
  'sunfuren':   S(face='dan', hat='toumian', flower=C['red'], robe=('nv', C['red']), prop='sword'),
  'zhugejin':   S(face='jun', beard=('san', 'black'), hat='shamao', robe=('guanyi', C['blue'])),
  'sunhao':     S(face='jun', beard=('san', 'black'), hat='wangmao', robe=('mang', C['orange'])),
}

BEHIND = {'blade', 'saber', 'axe', 'whip', 'twinji', 'spear', 'spear_snake', 'halberd', 'bow', 'sword', 'twinswords', 'whisk'}


def build(pid, shared=None):
    """The portrait's SVG content. With a `shared` dict, repeated parts (faces, beards, hats, costumes) are
    stored there once and referenced with <use>, which keeps a page of seventy portraits small."""
    def part(svg):
        if shared is None or len(svg) < 300:
            return svg
        key = shared.setdefault(svg, f'pp{len(shared)}')
        return f'<use href="#{key}"/>'

    sp = SPEC[pid]
    s = ''
    if sp.get('flags'):
        s += part(flags(sp['flags']))
    if sp.get('prop') in BEHIND:
        s += part(prop(sp['prop']))
    kind, col = sp['robe']
    s += part(robe(kind, col))
    s += part(PAINT[sp['face']](sp))
    if sp.get('beard'):
        s += part(beard(*sp['beard']))
    h = sp.get('hat')
    NET['col'] = sp.get('netcol', INK)
    if h == 'toumian':
        hs = hat_toumian(sp.get('flower'))
    elif h == 'caowang':
        hs = hat_caowang(sp.get('hatcol'), sp.get('plumes', False))
    elif h == 'fuzikui':
        hs = hat_fuzikui(sp.get('hatcol'), sp.get('ball'))
    elif h == 'zijinguan':
        hs = hat_zijinguan(sp.get('hatcol'), sp.get('foxtail', False))
    elif h in ('tengguan', 'huangjin'):
        hs = HATS[h]()
    else:
        hs = HATS[h](sp.get('hatcol'))
    s += part(hs)
    if sp.get('prop') and sp['prop'] not in BEHIND:
        s += part(prop(sp['prop']))
    return (f'<rect width="100" height="100" fill="{BG}"/>'
            f'<g transform="translate(50 56) scale(1.15) translate(-50 -56)">{s}</g>'
            + Cc(50, 50, 46.8, 'none', INK, 0.8, ' opacity=".35"'))


def symbols(ids):
    shared = {}
    out = []
    for pid in ids:
        out.append(f'<symbol id="pt-{pid}" viewBox="0 0 100 100">'
                   f'<clipPath id="pc-{pid}"><circle cx="50" cy="50" r="50"/></clipPath>'
                   f'<g clip-path="url(#pc-{pid})">{build(pid, shared)}</g></symbol>')
    parts = [f'<symbol id="{k}" overflow="visible">{svg}</symbol>' for svg, k in shared.items()]
    return '\n'.join(parts + out)
