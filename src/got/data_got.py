# -*- coding: utf-8 -*-
"""Game of Thrones (HBO, 2011-2019): characters, relationships and allegiances on an episode timeline.

Episodes are numbered 1-73 across the eight seasons (S1E1 = 1 ... S8E6 = 73; see episodes_got.py). The node and edge
data live in nodes_*.py and edges_*.py; this module assembles and checks them. The checks matter for spoilers: a
biography entry may only cite episodes up to its own, so that moving the slider never reveals what comes later.
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "common"))
from episodes_got import EPISODES, SEASONS, SE, FIRST, LAST, code, ref_zh, ref_en  # noqa: E402,F401
from nodes_got_north import NODES_NORTH  # noqa: E402
from nodes_got_south import NODES_SOUTH  # noqa: E402
from nodes_got_essos import NODES_ESSOS  # noqa: E402
from edges_got_a import EDGES_A  # noqa: E402
from edges_got_b import EDGES_B  # noqa: E402
from edges_got_c import EDGES_C  # noqa: E402
from seals_got import GLYPHS, EMBLEMS, HOME as EM_HOME  # noqa: E402

PRE = 0
NODES = NODES_NORTH + NODES_SOUTH + NODES_ESSOS
EDGES = EDGES_A + EDGES_B + EDGES_C

# how each death happened; True = a violent death (killed, executed, suicide, poison), marked with ✕
DEATH = {
  "ned": ("被乔佛里下令斩首", "Beheaded on Joffrey’s order", True),
  "catelyn": ("红色婚礼上被割喉", "Throat cut at the Red Wedding", True),
  "robb": ("红色婚礼上被卢斯·波顿刺死", "Stabbed by Roose Bolton at the Red Wedding", True),
  "talisa": ("红色婚礼上被刺死", "Stabbed to death at the Red Wedding", True),
  "rickon": ("被拉姆斯射死", "Shot by Ramsay", True),
  "benjen": ("为救琼恩被尸鬼吞没", "Overwhelmed by the dead saving Jon", True),
  "lyanna": ("产后死于极乐塔", "Died after childbirth at the Tower of Joy", False),
  "luwin": ("被铁种刺伤，由欧莎了结", "Stabbed by the ironborn; Osha ends his pain", True),
  "hodor": ("顶住洞门，被尸鬼撕碎", "Torn apart holding the door", True),
  "osha": ("被拉姆斯刺死", "Stabbed by Ramsay", True),
  "jojen": ("被尸鬼刺伤，由梅拉了结", "Stabbed by the dead; Meera ends his life", True),
  "roose": ("被拉姆斯刺死", "Stabbed by his son Ramsay", True),
  "ramsay": ("被自己的猎犬吃掉", "Eaten by his own hounds", True),
  "lyannamo": ("被巨人尸鬼捏死", "Crushed by a dead giant", True),
  "jeor": ("被叛变者拉斯特刺死", "Stabbed in the back by the mutineer Rast", True),
  "aemon": ("寿终", "Dies of old age", False),
  "alliser": ("被琼恩吊死", "Hanged by Jon", True),
  "edd": ("被尸鬼刺死", "Killed by a wight", True),
  "olly": ("被琼恩吊死", "Hanged by Jon", True),
  "craster": ("被叛变者卡尔刺死", "Stabbed by the mutineer Karl", True),
  "mance": ("火刑柱上被琼恩一箭射死", "Shot by Jon as he burns", True),
  "ygritte": ("被奥利射死", "Shot by Olly", True),
  "threeeyed": ("被夜王杀死", "Killed by the Night King", True),
  "nightking": ("被艾莉亚刺杀", "Stabbed by Arya", True),
  "tywin": ("被提利昂射死", "Shot by Tyrion", True),
  "kevan": ("死于大圣堂的野火", "Killed in the wildfire at the Sept", True),
  "cersei": ("被埋在红堡废墟中", "Buried under the falling Red Keep", True),
  "jaime": ("被埋在红堡废墟中", "Buried under the falling Red Keep", True),
  "lancel": ("死于大圣堂的野火", "Killed in the wildfire at the Sept", True),
  "joffrey": ("婚宴上中毒身亡", "Poisoned at his wedding", True),
  "myrcella": ("被艾拉莉亚毒死", "Poisoned by Ellaria", True),
  "tommen": ("跳楼自尽", "Throws himself from a window", True),
  "sandor": ("与魔山一同坠入火海", "Falls into the fire with the Mountain", True),
  "gregor": ("与猎狗一同坠入火海", "Falls into the fire with the Hound", True),
  "shae": ("被提利昂掐死", "Strangled by Tyrion", True),
  "qyburn": ("被魔山摔死", "Killed by the Mountain", True),
  "pycelle": ("被科本的孩子们刺死", "Stabbed by Qyburn’s children", True),
  "varys": ("被丹妮莉丝用龙焰处死", "Burned by Daenerys’s dragon", True),
  "littlefinger": ("被艾莉亚割喉处决", "Executed by Arya", True),
  "highsparrow": ("死于大圣堂的野火", "Killed in the wildfire at the Sept", True),
  "robert": ("狩猎时被野猪重伤而死", "Gored by a boar while hunting", True),
  "stannis": ("被布蕾妮处决", "Executed by Brienne", True),
  "renly": ("被影子刺杀", "Killed by a shadow", True),
  "selyse": ("自缢", "Hangs herself", True),
  "shireen": ("被献祭烧死", "Burned as a sacrifice", True),
  "melisandre": ("摘下项链，化为老妇死去", "Takes off her necklace and dies of her age", False),
  "blackfish": ("在奔流城战死", "Dies fighting at Riverrun", True),
  "walder": ("被艾莉亚割喉", "Throat cut by Arya", True),
  "beric": ("为掩护艾莉亚战死", "Dies shielding Arya", True),
  "thoros": ("被尸熊咬伤后冻死", "Mauled by a dead bear; dies in the cold", True),
  "lysa": ("被小指头推下月门", "Pushed through the Moon Door", True),
  "jonarryn": ("被妻子莱莎毒死", "Poisoned by his wife Lysa", True),
  "olenna": ("饮下詹姆给的毒酒", "Drinks the poison Jaime offers", True),
  "mace": ("死于大圣堂的野火", "Killed in the wildfire at the Sept", True),
  "loras": ("死于大圣堂的野火", "Killed in the wildfire at the Sept", True),
  "margaery": ("死于大圣堂的野火", "Killed in the wildfire at the Sept", True),
  "randyll": ("被龙焰烧死", "Burned by dragonfire", True),
  "oberyn": ("被魔山挤碎头颅", "Skull crushed by the Mountain", True),
  "doran": ("被艾拉莉亚刺死", "Stabbed by Ellaria", True),
  "balon": ("被攸伦推下吊桥", "Thrown from a bridge by Euron", True),
  "theon": ("为保护布兰被夜王刺死", "Killed by the Night King defending Bran", True),
  "euron": ("被詹姆刺死", "Killed by Jaime", True),
  "daenerys": ("被琼恩刺死", "Stabbed by Jon", True),
  "viserys": ("被熔金浇头而死", "Crowned with molten gold", True),
  "rhaegar": ("在三叉戟河被劳勃所杀", "Killed by Robert at the Trident", True),
  "aerys": ("被御林铁卫詹姆刺死", "Killed by his Kingsguard, Jaime", True),
  "drogo": ("伤后成了活死人，被丹妮莉丝闷死", "Smothered by Daenerys after the blood magic", True),
  "jorah": ("为保护丹妮莉丝战死", "Dies defending Daenerys", True),
  "barristan": ("被鹰身女妖之子杀害", "Killed by the Sons of the Harpy", True),
  "missandei": ("被瑟曦下令斩首", "Beheaded on Cersei’s order", True),
  "mirri": ("被绑上火葬堆烧死", "Burned on Drogo’s pyre", True),
  "hizdahr": ("被鹰身女妖之子刺死", "Stabbed by the Sons of the Harpy", True),
}
# deaths that did not last
DOWN = {"jon": ("遇刺身亡", "Murdered by his brothers", "复活", "Brought back to life")}

ids_dead = {n["id"] for n in NODES if n["dies"] is not None}
assert set(DEATH) == ids_dead, set(DEATH) ^ ids_dead
for _n in NODES:
    _n["death"] = DEATH.get(_n["id"])
    _n.setdefault("born", None)
    _n.setdefault("subs", [])
    _n.setdefault("seen", None)
    _n.setdefault("down", [])
    _n.setdefault("home", None)

EDGE_TYPES = {
  "kin": dict(zh="亲缘", en="Family", desc="血缘与婚姻", desc_en="Blood and marriage"),
  "love": dict(zh="情缘", en="Love", desc="爱情、私情与婚约", desc_en="Love, affairs and betrothals"),
  "mas": dict(zh="效忠", en="Service", desc="主君与臣属、雇主与佣兵、师徒", desc_en="Lords and sworn men, employers and hirelings, masters and pupils"),
  "aid": dict(zh="友盟", en="Friendship", desc="友谊、结盟与相助", desc_en="Friendship, alliance and help"),
  "foe": dict(zh="仇敌", en="Enmity", desc="敌对、背叛与杀戮", desc_en="Enmity, betrayal and killing"),
  "tie": dict(zh="纠葛", en="Entangled", desc="猜忌、利用与爱恨交织", desc_en="Suspicion, use and mixed feelings"),
}

# whose side a person is on: the colour of the seal's outer ring
CAMPS = {
  "stark": dict(zh="史塔克 · 北境", en="The Starks"),
  "bolton": dict(zh="波顿", en="The Boltons"),
  "nw": dict(zh="守夜人", en="Night’s Watch"),
  "beyond": dict(zh="长城以北", en="Beyond the Wall"),
  "dead": dict(zh="异鬼", en="The dead"),
  "lannister": dict(zh="兰尼斯特", en="The Lannisters"),
  "baratheon": dict(zh="拜拉席恩", en="The Baratheons"),
  "targaryen": dict(zh="坦格利安", en="The Targaryens"),
  "greyjoy": dict(zh="葛雷乔伊", en="The Greyjoys"),
  "river": dict(zh="河间", en="The Riverlands"),
  "arryn": dict(zh="艾林 · 谷地", en="The Vale"),
  "tyrell": dict(zh="提利尔", en="The Tyrells"),
  "martell": dict(zh="马泰尔 · 多恩", en="Dorne"),
  "faith": dict(zh="七神教会", en="The Faith"),
  "essos": dict(zh="厄索斯", en="Essos"),
  "none": dict(zh="无所归属", en="Unaligned"),
}

# the house colours of each seal: (field, letter)
HOUSES = {
  "stark": ("#5F6E79", "#F4F6F7"), "tully": ("#2F5DA8", "#F2F2F2"), "arryn": ("#8FB9DF", "#173A63"),
  "lannister": ("#9E1B22", "#F0C75E"), "baratheon": ("#E4B528", "#1C1C1C"), "stagion": ("#E4B528", "#9E1B22"),
  "targaryen": ("#1A1A1A", "#D0312D"), "greyjoy": ("#1E2A2A", "#D9B44A"), "tyrell": ("#3E7B3B", "#F3D35B"),
  "martell": ("#E58A2B", "#6E1212"), "bolton": ("#E7B6BE", "#7A1424"), "frey": ("#8A929B", "#21324F"),
  "mormont": ("#3B5E3A", "#ECECEC"), "tarly": ("#4F6B3A", "#EBDDB5"), "tarth": ("#3D6FB5", "#F5B8C8"),
  "clegane": ("#C9A227", "#1E1E1E"), "payne": ("#6A4C93", "#F2EEF7"), "seaworth": ("#5C5F66", "#EDE6D0"),
  "baelish": ("#4E6B63", "#EAE2C6"), "dondarrion": ("#211F2E", "#B49AF0"), "reed": ("#61804C", "#E5EED7"),
  "nw": ("#262626", "#E6E6E6"), "beyond": ("#7B5E3B", "#F3E8D3"), "weirwood": ("#EEE9DD", "#A3221E"),
  "dead": ("#D3EBF2", "#1E5D78"), "faith": ("#EFE9DA", "#6E5B3A"), "rhllor": ("#A3221E", "#F6B44A"),
  "maester": ("#8D9399", "#FFFFFF"), "essos": ("#B98A4E", "#2F1E0C"), "dothraki": ("#7A4E25", "#F2DDB8"),
  "faceless": ("#F1F1F1", "#202020"), "smallfolk": ("#B9AA8C", "#3A2F1F"), "selmy": ("#9C7A4B", "#F4E6C2"),
}

# roster groups
GROUPS = [
  ("north", "史塔克家与北境", "The Starks and the North",
   "临冬城的史塔克一家与他们的家臣，以及北境的波顿、莫尔蒙、黎德诸家",
   "The Starks of Winterfell and their household, and the Boltons, Mormonts and Reeds of the North"),
  ("wall", "长城内外", "The Wall and beyond", "守夜人、自由民，以及长城以北的古老力量",
   "The Night’s Watch, the Free Folk and the old powers beyond the Wall"),
  ("lannister", "兰尼斯特家", "The Lannisters", "凯岩城的兰尼斯特一家、瑟曦的三个孩子，以及为他们效力的骑士、佣兵和学士",
   "The Lannisters of Casterly Rock, Cersei’s three children, and the knights, sellswords and maester who serve them"),
  ("court", "君临宫廷", "The court", "御前会议的大臣、教会的领袖，以及宫中的过客",
   "The king’s councillors, the head of the Faith, and passing visitors to court"),
  ("baratheon", "拜拉席恩家", "The Baratheons", "劳勃和他的两个弟弟、龙石岛上的史坦尼斯一家，以及詹德利与布蕾妮",
   "Robert and his brothers, Stannis’s household on Dragonstone, and Gendry and Brienne"),
  ("river", "河间与谷地", "The Riverlands and the Vale", "徒利家、佛雷家、无旗兄弟会，以及鹰巢城的艾林家",
   "The Tullys, the Freys, the Brotherhood without Banners and the Arryns of the Eyrie"),
  ("south", "河湾与多恩", "The Reach and Dorne", "高庭的提利尔家、角陵的塔利家，以及多恩的马泰尔家",
   "The Tyrells of Highgarden, the Tarlys of Horn Hill and the Martells of Dorne"),
  ("iron", "铁群岛", "The Iron Islands", "派克岛的葛雷乔伊家", "The Greyjoys of Pyke"),
  ("essos", "坦格利安家与厄索斯", "The Targaryens and Essos", "坦格利安家的末裔，以及狭海对岸的追随者与对手",
   "The last Targaryens, and their followers and foes across the Narrow Sea"),
]

# the acts of the timeline are the seasons
ACTS = [dict(a=FIRST[s], b=FIRST[s] + SEASONS[s - 1] - 1, zh=f"第{'一二三四五六七八'[s - 1]}季", en=f"Season {s}",
             zs=f"S{s}", es=f"S{s}") for s in range(1, 9)]

# -------------------------------------------------------------------- checks
CHIP = re.compile(r"\(S(\d)E(\d+)(?:[—–]S(\d)E(\d+))?\)")


def cited(text):
    """Episode numbers cited as (S3E9) or (S3E9—S3E10) chips."""
    out = []
    for m in CHIP.finditer(text):
        out.append(next(n for n, se in SE.items() if se == (int(m.group(1)), int(m.group(2)))))
        if m.group(3):
            out.append(next(n for n, se in SE.items() if se == (int(m.group(3)), int(m.group(4)))))
    return out


_ids = [n["id"] for n in NODES]
assert len(_ids) == len(set(_ids)), "duplicate ids"
_set = set(_ids)
_byid = {n["id"]: n for n in NODES}
_houses_used = set()
for _n in NODES:
    i = _n["id"]
    assert _n["camps"][0][0] == _n["debut"], (i, "first camp must start at debut")
    assert all(_n["camps"][k][0] <= _n["camps"][k + 1][0] for k in range(len(_n["camps"]) - 1)), i
    for c in _n["camps"]:
        assert c[1] in CAMPS, (i, c)
        assert len(c) in (2, 4), (i, c)
    assert _n["grp"] in {g[0] for g in GROUPS}, i
    assert _n["house"] in HOUSES, (i, _n["house"])
    if _n["dies"]:
        assert _n["dies"] >= _n["debut"], i
    if _n["dies"] == PRE:
        assert _n["seen"] is None or _n["seen"] >= _n["debut"], i
    for k in ("subs", "bios"):
        eps = [b[0] for b in _n[k]]
        assert eps == sorted(eps) and len(eps) == len(set(eps)), (i, k, eps)
        assert not eps or eps[0] >= _n["debut"], (i, k, "before debut")
    # spoiler safety: a biography entry may not cite a later episode
    for ep, zh, en in _n["bios"]:
        for c in cited(zh) + cited(en):
            assert c <= ep, (i, "bio entry", code(ep), "cites", code(c))
        assert sorted(cited(zh)) == sorted(cited(en)), (i, code(ep), "zh/en cite different episodes")
    assert _n["bios"], (i, "no biography")
    for a, b in _n["down"]:
        assert a < b, i
_pairs = set()
for _e in EDGES:
    assert _e["s"] in _set and _e["t"] in _set, (_e["s"], _e["t"])
    _k = frozenset((_e["s"], _e["t"]))
    assert _k not in _pairs, ("duplicate edge", _e["s"], _e["t"])
    _pairs.add(_k)
    _chs = [p["ch"] for p in _e["phases"]]
    assert _chs == sorted(_chs) and len(_chs) == len(set(_chs)), (_e["s"], _e["t"], [code(c) for c in _chs])
    for p in _e["phases"]:
        assert p["type"] in EDGE_TYPES, (_e["s"], _e["t"], p["type"])
        for who in (_e["s"], _e["t"]):
            assert p["ch"] >= _byid[who]["debut"], ("phase before debut", who, _e["s"], _e["t"], code(p["ch"]))
_deg = {i: 0 for i in _ids}
for _e in EDGES:
    _deg[_e["s"]] += 1
    _deg[_e["t"]] += 1
assert all(_deg.values()), [i for i, d in _deg.items() if not d]
# the emblems on the seals
assert set(EMBLEMS) == _set, (set(EMBLEMS) ^ _set)
for _n in NODES:
    i, _em = _n["id"], EMBLEMS[_n["id"]]
    _eps = [e for e, _ in _em]
    assert _eps[0] == _n["debut"], (i, "first emblem must be at debut")
    assert _eps == sorted(_eps) and len(_eps) == len(set(_eps)), (i, "emblems", _eps)
    assert all(g in GLYPHS for _, g in _em), i
    assert all(_em[k][1] != _em[k + 1][1] for k in range(len(_em) - 1)), (i, "same emblem twice in a row")
    if _n["dies"]:
        assert _eps[-1] <= _n["dies"], (i, "emblem after death")
for i, g in EM_HOME.items():
    assert g in [x for _, x in EMBLEMS[i]], (i, g)
