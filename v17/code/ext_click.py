"""E5 clickstream (PLAN-exploratory). python ext_click.py filter   |   python ext_click.py analyze
filter : stream each monthly enwiki clickstream file, keep rows whose curr (or prev) is a main-sample article.
analyze: classes SEARCH / DIRECT / LINK / OTHER, uplift Feb(y) vs Oct(y-1), group gaps with pair bootstrap.
"""
import sys, importlib.util
from pathlib import Path
import numpy as np
import pandas as pd

PROJ = Path(r"D:\Research-Publishing\05-wikipedia-exam-traffic")
CS = PROJ / "rework-v3" / "clickstream"
FIL = CS / "filtered"; FIL.mkdir(exist_ok=True)
RES = PROJ / "rework-v3" / "results"
MONTHS = ["2018-10", "2019-02", "2019-10", "2020-02", "2022-10", "2023-02", "2023-10", "2024-02", "2024-10", "2025-02", "2025-10", "2026-02"]
sys.path.insert(0, str(PROJ / "code"))
spec = importlib.util.spec_from_file_location("an", PROJ / "code" / "05_analyze.py")
an = importlib.util.module_from_spec(spec); spec.loader.exec_module(an)


def pairs_titles():
    ix, m = an.load("full", "en", "all")
    P = an.pairs(ix)
    t = lambda i: ix.article.iloc[i].replace(" ", "_")
    return ix, m, P, [(t(a), t(b)) for a, b in P]


def do_filter():
    ix, m, P, pt = pairs_titles()
    keep = set(x for p in pt for x in p)
    print("articles in sample:", len(keep), flush=True)
    for mo in MONTHS:
        out = FIL / ("%s.csv.gz" % mo)
        f = CS / ("clickstream-enwiki-%s.tsv.gz" % mo)
        if out.exists() or not f.exists():
            continue
        parts = []
        for ch in pd.read_csv(f, sep="\t", header=None, names=["prev", "curr", "type", "n"], quoting=3, chunksize=3_000_000,
                              dtype={"prev": str, "curr": str, "type": str, "n": np.int64}, keep_default_na=False):
            sel = ch[ch.curr.isin(keep) | (ch.prev.isin(keep) & (ch.type == "link"))]
            parts.append(sel)
        d = pd.concat(parts); d.to_csv(out, index=False)
        print(mo, "rows kept", len(d), flush=True)


def cls(prev, typ):
    if prev == "other-search": return "SEARCH"
    if prev == "other-empty": return "DIRECT"
    if typ == "link": return "LINK"
    return "OTHER"


