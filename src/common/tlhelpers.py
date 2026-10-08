# -*- coding: utf-8 -*-
"""Helpers shared by the timeline books (Three Kingdoms, Red Chamber): node/edge constructors and chapter references."""

N = lambda **k: k


def P(ch, typ, zl, zt, el, et, ref=None):
    return dict(ch=ch, type=typ, zl=zl, zt=zt, el=el, et=et, ref=ref if ref is not None else ch)


def E(s, t, *phases):
    return dict(s=s, t=t, phases=list(phases))


DIG = "零一二三四五六七八九"


def cnum(n):
    """1..120 -> 一 … 一百二十 (一百零五, 一百一十)."""
    if n < 10:
        return DIG[n]
    if n < 20:
        return "十" + (DIG[n % 10] if n % 10 else "")
    if n < 100:
        return DIG[n // 10] + "十" + (DIG[n % 10] if n % 10 else "")
    r = n - 100
    if r == 0:
        return "一百"
    if r < 10:
        return "一百零" + DIG[r]
    return "一百" + cnum(r) if r >= 20 else "一百一" + cnum(r)


def ref_zh(ref):
    """25 -> 第二十五回; (51, 56) -> 第五十一回至五十六回; [8, 22] -> 第八回、第二十二回."""
    items = ref if isinstance(ref, list) else [ref]
    out = []
    for r in items:
        if isinstance(r, tuple):
            out.append(f"第{cnum(r[0])}回至{cnum(r[1])}回")
        else:
            out.append(f"第{cnum(r)}回")
    return "、".join(out)


def ref_en(ref):
    items = ref if isinstance(ref, list) else [ref]
    parts, count = [], 0
    for r in items:
        if isinstance(r, tuple):
            parts.append(f"{r[0]}–{r[1]}")
            count += 2
        else:
            parts.append(str(r))
            count += 1
    return ("Chapters " if count > 1 else "Chapter ") + ", ".join(parts)
