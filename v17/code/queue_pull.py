"""Single sequential fetch queue (PLAN-exploratory amendment A3). Resumable: cached series are skipped.
Replaces running 03_pull_pageviews.py --full and ext_pull.py as two processes. Uses the same cache layout, so
04_build_panel.py and 05_analyze.py read the results unchanged.
"""
import sys, time, importlib.util
from pathlib import Path
import numpy as np
import pandas as pd

PROJ = Path(r"D:\Research-Publishing\05-wikipedia-exam-traffic")
sys.path.insert(0, str(PROJ / "code"))
sys.path.insert(0, str(PROJ / "rework-v3" / "code"))
import ext_pull as ep           # choose_placebo, pull_agent, pull03
pull03 = ep.pull03
OUT = PROJ / "rework-v3" / "data"

tl = pd.read_csv(PROJ / "data" / "titles_full.csv", dtype=str).fillna("")
core = tl.area.isin(["SCI", "MAT"]) & tl.group.isin(["syllabus", "A_same_area"])
c = [0]


def run(items, label):
    todo = [x for x in items if not pull03.series_path(*x).exists()]
    print("%s: %d total, %d to fetch  %s" % (label, len(items), len(todo), time.strftime("%H:%M:%S")), flush=True)
    for i, x in enumerate(todo):
        pull03.pull(*x, c)
        if (i + 1) % 100 == 0:
            print("   %s %d/%d  %s" % (label, i + 1, len(todo), time.strftime("%H:%M:%S")), flush=True)


def main():
    for lang in ("hi", "kn"):
        sub = tl[core & (tl.lang == lang)]
        run([(lang + ".wikipedia", r.title, "all-access") for r in sub.itertuples()], lang + " all-access")
    pl = ep.choose_placebo()
    ctl = pd.read_csv(PROJ / "data" / "control_articles.csv", dtype=str).fillna("")
    A = ctl[(ctl.control_set == "A_same_area") & ctl.area.isin(["SCI", "MAT"])].sort_values("matched_to")
    rng = np.random.default_rng(20261014)
    pick = A.iloc[np.sort(rng.choice(len(A), 250, replace=False))]
    pd.DataFrame({"title": list(pick.matched_to) + list(pick.en_title)}).to_csv(OUT / "e3_sample_titles.csv", index=False)
    # stream 1: placebo series in seeded random pair order
    plm = pl[pl.placebo_C != ""].reset_index(drop=True)
    s_placebo = [("en.wikipedia", plm.placebo_C[k], "all-access") for k in np.random.default_rng(20261016).permutation(len(plm))]
    # stream 2: agent series, pairs in random order, both articles, both agents
    order = np.random.default_rng(20261017).permutation(len(pick))
    s_agent = []
    for k in order:
        r = pick.iloc[k]
        for t in (r.matched_to, r.en_title):
            for agent in ("automated", "all-agents"):
                s_agent.append((agent, t))
    # stream 3: desktop in random pair order
    en = tl[core & (tl.lang == "en")]
    syl = en[en.group == "syllabus"].drop_duplicates("article"); ctlr = en[en.group == "A_same_area"].drop_duplicates("matched_to").set_index("matched_to")
    pairs = [(r.article, ctlr.loc[r.matched_to, "article"]) for r in syl.itertuples() if r.matched_to in ctlr.index]
    s_desk = []
    for k in np.random.default_rng(20261015).permutation(len(pairs)):
        for art in pairs[k]:
            for r in en[en.article == art].itertuples():
                s_desk.append(("en.wikipedia", r.title, "desktop"))
    def todo_pv(items): return [x for x in items if not pull03.series_path(*x).exists()]
    def todo_ag(items): return [x for x in items if not ep.cache_path("pv_agent/" + x[0], x[1], ext=".json.gz").exists()]
    streams = {"desktop": [todo_pv(s_desk), lambda x: pull03.pull(*x, c)], "placebo": [todo_pv(s_placebo), lambda x: pull03.pull(*x, c)],
               "agent": [todo_ag(s_agent), lambda x: ep.pull_agent(x[0], x[1], c)]}
    print("streams to fetch:", {k: len(v[0]) for k, v in streams.items()}, time.strftime("%H:%M:%S"), flush=True)
    while any(v[0] for v in streams.values()):
        for k, v in streams.items():
            for _ in range({'agent': 120, 'placebo': 60, 'desktop': 40}[k]):
                if not v[0]: break
                v[1](v[0].pop(0))
            print("  round-robin %s remaining %d  %s" % (k, len(v[0]), time.strftime("%H:%M:%S")), flush=True)
    rest = tl[((tl.area == "SST") & tl.group.isin(["syllabus", "A_same_area"])) | ((tl.group == "B_other_area") & (tl.lang == "en"))]
    run([(r.lang + ".wikipedia", r.title, "all-access") for r in rest.itertuples()], "SST + control B")
    print("queue done", time.strftime("%H:%M:%S"), flush=True)


if __name__ == "__main__":
    main()
