"""Extension pulls (PLAN-exploratory E2a, E3). Sequential; waits for the frozen pull (a PID) to finish first.

  python ext_pull.py <pid-to-wait-for>
Writes: ../data/placebo_pairs.csv ; caches into the project's data/cache (same layout as 03_pull_pageviews.py;
agent series under pv_agent/<agent>/).
"""
import sys, os, time, gzip, json, importlib.util
from pathlib import Path
from urllib.parse import quote
import numpy as np
import pandas as pd

PROJ = Path(r"D:\Research-Publishing\05-wikipedia-exam-traffic")
sys.path.insert(0, str(PROJ / "code"))
import common
from common import get, cache_path
spec = importlib.util.spec_from_file_location("pull03", PROJ / "code" / "03_pull_pageviews.py")
pull03 = importlib.util.module_from_spec(spec); spec.loader.exec_module(pull03)
OUT = PROJ / "rework-v3" / "data"
OUT.mkdir(exist_ok=True)

START, END = "2015070100", "2026093000"
URL = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/{agent}/{title}/daily/" + START + "/" + END


def wait_pid(pid):
    import subprocess
    while True:
        r = subprocess.run(["tasklist", "/FI", "PID eq %s" % pid], capture_output=True, text=True).stdout
        if str(pid) not in r:
            return
        time.sleep(60)


def pull_agent(agent, title, counter):
    p = cache_path("pv_agent/" + agent, title, ext=".json.gz")
    if p.exists():
        return
    r = get(URL.format(agent=agent, title=quote(title.replace(" ", "_"), safe="")), ok404=True)
    items = [] if r is None else [[i["timestamp"][:8], i["views"]] for i in r.json()["items"]]
    tmp = str(p) + ".tmp"
    with gzip.open(tmp, "wt") as f:
        json.dump(items, f)
    os.replace(tmp, p)
    counter[0] += 1
    if counter[0] % 250 == 0:
        print("  ext fetched", counter[0], time.strftime("%H:%M:%S"), flush=True)


def choose_placebo():
    ctl = pd.read_csv(PROJ / "data" / "control_articles.csv", dtype=str).fillna("")
    syl = pd.read_csv(PROJ / "data" / "syllabus_articles.csv", dtype=str).fillna("")
    cand = pd.read_csv(PROJ / "data" / "control_candidates.csv")
    used = set(syl.en_title) | set(syl.en_title_mapped) | set(ctl.en_title)
    pool = cand[~cand.en_title.isin(used)].copy()
    pool["lv"] = np.log(pool.pre_views)
    A = ctl[(ctl.control_set == "A_same_area") & ctl.area.isin(["SCI", "MAT"])].copy()
    A["pre_views"] = A.pre_views.astype(float)
    rows, taken = [], set()
    for r in A.sort_values("en_title").itertuples():
        sub = pool[(pool.area == r.area) & ~pool.en_title.isin(taken)]
        if len(sub) == 0:
            rows.append((r.en_title, r.matched_to, r.area, "", np.nan)); continue
        d = (sub.lv - np.log(r.pre_views)).abs()
        j = d.sort_values(kind="mergesort").index[0]
        # ties: alphabetical (mergesort keeps pool order; resolve explicitly)
        best = sub[(d - d.min()).abs() < 1e-12].sort_values("en_title").iloc[0]
        dd = abs(best.lv - np.log(r.pre_views))
        if dd <= 0.25:
            taken.add(best.en_title)
            rows.append((r.en_title, r.matched_to, r.area, best.en_title, dd))
        else:
            rows.append((r.en_title, r.matched_to, r.area, "", dd))
    df = pd.DataFrame(rows, columns=["control_A", "syllabus_article", "area", "placebo_C", "abs_log_diff"])
    df.to_csv(OUT / "placebo_pairs.csv", index=False)
    print("placebo pairs: matched %d of %d; median abs log diff %.4f" % ((df.placebo_C != "").sum(), len(df), df.abs_log_diff[df.placebo_C != ""].median()), flush=True)
    return df


def main():
    if len(sys.argv) > 1:
        wait_pid(sys.argv[1])
    print("start ext pull", time.strftime("%H:%M:%S"), flush=True)
    pl = choose_placebo()
    c = [0]
    # E2a: placebo series, same cache/layout as main pull so 04_build_panel-style loading works
    for t in pl.placebo_C[pl.placebo_C != ""]:
        pull03.pull("en.wikipedia", t, "all-access", c)
    print("placebo series done", time.strftime("%H:%M:%S"), flush=True)
    # E3: automated and all-agents for syllabus + control A (current title)
    syl = pd.read_csv(PROJ / "data" / "syllabus_articles.csv", dtype=str).fillna("")
    ctl = pd.read_csv(PROJ / "data" / "control_articles.csv", dtype=str).fillna("")
    A = ctl[(ctl.control_set == "A_same_area") & ctl.area.isin(["SCI", "MAT"])].sort_values("matched_to")
    rng = np.random.default_rng(20261014)
    pick = A.iloc[np.sort(rng.choice(len(A), 250, replace=False))]          # amendment A2: 250 pairs
    titles = list(pick.matched_to) + list(pick.en_title)
    pd.DataFrame({"title": titles}).to_csv(OUT / "e3_sample_titles.csv", index=False)
    for agent in ("automated", "all-agents"):
        for t in titles:
            pull_agent(agent, t, c)
    print("ext pull done", time.strftime("%H:%M:%S"), flush=True)


if __name__ == "__main__":
    main()
