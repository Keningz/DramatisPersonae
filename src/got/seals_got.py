# -*- coding: utf-8 -*-
"""Game of Thrones (TV): the emblems on the seals.

The characters and house sigils belong to the series, so nobody is drawn. Instead each seal carries a small generic
emblem for the person's role at that point of the story (a crown for a ruler, a chain for a maester, a torch for the
Night's Watch ...), drawn here from scratch. The emblem changes over the episodes, like the person's side.

GLYPHS: name -> (zh label, en label, svg markup in a 100 x 100 box, centred near (50, 46), drawn in currentColor)
EMBLEMS: person id -> [(episode, glyph), ...], the first at the person's debut
HOME: the glyph shown in the whole-series view when it is not simply the one held longest
"""
import math
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from episodes_got import *  # noqa: E402,F401,F403

F = 'fill="currentColor"'
S = 'fill="none" stroke="currentColor"'


def _star(n, cx, cy, ro, ri, rot=-90):
    pts = []
    for k in range(2 * n):
        r = ro if k % 2 == 0 else ri
        a = math.radians(rot + k * 180 / n)
        pts.append(f'{cx + r * math.cos(a):.1f},{cy + r * math.sin(a):.1f}')
    return 'M' + ' L'.join(pts) + ' Z'


def _snow():
    d = ''
    for k in range(6):
        a = math.radians(90 + k * 60)
        x1, y1 = 50 + 23 * math.cos(a), 46 - 23 * math.sin(a)
        d += f'M50,46 L{x1:.1f},{y1:.1f} '
        for s in (-1, 1):            # a little branch on each arm
            bx, by = 50 + 14 * math.cos(a), 46 - 14 * math.sin(a)
            b = a + s * math.radians(40)
            d += f'M{bx:.1f},{by:.1f} L{bx + 8 * math.cos(b):.1f},{by - 8 * math.sin(b):.1f} '
    return f'<path {S} stroke-width="3.6" stroke-linecap="round" d="{d.strip()}"/>'


def _flower():
    out = ''
    for k in range(5):
        a = math.radians(-90 + k * 72)
        out += f'<circle {F} cx="{50 + 10.5 * math.cos(a):.1f}" cy="{40 + 10.5 * math.sin(a):.1f}" r="8"/>'
    return (out + f'<path {S} stroke-width="3" stroke-linecap="round" d="M50 50 Q50 62 50 74"/>'
            f'<path {F} d="M50 66 Q40 58 36 62 Q42 70 50 68 Z"/>')


