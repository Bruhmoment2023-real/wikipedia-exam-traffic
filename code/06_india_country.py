"""Step 6 (robustness R10). India-only page views from Wikimedia's differentially-private
"pageviews per country per project per page" daily files.

  historical files (9 Feb 2017 - 5 Feb 2023): rows released only above 450 views, Laplace noise
  current files    (6 Feb 2023 - today):      rows released above 90 views in India's risk tier, Gaussian noise,
                                              counts only each device's first 10 distinct pages per day
The two regimes are not comparable in level, so each exam year is analysed inside one regime
(baseline days and exam days from the same regime) and 2023 is skipped. To make the regimes
comparable in *selection*, every value below 450 is treated as not released.

Only a sample of days is downloaded (six in the exam window, six in the previous August-September)
because each current file is about 25 MB. Each file is streamed, the India rows for en/hi/kn
Wikipedia are kept in data/cache/country_in/<date>.csv.gz, and the rest is discarded.

Usage:  python 06_india_country.py download     # resumable; about 470 MB of transfer in total
        python 06_india_country.py analyze
"""
import csv, gzip, io, os, sys
import numpy as np
import pandas as pd
from common import DATA, CACHE, RESULTS, session

OUT = CACHE / "country_in"
OUT.mkdir(parents=True, exist_ok=True)
FIRST = {2018: "2018-03-05", 2019: "2019-02-15", 2020: "2020-02-15", 2024: "2024-02-15", 2025: "2025-02-15", 2026: "2026-02-17"}
EXAM_OFFSETS = [-12, -6, 0, 6, 12, 18]
BASE_OFFSETS = [0, 6, 12, 18, 24, 30]          # from 1 August of the previous year
THRESH = 450
RNG = np.random.default_rng(20261013)


def sample_days():
    rows = []
    for y, f in FIRST.items():
        F = pd.Timestamp(f)
        for o in EXAM_OFFSETS:
            rows.append((y, "exam", (F + pd.Timedelta(days=o)).strftime("%Y-%m-%d")))
        for o in BASE_OFFSETS:
            rows.append((y, "base", (pd.Timestamp("%d-08-01" % (y - 1)) + pd.Timedelta(days=o)).strftime("%Y-%m-%d")))
    return pd.DataFrame(rows, columns=["exam_year", "window", "date"])


def url(date):
    d = "country_project_page_historical" if date < "2023-02-06" else "country_project_page"
    return "https://analytics.wikimedia.org/published/datasets/%s/%s.tsv" % (d, date)


def download():
    total = 0
    for r in sample_days().itertuples():
        p = OUT / (r.date + ".csv.gz")
        if p.exists():
            continue
        resp = session().get(url(r.date), stream=True, timeout=300)
        if resp.status_code != 200:
            print("  missing on server:", r.date, resp.status_code, flush=True)
            continue
        resp.raw.decode_content = True
        n = 0
        tmp = str(p) + ".tmp"
        with gzip.open(tmp, "wt", encoding="utf8", newline="") as g:
            w = csv.writer(g)
            for line in io.TextIOWrapper(resp.raw, encoding="utf8", errors="replace"):
                f = line.rstrip("\n").split("\t")
                # columns: country, country_code, project, page_id, page_title, item_id, count
                if len(f) >= 7 and f[1] == "IN" and f[2] in ("en.wikipedia", "hi.wikipedia", "kn.wikipedia"):
                    w.writerow([f[2], f[3], f[4], f[5], f[6]])
                    n += 1
        os.replace(tmp, p)
        total += int(resp.raw.tell())
        print("  %s  India rows kept: %d  (transferred so far: %.0f MB)" % (r.date, n, total / 1e6), flush=True)


def analyze():
    syl = pd.read_csv(DATA / "syllabus_articles.csv", dtype=str).fillna("")
    ctl = pd.read_csv(DATA / "control_articles.csv", dtype=str).fillna("")
    ctl = ctl[ctl.control_set == "A_same_area"]
    grp = {}
    for r in syl.itertuples():
        if r.area in ("SCI", "MAT"):
            grp[r.en_pageid] = "syllabus"
    sm = set(syl[syl.area.isin(["SCI", "MAT"])].en_title)
    for r in ctl.itertuples():
        if r.matched_to in sm:
            grp[str(r.en_pageid)] = "control"
    days = sample_days()
    recs = []
    for r in days.itertuples():
        p = OUT / (r.date + ".csv.gz")
        if not p.exists():
            continue
        d = pd.read_csv(p, header=None, names=["project", "page_id", "title", "qid", "n"], dtype=str)
        d = d[(d.project == "en.wikipedia") & d.page_id.isin(grp.keys())]
        d["n"] = pd.to_numeric(d.n, errors="coerce")
        for x in d.itertuples():
            recs.append((r.exam_year, r.window, r.date, x.page_id, grp[x.page_id], x.n))
    D = pd.DataFrame(recs, columns=["exam_year", "window", "date", "page_id", "group", "n"])
    D.to_csv(RESULTS / "india_country_rows.csv", index=False)
    out = []
    for y in sorted(D.exam_year.unique()):
        dy = D[(D.exam_year == y) & (D.n >= THRESH)]
        nd = days[(days.exam_year == y)].groupby("window").size()
        have = {w: sum((OUT / (d + ".csv.gz")).exists() for d in days[(days.exam_year == y) & (days.window == w)].date) for w in ("exam", "base")}
        piv = dy.pivot_table(index=["page_id", "group"], columns="window", values="n", aggfunc=["mean", "count"])
        if piv.empty or ("count", "exam") not in piv or ("count", "base") not in piv:
            continue
        full = piv[(piv[("count", "exam")] == have["exam"]) & (piv[("count", "base")] == have["base"])]
        U = np.log(full[("mean", "exam")]) - np.log(full[("mean", "base")])
        g = U.reset_index()
        g.columns = ["page_id", "group", "U"]
        s, c = g[g.group == "syllabus"].U.values, g[g.group == "control"].U.values
        row = dict(exam_year=y, regime="historical (>450, Laplace)" if y < 2023 else "current (>90, Gaussian, first 10 pages per device)",
                   days_exam=have["exam"], days_base=have["base"], n_syllabus=len(s), n_control=len(c),
                   uplift_syllabus=s.mean() if len(s) else np.nan, uplift_control=c.mean() if len(c) else np.nan)
        if len(s) >= 5 and len(c) >= 5:
            bs = [RNG.choice(s, len(s)).mean() - RNG.choice(c, len(c)).mean() for _ in range(2000)]
            row.update(gap=s.mean() - c.mean(), ci_lo=np.percentile(bs, 2.5), ci_hi=np.percentile(bs, 97.5))
        # articles seen above the threshold on at least one exam day (how selective the panel is)
        row["n_syllabus_any_exam_day"] = dy[(dy.group == "syllabus") & (dy.window == "exam")].page_id.nunique()
        out.append(row)
    R = pd.DataFrame(out)
    R.round(4).to_csv(RESULTS / "R10_india_only.csv", index=False)
    pd.set_option("display.width", 250); pd.set_option("display.max_columns", 30)
    print(R.round(3).to_string(index=False))


if __name__ == "__main__":
    {"download": download, "analyze": analyze}[sys.argv[1]]()
