# -*- coding: utf-8 -*-
"""Dream of the Red Chamber (红楼梦): characters, relationships, households and verses on a chapter timeline.

Chapter numbers (回) follow the 120-chapter Cheng-Gao text. Chapters 1-80 are Cao Xueqin's; chapters 81-120 are the
continuation published by Cheng Weiyuan and Gao E in 1791. Everything that happens after chapter 80 (a phase of a
relationship, a death, a change of household, the `late` part of a biography) is shown only when the page's
"last forty chapters" switch is on.

The node, edge and verse data live in nodes_*.py, edges_*.py and verses_hl.py; this module assembles and checks them.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "common"))
from tlhelpers import cnum, ref_zh, ref_en  # noqa: E402,F401
from nodes_jia import NODES_JIA  # noqa: E402
from nodes_kin import NODES_KIN  # noqa: E402
from nodes_out import NODES_OUT  # noqa: E402
from edges_a import EDGES_A  # noqa: E402
from edges_b import EDGES_B  # noqa: E402
from verses_hl import VERSES  # noqa: E402

CUT = 80          # last chapter of Cao Xueqin's text
LAST = 120

NODES = NODES_JIA + NODES_KIN + NODES_OUT
EDGES = EDGES_A + EDGES_B

# how each death happened; True = died by violence, suicide or poison, marked with ✕ (illness and old age are not)
DEATH = {
  "fengyuan": ("被薛家豪奴打死", "Beaten to death by Xue Pan’s men", True),
  "jiarui": ("照风月宝鉴而死", "Dies gazing into the Mirror of Love", False),
  "qinkeqing": ("病逝", "Dies of illness", False),
  "linruhai": ("病故扬州", "Dies of illness in Yangzhou", False),
  "qinzhong": ("病逝", "Dies of illness", False),
  "jinchuan": ("投井自尽", "Drowns herself in a well", True),
  "baoer": ("上吊自尽", "Hangs herself", True),
  "jiajing": ("吞服金丹而死", "Poisoned by his own elixir", True),
  "yousanjie": ("自刎", "Cuts her own throat", True),
  "youerjie": ("吞金自逝", "Swallows gold", True),
  "qingwen": ("含冤病死", "Dies of illness, wronged", False),
  "siqi": ("撞墙而死", "Dashes her head against a wall", True),
  "yuanchun": ("薨逝", "Dies in the palace", False),
  "wangziteng": ("途中误药而死", "Dies on the road of a wrong medicine", False),
  "daiyu": ("泪尽而逝", "Dies, her tears all shed", False),
  "xiajingui": ("误服毒汤而死", "Drinks the poison she meant for another", True),
  "yingchun": ("被孙绍祖折磨而死", "Dies of her husband’s cruelty", True),
  "jiamu": ("寿终", "Dies at a great age", False),
  "yuanyang": ("自缢殉主", "Hangs herself to follow her mistress", True),
  "zhaoyiniang": ("中邪暴死", "Dies raving, possessed", True),
  "xifeng": ("病逝", "Dies of illness", False),
  "xiangling": ("难产而死", "Dies in childbirth", False),
}
assert set(DEATH) == {n["id"] for n in NODES if n["dies"]}, set(DEATH) ^ {n["id"] for n in NODES if n["dies"]}
for _n in NODES:
    _n["death"] = DEATH.get(_n["id"])
    _n["verses"] = VERSES.get(_n["id"], [])
    _n.setdefault("late", None)
    _n.setdefault("born", None)

EDGE_TYPES = {
  "kin": dict(zh="亲缘", en="Family", desc="血缘与婚姻", desc_en="Blood and marriage"),
  "love": dict(zh="情缘", en="Love", desc="爱慕、私情与婚约", desc_en="Love, affairs and betrothals"),
  "mas": dict(zh="主仆", en="Service", desc="主子与丫鬟、小厮、奶妈、陪房", desc_en="Masters and mistresses with their maids, pages and nurses"),
  "aid": dict(zh="知交", en="Friendship", desc="姊妹知心、诗社往来、提携与相救", desc_en="Confidences, poetry, patronage and help"),
  "foe": dict(zh="构陷", en="Harm", desc="谋害、欺压与陷害", desc_en="Plots, persecution and cruelty"),
  "tie": dict(zh="纠葛", en="Entangled", desc="猜忌、争执与爱恨交织", desc_en="Jealousy, quarrels and mixed feelings"),
}

# households: the colour of a portrait's border. Guests keep their own family's colour, and so do their maids.
CAMPS = {
  "ning": dict(zh="宁国府", en="Ning mansion"),
  "rong": dict(zh="荣国府", en="Rong mansion"),
  "gong": dict(zh="宫中", en="The palace"),
  "lin": dict(zh="林家", en="The Lins"),
  "shi": dict(zh="史家", en="The Shis"),
  "wang": dict(zh="王家", en="The Wangs"),
  "xue": dict(zh="薛家", en="The Xues"),
  "out": dict(zh="府外", en="Outside"),
  "kong": dict(zh="空门 · 方外", en="Clergy & immortals"),
}

# roster groups
GROUPS = [
  ("ning", "宁国府", "The Ning mansion", "宁国公一脉：贾敬、贾珍、贾蓉三代，尤氏姊妹，以及养在荣府的惜春",
   "The Duke of Ning’s line — three generations of men, the You sisters, and Xichun, raised in the Rong mansion"),
  ("rong", "荣国府", "The Rong mansion", "荣国公一脉：贾母与她的两个儿子，孙辈的姊妹兄弟，以及族中子弟",
   "The Duke of Rong’s line — Grandmother Jia, her two sons, the grandchildren and two poorer clansmen"),
  ("kin", "林 · 史 · 王 · 薛", "The Lins, Shis, Wangs and Xues", "与贾家世代联姻的亲戚——“贾不假，白玉为堂金作马”，四大家族“一损皆损，一荣皆荣”",
   "The families bound to the Jias by marriage — the four great houses that “rise together and fall together”"),
  ("serv", "丫鬟仆妇", "Maids and servants", "丫鬟、小厮、奶妈、陪房和小戏子", "Maids, pages, nurses, stewards’ wives and the young actresses"),
  ("out", "府外与方外", "Outside the walls", "亲友、官员、优伶、僧尼道士，以及在书首书尾出入幻境的仙人",
   "Friends, officials, actors, nuns and priests, and the immortals who open and close the story"),
]

# the story's acts: (first chapter, last chapter); the last two belong to the continuation
ACTS = [
  dict(a=1, b=5, zh="缘起", zs="缘起", en="Origins", es="Origins"),
  dict(a=6, b=16, zh="秦氏之死", zs="秦氏", en="Lady Qin", es="Lady Qin"),
  dict(a=17, b=22, zh="元妃省亲", zs="省亲", en="The visit", es="Visit"),
  dict(a=23, b=36, zh="入住大观园", zs="入园", en="The garden", es="Garden"),
  dict(a=37, b=54, zh="诗社与盛宴", zs="诗社", en="Poetry and feasts", es="Poetry"),
  dict(a=55, b=70, zh="理家与二尤", zs="二尤", en="The You sisters", es="Sisters"),
  dict(a=71, b=80, zh="抄检大观园", zs="抄检", en="The search", es="Search"),
  dict(a=81, b=98, zh="调包与黛玉之死", zs="调包", en="The switch", es="Switch"),
  dict(a=99, b=120, zh="抄家与出家", zs="散场", en="The fall", es="Fall"),
]

# -------------------------------------------------------------------- checks
_ids = [n["id"] for n in NODES]
assert len(_ids) == len(set(_ids)), "duplicate ids"
_set = set(_ids)
for _n in NODES:
    assert _n["camps"][0][0] == _n["debut"], (_n["id"], "first household must start at debut")
    assert all(_n["camps"][i][0] <= _n["camps"][i + 1][0] for i in range(len(_n["camps"]) - 1)), _n["id"]
    for c in _n["camps"]:
        assert c[1] in CAMPS, (_n["id"], c)
        assert len(c) in (2, 4), (_n["id"], c)
    assert _n["grp"] in {g[0] for g in GROUPS}, _n["id"]
    if _n["dies"]:
        assert _n["dies"] >= _n["debut"], _n["id"]
    import re as _re
    for _c in map(int, _re.findall(r"第(\d+)", _n["bio"][0])):
        assert _c <= CUT, (_n["id"], "bio cites a late chapter", _c)
    if _n["late"]:
        for _c in map(int, _re.findall(r"第(\d+)", _n["late"][0])):
            assert _c > CUT, (_n["id"], "late bio cites an early chapter", _c)
    has_late = any(c[0] > CUT for c in _n["camps"]) or (_n["dies"] or 0) > CUT
    assert not has_late or _n["late"], (_n["id"], "late events need a late bio")
_pairs = set()
for _e in EDGES:
    assert _e["s"] in _set and _e["t"] in _set, (_e["s"], _e["t"])
    _k = frozenset((_e["s"], _e["t"]))
    assert _k not in _pairs, ("duplicate edge", _e["s"], _e["t"])
    _pairs.add(_k)
    _chs = [p["ch"] for p in _e["phases"]]
    assert _chs == sorted(_chs), (_e["s"], _e["t"], _chs)
    for p in _e["phases"]:
        assert p["type"] in EDGE_TYPES, (_e["s"], _e["t"], p["type"])
        _byid = {n["id"]: n for n in NODES}
        for who in (_e["s"], _e["t"]):
            assert p["ch"] >= _byid[who]["debut"], ("phase before debut", who, _e["s"], _e["t"], p["ch"])
_deg = {i: 0 for i in _ids}
for _e in EDGES:
    _deg[_e["s"]] += 1
    _deg[_e["t"]] += 1
assert all(_deg.values()), [i for i, d in _deg.items() if not d]