GLYPHS = {
  'crown': ('国王、王后', 'King or queen',
            f'<path {F} d="M27 64 L73 64 L73 57 L27 57 Z M28 55 L23 31 L37 45 L50 25 L63 45 L77 31 L72 55 Z"/>'
            f'<circle {F} cx="23" cy="29" r="4"/><circle {F} cx="50" cy="23" r="4"/><circle {F} cx="77" cy="29" r="4"/>'),
  'keep': ('贵族、领主', 'Noble or lord',
           f'<path {F} fill-rule="evenodd" d="M31 70 L31 30 L38 30 L38 37 L46 37 L46 30 L54 30 L54 37 L62 37 L62 30 L69 30 L69 70 Z '
           f'M44 70 L44 58 A6 6 0 0 1 56 58 L56 70 Z M47.5 43 L52.5 43 L52.5 50 L47.5 50 Z"/>'),
  'hand': ('首相', 'Hand',
           f'<rect {F} x="33" y="30" width="7" height="26" rx="3.5"/><rect {F} x="41" y="23" width="7" height="33" rx="3.5"/>'
           f'<rect {F} x="49" y="22" width="7" height="34" rx="3.5"/><rect {F} x="57" y="26" width="7" height="30" rx="3.5"/>'
           f'<rect {F} x="33" y="44" width="31" height="25" rx="10"/>'
           f'<rect {F} x="61" y="44" width="7" height="20" rx="3.5" transform="rotate(38 64.5 54)"/>'),
  'sword': ('骑士、武士', 'Knight or fighter',
            f'<path {F} d="M45.5 22 L50 12 L54.5 22 L55 55 L45 55 Z"/><rect {F} x="33" y="54" width="34" height="7" rx="3.5"/>'
            f'<rect {F} x="46" y="60" width="8" height="12" rx="2"/><circle {F} cx="50" cy="75" r="5.5"/>'),
  'spear': ('持矛战士', 'Spear fighter',
            f'<path {F} d="M50 11 L59.5 31 L50 40 L40.5 31 Z"/><rect {F} x="46.8" y="37" width="6.4" height="42" rx="2.5"/>'
            f'<rect {F} x="42" y="41" width="16" height="4.5" rx="2.2"/>'),
  'bow': ('弓手', 'Archer',
          f'<path {S} stroke-width="6.5" stroke-linecap="round" d="M38 18 Q70 46 38 74"/>'
          f'<path {S} stroke-width="2.2" d="M38 18 L38 74"/><path {S} stroke-width="4.5" stroke-linecap="round" d="M26 46 L62 46"/>'
          f'<path {F} d="M75 46 L61 38 L61 54 Z"/><path {F} d="M28 46 L20 39 L23 46 L20 53 Z"/>'),
  'axe': ('野人', 'Wildling',
          f'<g transform="rotate(28 50 47)"><rect {F} x="45.5" y="15" width="7.5" height="64" rx="3"/>'
          f'<path {F} d="M53 30 L60 29 Q70 18 79 20 Q86 38 79 58 Q70 60 60 49 L53 48 Z"/>'
          f'<path {F} d="M45.5 33 L35 39 L45.5 44 Z"/></g>'),
  'chain': ('学士', 'Maester',
            f'<ellipse {S} stroke-width="5" cx="50" cy="26" rx="7.5" ry="11"/><ellipse {S} stroke-width="5" cx="50" cy="46" rx="12" ry="8.5"/>'
            f'<ellipse {S} stroke-width="5" cx="50" cy="66" rx="7.5" ry="11"/>'),
  'book': ('读书人', 'Reader',
           f'<path {F} d="M48 33 Q39 27 26 29 L26 65 Q39 63 48 69 Z M52 33 Q61 27 74 29 L74 65 Q61 63 52 69 Z"/>'),
  'coin': ('钱财', 'Coin',
           f'<ellipse {F} cx="50" cy="27" rx="22" ry="7.5"/>'
           f'<path {F} d="M28 29.5 A22 7.5 0 0 0 72 29.5 L72 37.5 A22 7.5 0 0 1 28 37.5 Z"/>'
           f'<path {F} d="M28 40.0 A22 7.5 0 0 0 72 40.0 L72 48.0 A22 7.5 0 0 1 28 48.0 Z"/>'
           f'<path {F} d="M28 50.5 A22 7.5 0 0 0 72 50.5 L72 58.5 A22 7.5 0 0 1 28 58.5 Z"/>'),
  'bird': ('情报', 'Spymaster',
           f'<path {F} d="M22 45 Q36 31 50 45 Q64 31 78 45 Q64 40 52 55 L50 60 L48 55 Q36 40 22 45 Z"/>'),
  'flame': ('光之王信徒', 'Lord of Light',
            f'<path {F} d="M50 15 Q68 36 64 54 Q61 72 50 73 Q38 72 36 57 Q34 43 45 34 Q45 46 52 49 Q57 34 50 15 Z"/>'),
  'star': ('七神', 'The Faith', f'<path {F} d="{_star(7, 50, 46, 26, 12)}"/>'),
  'ship': ('航海', 'Seafarer',
           f'<path {F} d="M22 56 L78 56 L69 69 L31 69 Z"/><rect {F} x="48.5" y="18" width="3" height="38"/>'
           f'<path {F} d="M53 21 L72 51 L53 51 Z M47 26 L32 51 L47 51 Z"/>'),
  'tree': ('古老诸神', 'Old gods',
           f'<path {F} d="M46.5 72 L47.5 50 L52.5 50 L53.5 72 Q56 72 60 74 L40 74 Q44 72 46.5 72 Z"/>'
           f'<circle {F} cx="50" cy="33" r="14"/><circle {F} cx="37" cy="43" r="10"/><circle {F} cx="63" cy="43" r="10"/>'),
  'snow': ('异鬼', 'White Walker', _snow()),
  'horse': ('多斯拉克', 'Dothraki',
            f'<path {F} d="M34 72 L66 72 L64 63 L59 63 Q61 50 57 41 L63 47 L69 42 Q64 28 51 24 L49 18 L45 25 Q37 27 33 35 '
            f'L27 45 Q28 50 33 49 L41 43 Q43 54 37 63 L35 63 Z"/>'),
  'herb': ('医者', 'Healer',
           f'<path {S} stroke-width="4.5" stroke-linecap="round" d="M50 76 Q47 50 53 20"/>'
           f'<path {F} d="M49.5 62 Q32 60 26 44 Q45 44 49.5 62 Z M50.5 47 Q67 44 74 28 Q55 29 50.5 47 Z M51.5 32 Q39 30 36 17 Q50 19 51.5 32 Z"/>'),
  'mask': ('无面者', 'Faceless',
           f'<path {F} fill-rule="evenodd" d="M29 27 Q50 17 71 27 Q74 55 50 73 Q26 55 29 27 Z '
           f'M35 41 A6.5 4 0 1 0 48 41 A6.5 4 0 1 0 35 41 Z M52 41 A6.5 4 0 1 0 65 41 A6.5 4 0 1 0 52 41 Z '
           f'M43 58 Q50 62 57 58 Q50 60 43 58 Z"/>'),
  'brokenchain': ('解放者', 'Liberator',
                  f'<ellipse {S} stroke-width="4" cx="35" cy="54" rx="11" ry="7" transform="rotate(-35 35 54)"/>'
                  f'<ellipse {S} stroke-width="4" cx="65" cy="38" rx="11" ry="7" transform="rotate(-35 65 38)"/>'
                  f'<path {S} stroke-width="2.5" stroke-linecap="round" d="M46 38 L42 33 M50 34 L50 27 M54 58 L58 63 M50 58 L50 65"/>'),
  'quill': ('译者', 'Interpreter',
            f'<path {F} d="M70 16 Q45 22 35 57 L40 59 Q52 38 70 16 Z"/>'
            f'<path {S} stroke-width="3" stroke-linecap="round" d="M37 58 L32 72 M30 74 L58 74"/>'),
  'shield': ('护卫、侍从', 'Guard or squire',
             f'<path {F} d="M31 23 L69 23 L69 44 Q69 63 50 73 Q31 63 31 44 Z"/>'),
  'hammer': ('铁匠', 'Smith',
             f'<g transform="rotate(-32 50 48)"><rect {F} x="28" y="20" width="36" height="15" rx="2.5"/>'
             f'<path {F} d="M64 22 L74 25 L74 30 L64 33 Z"/><rect {F} x="43" y="35" width="8.5" height="43" rx="3"/></g>'),
  'cup': ('侍酒', 'Cupbearer',
          f'<path {F} d="M33 21 L67 21 Q68 45 50 50 Q32 45 33 21 Z"/><rect {F} x="47.5" y="49" width="5" height="14"/>'
          f'<path {F} d="M36 72 Q50 61 64 72 Z"/>'),
  'scales': ('法律大臣', 'Master of Laws',
             f'<rect {F} x="48.5" y="22" width="3" height="46"/><rect {F} x="25" y="28" width="50" height="3.2" rx="1.6"/>'
             f'<rect {F} x="39" y="67" width="22" height="5" rx="2"/>'
             f'<path {S} stroke-width="1.6" d="M28 31 L22 50 M28 31 L34 50 M72 31 L66 50 M72 31 L78 50"/>'
             f'<path {F} d="M20 50 L36 50 Q28 59 20 50 Z M64 50 L80 50 Q72 59 64 50 Z"/>'),
  'torch': ('守夜人', 'Night’s Watch',
            f'<path {F} d="M50 13 Q63 28 59 39 Q57 45 50 45 Q43 45 41 39 Q37 28 50 13 Z"/>'
            f'<path {F} d="M43 46 L57 46 L55 52 L45 52 Z M46 52 L54 52 L52 76 L48 76 Z"/>'),
  'flower': ('少女、恋人', 'Maiden or lover', _flower()),
  'eye': ('先知', 'Seer',
          f'<path {F} fill-rule="evenodd" d="M22 46 Q50 22 78 46 Q50 70 22 46 Z M50 35 A11 11 0 1 0 50 57 A11 11 0 1 0 50 35 Z"/>'
          f'<circle {F} cx="50" cy="46" r="5"/>'),
  'shackle': ('俘虏', 'Captive',
              f'<path {S} stroke-width="7" d="M37 46 L37 35 A13 13 0 0 1 63 35 L63 46"/>'
              f'<path {F} fill-rule="evenodd" d="M34 43 H66 Q71 43 71 48 V70 Q71 75 66 75 H34 Q29 75 29 70 V48 Q29 43 34 43 Z '
              f'M45 55 A5 5 0 1 0 55 55 A5 5 0 1 0 45 55 Z M47.5 60 H52.5 L53.5 67 H46.5 Z"/>'),
}