def do_analyze():
    seed = np.random.default_rng(20261013 + 7)
    ix, m, P, pt = pairs_titles()
    rr = an.article_level(ix, m["all"], list(range(2016, 2027)), an.PRE, an.POST, P)      # inclusion rule -> the 711 main pairs
    P = rr["Pk"]; t_ = lambda i: ix.article.iloc[i].replace(" ", "_"); pt = [(t_(a), t_(b)) for a, b in P]
    syl = np.array([a for a, b in pt]); ctl = np.array([b for a, b in pt])
    idx = {t: i for i, t in enumerate(list(syl) + list(ctl))}
    npair = len(pt)
    C = ["SEARCH", "DIRECT", "LINK", "OTHER", "ALL"]
    counts = {}      # month -> array (class, 2*npair)  [first npair syllabus, last npair control]
    top = {}
    for mo in MONTHS:
        f = FIL / ("%s.csv.gz" % mo)
        d = pd.read_csv(f, keep_default_na=False, dtype={"prev": str, "curr": str, "type": str})
        inc = d[d.curr.isin(idx)].copy()
        inc["cls"] = [cls(p, t) for p, t in zip(inc.prev, inc.type)]
        arr = np.zeros((len(C), 2 * npair))
        for c in C[:4]:
            s = inc[inc.cls == c].groupby("curr").n.sum()
            for t, v in s.items():
                i = idx[t]; arr[C.index(c), i if i < npair else npair + (i - npair)] += v
        arr[4] = arr[:4].sum(0)
        counts[mo] = arr
        if mo in ("2019-10", "2020-02", "2023-10", "2024-02", "2025-02", "2026-02"):
            sy = set(syl)
            link = inc[(inc.cls == "LINK") & inc.curr.isin(sy)]
            top[(mo, "in")] = link.groupby("prev").n.sum().sort_values(ascending=False).head(15)
            top[(mo, "share_from_syllabus")] = link[link.prev.isin(sy)].n.sum() / max(link.n.sum(), 1)
            out = d[(d.type == "link") & d.prev.isin(sy)]
            top[(mo, "out")] = out.groupby("curr").n.sum().sort_values(ascending=False).head(15)
            top[(mo, "out_share_to_syllabus")] = out[out.curr.isin(sy)].n.sum() / max(out.n.sum(), 1)
    days = {mo: (31 if mo.endswith("-10") else (29 if mo in ("2020-02", "2024-02") else 28)) for mo in MONTHS}
    rows = []
    boot = seed.integers(0, npair, size=(1000, npair))
    def up(arr_f, arr_o, df_, do_, sel, c):
        sf, so = arr_f[c, sel].sum() / df_, arr_o[c, sel].sum() / do_
        return np.log(sf) - np.log(so)
    for y in (2019, 2020, 2023, 2024, 2025, 2026):
        fe, bo = "%d-02" % y, "%d-10" % (y - 1)
        for ci, c in enumerate(C):
            def gap(sel_s, sel_c):
                us = np.log(counts[fe][ci, sel_s].sum() / days[fe]) - np.log(counts[bo][ci, sel_s].sum() / days[bo])
                uc = np.log(counts[fe][ci, sel_c].sum() / days[fe]) - np.log(counts[bo][ci, sel_c].sum() / days[bo])
                return us, uc
            s_all, c_all = np.arange(npair), npair + np.arange(npair)
            us, uc = gap(s_all, c_all)
            bs = []
            for b in boot:
                with np.errstate(all="ignore"):
                    a, bb = gap(b, npair + b)
                bs.append(a - bb)
            rows.append(dict(year=y, cls=c, uplift_syllabus=us, uplift_control=uc, gap=us - uc,
                             ci_lo=np.nanpercentile(bs, 2.5), ci_hi=np.nanpercentile(bs, 97.5),
                             feb_count_syl=counts[fe][ci, :npair].sum(), oct_count_syl=counts[bo][ci, :npair].sum()))
    R = pd.DataFrame(rows).round(4); R.to_csv(RES / "E5_clickstream_gaps.csv", index=False)
    # class shares
    sh = []
    for mo in MONTHS:
        for g, sl in (("syllabus", slice(0, npair)), ("control", slice(npair, 2 * npair))):
            tot = counts[mo][4, sl].sum()
            sh.append(dict(month=mo, group=g, **{c + "_share": counts[mo][i, sl].sum() / tot for i, c in enumerate(C[:4])}, total_per_day=tot / days[mo]))
    pd.DataFrame(sh).round(4).to_csv(RES / "E5_clickstream_class_shares.csv", index=False)
    # coverage vs Pageviews (user, all-access, same articles) per month
    cov = []
    for mo in MONTHS:
        yy, mm = int(mo[:4]), int(mo[5:])
        sl = an.idx("%d-%02d-01" % (yy, mm), (pd.Timestamp("%d-%02d-01" % (yy, mm)) + pd.offsets.MonthEnd(0)).strftime("%Y-%m-%d"))
        for g, col in (("syllabus", 0), ("control", 1)):
            pv = m["all"][P[:, col]][:, sl].sum()
            cs_ = counts[mo][4, :npair].sum() if g == "syllabus" else counts[mo][4, npair:].sum()
            cov.append(dict(month=mo, group=g, clickstream_total=cs_, pageviews_total=pv, coverage=cs_ / pv))
    pd.DataFrame(cov).round(4).to_csv(RES / "E5_clickstream_coverage.csv", index=False)
    with open(RES / "E5_clickstream_top_pages.txt", "w", encoding="utf8") as f:
        for k, v in top.items():
            f.write("== %s %s\n%s\n" % (k[0], k[1], v.to_string() if hasattr(v, "to_string") else "%.4f" % v))
    print(R.pivot(index="year", columns="cls", values="gap").round(3).to_string())
    print(pd.DataFrame(cov).round(3).to_string())


if __name__ == "__main__":
    {"filter": do_filter, "analyze": do_analyze}[sys.argv[1]]()
