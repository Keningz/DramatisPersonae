# -*- coding: utf-8 -*-
"""Game of Thrones (HBO, 2011-2019): the 73 episodes, numbered 1-73 across the eight seasons.

Every episode also gets a module-level name, S1E1 ... S8E6, so the data files can write P(S3E9, ...) and read naturally.
Chinese titles follow the episode list of the Chinese A Song of Ice and Fire wiki (asoiaf.huijiwiki.com); the five it
leaves in English are given the usual Chinese renderings.
"""
SEASONS = [10, 10, 10, 10, 10, 10, 7, 6]
YEARS = [2011, 2012, 2013, 2014, 2015, 2016, 2017, 2019]

EPISODES = [
  # season 1
  ("凛冬将至", "Winter Is Coming"), ("国王大道", "The Kingsroad"), ("雪诺大人", "Lord Snow"),
  ("残缺之躯", "Cripples, Bastards, and Broken Things"), ("狮狼之争", "The Wolf and the Lion"), ("黄金宝冠", "A Golden Crown"),
  ("不胜则死", "You Win or You Die"), ("剑之尖端", "The Pointy End"), ("贝勒圣堂", "Baelor"), ("血火同源", "Fire and Blood"),
  # season 2
  ("北境不忘", "The North Remembers"), ("夜之国度", "The Night Lands"), ("逝者不死", "What Is Dead May Never Die"),
  ("骸骨花园", "Garden of Bones"), ("古堡幽灵", "The Ghost of Harrenhal"), ("新旧诸神", "The Old Gods and the New"),
  ("毁誉之人", "A Man Without Honor"), ("北国僭主", "The Prince of Winterfell"), ("黑水大战", "Blackwater"),
  ("凡人皆有一死", "Valar Morghulis"),
  # season 3
  ("凡人皆须侍奉", "Valar Dohaeris"), ("黑色翅膀，黑色消息", "Dark Wings, Dark Words"), ("惩罚之旅", "Walk of Punishment"),
  ("至死方休", "And Now His Watch Is Ended"), ("火吻而生", "Kissed by Fire"), ("绝壁攀爬", "The Climb"),
  ("狗熊与美少女", "The Bear and the Maiden Fair"), ("次子", "Second Sons"), ("卡斯特梅的雨季", "The Rains of Castamere"),
  ("弥莎", "Mhysa"),
  # season 4
  ("双剑", "Two Swords"), ("王家婚礼", "The Lion and the Rose"), ("碎镣之人", "Breaker of Chains"), ("守誓之剑", "Oathkeeper"),
  ("托曼一世", "First of His Name"), ("国法家法", "The Laws of Gods and Men"), ("知更展翅", "Mockingbird"),
  ("比武审判", "The Mountain and the Viper"), ("长城守望", "The Watchers on the Wall"), ("万生之子", "The Children"),
  # season 5
  ("战争将至", "The Wars to Come"), ("黑白之院", "The House of Black and White"), ("大麻雀", "High Sparrow"),
  ("鹰身女妖之子", "Sons of the Harpy"), ("杀死男孩", "Kill the Boy"), ("不屈不挠", "Unbowed, Unbent, Unbroken"),
  ("礼物", "The Gift"), ("艰难屯", "Hardhome"), ("魔龙的狂舞", "The Dance of Dragons"), ("圣母慈悲", "Mother’s Mercy"),
  # season 6
  ("红袍祭司", "The Red Woman"), ("家", "Home"), ("破誓者", "Oathbreaker"), ("陌客之书", "Book of the Stranger"),
  ("门", "The Door"), ("吾血之血", "Blood of My Blood"), ("残人", "The Broken Man"), ("无名之辈", "No One"),
  ("私生子之战", "Battle of the Bastards"), ("凛冬的寒风", "The Winds of Winter"),
  # season 7
  ("龙石岛", "Dragonstone"), ("风暴降生", "Stormborn"), ("女王的正义", "The Queen’s Justice"), ("战利品", "The Spoils of War"),
  ("东海望", "Eastwatch"), ("塞外", "Beyond the Wall"), ("龙与狼", "The Dragon and the Wolf"),
  # season 8
  ("临冬城", "Winterfell"), ("七王国的骑士", "A Knight of the Seven Kingdoms"), ("长夜", "The Long Night"),
  ("最后的史塔克", "The Last of the Starks"), ("钟声", "The Bells"), ("铁王座", "The Iron Throne"),
]
assert len(EPISODES) == sum(SEASONS) == 73

SE = {}          # episode number -> (season, episode within the season)
_n = 0
for _s, _cnt in enumerate(SEASONS, 1):
    for _e in range(1, _cnt + 1):
        _n += 1
        SE[_n] = (_s, _e)
        globals()[f"S{_s}E{_e}"] = _n
FIRST = {s: min(n for n, (ss, _) in SE.items() if ss == s) for s in range(1, 9)}
LAST = 73


def code(n):
    s, e = SE[n]
    return f"S{s}E{e}"


def ref_zh(ref):
    """29 -> S3E9《卡斯特梅的雨季》; (29, 30) -> S3E9—S3E10; [5, 29] -> S1E5、S3E9."""
    items = ref if isinstance(ref, list) else [ref]
    out = []
    for r in items:
        if isinstance(r, tuple):
            out.append(f"{code(r[0])}—{code(r[1])}")
        else:
            out.append(f"{code(r)}《{EPISODES[r - 1][0]}》")
    return "、".join(out)


def ref_en(ref):
    items = ref if isinstance(ref, list) else [ref]
    out = []
    for r in items:
        if isinstance(r, tuple):
            out.append(f"{code(r[0])}–{code(r[1])}")
        else:
            out.append(f"{code(r)} “{EPISODES[r - 1][1]}”")
    return ", ".join(out)


__all__ = ["SEASONS", "YEARS", "EPISODES", "SE", "FIRST", "LAST", "code", "ref_zh", "ref_en"] + \
          [f"S{s}E{e}" for s, e in SE.values()]