EMBLEMS = {
  # the Starks and the North
  'ned': [(S1E1, 'keep'), (S1E2, 'hand'), (S1E8, 'shackle')],
  'catelyn': [(S1E1, 'keep')],
  'robb': [(S1E1, 'sword'), (S1E10, 'crown')],
  'talisa': [(S2E4, 'herb'), (S2E10, 'crown')],
  'sansa': [(S1E1, 'flower'), (S6E9, 'keep'), (S8E6, 'crown')],
  'arya': [(S1E1, 'bow'), (S1E2, 'sword'), (S2E4, 'cup'), (S2E8, 'sword'), (S3E7, 'shackle'), (S5E2, 'mask'), (S6E8, 'sword')],
  'bran': [(S1E1, 'keep'), (S4E10, 'tree'), (S6E5, 'eye'), (S8E6, 'crown')],
  'rickon': [(S1E1, 'keep'), (S6E3, 'shackle')],
  'jon': [(S1E1, 'sword'), (S1E3, 'torch'), (S2E10, 'axe'), (S3E10, 'torch'), (S6E3, 'sword'), (S6E10, 'crown'),
          (S7E6, 'sword'), (S8E6, 'torch')],
  'benjen': [(S1E1, 'torch'), (S6E6, 'tree')],
  'lyanna': [(S1E1, 'flower')],
  'luwin': [(S1E1, 'chain')],
  'hodor': [(S1E1, 'shield')],
  'osha': [(S1E6, 'axe')],
  'meera': [(S3E2, 'spear')],
  'jojen': [(S3E2, 'eye')],
  'roose': [(S2E4, 'keep')],
  'ramsay': [(S3E2, 'bow'), (S6E2, 'keep')],
  'lyannamo': [(S6E7, 'keep')],
  # the Wall and beyond
  'jeor': [(S1E3, 'torch')], 'aemon': [(S1E3, 'chain')], 'alliser': [(S1E3, 'sword')], 'edd': [(S2E1, 'torch')],
  'olly': [(S4E3, 'bow')], 'sam': [(S1E4, 'book'), (S8E6, 'chain')], 'gilly': [(S2E2, 'flower')],
  'craster': [(S2E1, 'axe')], 'mance': [(S3E1, 'crown')], 'tormund': [(S3E1, 'axe')], 'ygritte': [(S2E6, 'bow')],
  'threeeyed': [(S4E10, 'tree')], 'nightking': [(S4E4, 'snow')],
  # the Lannisters and the court
  'tywin': [(S1E7, 'keep'), (S1E8, 'hand')],
  'kevan': [(S1E8, 'sword')],
  'cersei': [(S1E1, 'crown'), (S5E7, 'shackle'), (S5E10, 'crown')],
  'jaime': [(S1E1, 'sword'), (S1E9, 'shackle'), (S3E10, 'sword')],
  'tyrion': [(S1E1, 'book'), (S1E4, 'shackle'), (S1E6, 'book'), (S1E10, 'hand'), (S2E10, 'book'), (S3E3, 'coin'),
             (S4E2, 'shackle'), (S4E10, 'book'), (S6E10, 'hand')],
  'lancel': [(S1E3, 'cup'), (S5E1, 'star')],
  'joffrey': [(S1E1, 'sword'), (S1E7, 'crown')],
  'myrcella': [(S1E1, 'flower')],
  'tommen': [(S1E1, 'keep'), (S4E5, 'crown')],
  'sandor': [(S1E1, 'sword')],
  'gregor': [(S1E4, 'sword')],
  'bronn': [(S1E4, 'sword'), (S8E6, 'coin')],
  'pod': [(S2E2, 'shield'), (S8E6, 'sword')],
  'shae': [(S1E9, 'flower')],
  'qyburn': [(S3E1, 'herb'), (S5E2, 'bird'), (S6E10, 'hand')],
  'pycelle': [(S1E3, 'chain')],
  'varys': [(S1E3, 'bird')],
  'littlefinger': [(S1E3, 'coin'), (S4E8, 'keep')],
  'highsparrow': [(S5E3, 'star')],
  'syrio': [(S1E3, 'sword')],
  # the Baratheons
  'robert': [(S1E1, 'crown')],
  'stannis': [(S2E1, 'crown')],
  'renly': [(S1E3, 'scales'), (S2E3, 'crown')],
  'selyse': [(S3E5, 'flame')],
  'shireen': [(S3E5, 'book')],
  'davos': [(S2E1, 'ship'), (S3E1, 'shackle'), (S3E8, 'hand'), (S8E6, 'ship')],
  'melisandre': [(S2E1, 'flame')],
  'gendry': [(S1E4, 'hammer'), (S8E4, 'keep')],
  'brienne': [(S2E3, 'sword')],
  # the Riverlands and the Vale
  'edmure': [(S3E3, 'keep'), (S3E9, 'shackle'), (S8E6, 'keep')],
  'blackfish': [(S3E3, 'sword')], 'walder': [(S1E9, 'keep')], 'beric': [(S1E6, 'sword')], 'thoros': [(S3E2, 'flame')],
  'lysa': [(S1E5, 'keep')], 'robin': [(S1E5, 'keep')], 'jonarryn': [(S1E1, 'hand')],
  # the Reach and Dorne
  'olenna': [(S3E2, 'keep')], 'mace': [(S4E2, 'keep')], 'loras': [(S1E5, 'sword'), (S5E4, 'shackle')],
  'margaery': [(S2E3, 'crown'), (S2E5, 'keep'), (S5E3, 'crown'), (S5E6, 'shackle'), (S6E6, 'crown')],
  'randyll': [(S6E6, 'sword')], 'oberyn': [(S4E1, 'spear')], 'ellaria': [(S4E1, 'flower'), (S7E3, 'shackle')],
  'doran': [(S5E2, 'keep')],
  # the Iron Islands
  'balon': [(S2E2, 'crown')],
  'yara': [(S2E2, 'ship'), (S7E2, 'shackle'), (S8E1, 'ship')],
  'theon': [(S1E1, 'bow'), (S2E3, 'ship'), (S2E6, 'keep'), (S2E10, 'shackle'), (S5E10, 'bow'), (S6E4, 'ship'), (S8E2, 'bow')],
  'euron': [(S6E2, 'ship'), (S6E5, 'crown')],
  # the Targaryens and Essos
  'daenerys': [(S1E1, 'flower'), (S1E2, 'horse'), (S3E4, 'brokenchain'), (S4E5, 'crown')],
  'viserys': [(S1E1, 'crown')], 'rhaegar': [(S1E1, 'sword')], 'aerys': [(S1E2, 'crown')],
  'drogo': [(S1E1, 'horse')], 'jorah': [(S1E1, 'sword')], 'barristan': [(S1E3, 'shield')],
  'missandei': [(S3E1, 'quill')], 'greyworm': [(S3E4, 'spear')], 'daario': [(S3E8, 'sword')],
  'illyrio': [(S1E1, 'coin')], 'mirri': [(S1E8, 'herb')], 'hizdahr': [(S4E6, 'keep')], 'jaqen': [(S2E2, 'shackle'), (S2E10, 'mask')],
}

# the whole-series view, where the emblem held longest would mislead
HOME = {'bran': 'eye', 'margaery': 'crown', 'tyrion': 'hand', 'theon': 'ship'}
