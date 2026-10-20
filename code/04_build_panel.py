"""Step 4. Assemble cached series into daily article-by-day matrices.

For each language edition, builds an (articles x days) matrix of user page views for
all-access and for desktop, summing the current title and the redirect titles listed in
data/titles_<name>.csv. Output: data/panel_<name>_<lang>.npz and data/panel_<name>_<lang>_index.csv
Usage:  python 04_build_panel.py pilot|full
"""
import gzip, json, sys
import numpy as np
import pandas as pd
from common import DATA
from importlib import import_module

pull = import_module("03_pull_pageviews")
DAYS = pd.date_range("2015-07-01", "2026-09-30", freq="D")
POS = {d.strftime("%Y%m%d"): i for i, d in enumerate(DAYS)}


def load(proj, title, access):
    p = pull.series_path(proj, title, access)
    if not p.exists():
        return None
    v = np.zeros(len(DAYS), dtype=np.float32)
    with gzip.open(p, "rt") as f:
        for d, x in json.load(f):
            if d in POS:
                v[POS[d]] = x
    return v


def main(name):
    tl = pd.read_csv(DATA / ("titles_%s.csv" % name), dtype=str).fillna("")
    accesses = ["all-access", "desktop"] + (["mobile-app"] if name == "pilot" else [])
    for lang, g in tl.groupby("lang"):
        arts = g.drop_duplicates("article")[["article", "group", "en_title", "matched_to", "area"]].reset_index(drop=True)
        mats = {a: np.zeros((len(arts), len(DAYS)), dtype=np.float32) for a in accesses}
        main_share, missing = [], 0
        pos = {a: i for i, a in enumerate(arts.article)}
        tot_main = np.zeros(len(arts)); tot_all = np.zeros(len(arts)); n_red = np.zeros(len(arts), dtype=int)
        complete = np.ones(len(arts), dtype=bool)
        for r in g.itertuples():
            i = pos[r.article]
            for a in accesses:
                v = load(lang + ".wikipedia", r.title, a)
                if v is None:
                    missing += 1
                    if a == "all-access" and r.title == r.article:
                        complete[i] = False
                    continue
                mats[a][i] += v
                if a == "all-access":
                    tot_all[i] += v.sum()
                    if r.title == r.article:
                        tot_main[i] += v.sum()
                    else:
                        n_red[i] += 1
        arts["fetched"] = complete
        arts["n_redirect_titles"] = n_red
        arts["total_views"] = tot_all
        arts["share_on_current_title"] = np.where(tot_all > 0, tot_main / np.maximum(tot_all, 1), np.nan)
        np.savez_compressed(DATA / ("panel_%s_%s.npz" % (name, lang)), **{a.replace("-", "_"): m for a, m in mats.items()})
        arts.to_csv(DATA / ("panel_%s_%s_index.csv" % (name, lang)), index=False)
        print(lang, "articles:", len(arts), "| fetched:", int(complete.sum()), "| series files missing:", missing,
              "| median share of views on current title: %.3f" % np.nanmedian(arts.share_on_current_title),
              "| articles with <90%% on current title: %d" % int((arts.share_on_current_title < 0.9).sum()))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "full")
