"""Step 2. Build matched control sets of non-syllabus articles.

Candidate pool: English Wikipedia "Vital articles, Level 4" lists (a community-curated list of about
10,000 important articles, organised by subject). Rule:
  * Control set A (same subject area): candidates from the vital-article lists of the same broad area
    as the syllabus article (SCI = Physical sciences + Biology and health sciences + Technology;
    MAT = Mathematics; SST = History + Geography + Society and social sciences).
  * Control set B (different area): candidates from Arts + Philosophy and religion + Everyday life.
  * A candidate is dropped if it is one of the syllabus articles or if its title (lower-cased) occurs
    anywhere in the text of any of the 14 syllabus documents ("possibly on the syllabus").
  * Matching variable: mean daily views (user traffic, all access) over Jan 2016 - Dec 2019, i.e.
    strictly before the treatment date and before COVID. 1:1 nearest neighbour on log traffic,
    without replacement, processing syllabus articles in a fixed seeded random order.
Nothing after 2019 is read by this script.
Usage:  python 02_build_controls.py
"""
import csv, math, random, re
import pandas as pd
from common import DATA, mw_api, cached_json, get

SEED = 20261013
POOLS = {
    "SCI": ["Physical sciences", "Biology and health sciences", "Technology"],
    "MAT": ["Mathematics"],
    "SST": ["History", "Geography", "Society and social sciences"],
    "OFF": ["Arts", "Philosophy and religion", "Everyday life"],
}
SAMPLE = {"SCI": 1100, "MAT": 10**6, "SST": 350, "OFF": 600}
PV = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/{proj}/all-access/user/{title}/monthly/2016010100/2019123100"


def vital_links(sub):
    def fetch():
        out, cont = [], {}
        while True:
            d = mw_api("en", action="query", titles="Wikipedia:Vital articles/Level 4/" + sub, redirects=1,
                       prop="links", plnamespace=0, pllimit="max", **cont)
            for p in d["query"]["pages"]:
                out += [l["title"] for l in p.get("links", [])]
            if "continue" in d:
                cont = d["continue"]
            else:
                return sorted(set(out))
    return cached_json("vital", sub, fetch)


def pre_traffic(title, proj="en.wikipedia"):
    """Mean daily user views, 2016-2019 (48 months). 0 if the API has no data."""
    def fetch():
        from urllib.parse import quote
        r = get(PV.format(proj=proj, title=quote(title.replace(" ", "_"), safe="")), ok404=True)
        return [] if r is None else [(i["timestamp"], i["views"]) for i in r.json()["items"]]
    items = cached_json("pre_monthly", proj + "|" + title, fetch)
    return sum(v for _, v in items) / 1461.0


def main():
    random.seed(SEED)
    syl = pd.read_csv(DATA / "syllabus_articles.csv", dtype=str).fillna("")
    syl_titles = set(syl.en_title)
    syltext = " ".join(re.sub(r"\s+", " ", p.read_text(encoding="utf8").lower())
                       for p in (DATA / "syllabus").glob("*.txt"))
    cands = {}
    for area, subs in POOLS.items():
        pool = sorted(set(t for s in subs for t in vital_links(s)))
        n0 = len(pool)
        pool = [t for t in pool if t not in syl_titles]
        n1 = len(pool)
        pool = [t for t in pool if re.search(r"(?<![a-z])" + re.escape(t.lower()) + r"(?![a-z])", syltext) is None]
        print(area, "vital-list links:", n0, "| not a syllabus article:", n1, "| title not in syllabus text:", len(pool))
        random.shuffle(pool)
        cands[area] = pool[:SAMPLE[area]]
    # resolve candidates (drop redirects-to-syllabus, disambiguation pages, missing)
    from importlib import import_module
    bt = import_module("01_build_topics")
    allc = [t for v in cands.values() for t in v]
    res = bt.resolve_titles("en", allc)
    rows = []
    for area, v in cands.items():
        for t in v:
            x = res[t]
            if x["missing"] or x["disambig"] or x["canonical"] in syl_titles:
                continue
            rows.append(dict(area=area, en_title=x["canonical"], qid=x["qid"], en_pageid=x["pageid"]))
    cand = pd.DataFrame(rows).drop_duplicates("en_title")
    print("candidates to screen:", len(cand))
    cand["pre_views"] = [pre_traffic(t) for t in cand.en_title]
    syl["pre_views"] = [pre_traffic(t) for t in syl.en_title]
    cand = cand[cand.pre_views > 0]
    cand.to_csv(DATA / "control_candidates.csv", index=False)

    def match(target, pool, label):
        pool = pool.copy()
        pool["lv"] = pool.pre_views.map(math.log)
        used, out = set(), []
        order = list(target.index)
        random.Random(SEED).shuffle(order)
        for i in order:
            t = target.loc[i]
            if t.pre_views <= 0:
                continue
            avail = pool[~pool.en_title.isin(used)]
            if avail.empty:
                break
            j = (avail.lv - math.log(t.pre_views)).abs().idxmin()
            c = avail.loc[j]
            used.add(c.en_title)
            out.append(dict(control_set=label, matched_to=t.en_title, area=t.area, subject=t.subject,
                            en_title=c.en_title, qid=c.qid, en_pageid=c.en_pageid,
                            pre_views=round(c.pre_views, 2), matched_pre_views=round(t.pre_views, 2),
                            log_gap=round(math.log(c.pre_views) - math.log(t.pre_views), 3)))
        return out

    out = []
    for area in ("SCI", "MAT", "SST"):
        out += match(syl[syl.area == area], cand[cand.area == area], "A_same_area")
    out += match(syl.sample(frac=0.5, random_state=SEED), cand[cand.area == "OFF"], "B_other_area")
    ctl = pd.DataFrame(out)
    sl = bt.sitelinks(list(ctl.qid))
    ctl["hi_title"] = [(sl.get(q, ("", ""))[0] or "") for q in ctl.qid]
    ctl["kn_title"] = [(sl.get(q, ("", ""))[1] or "") for q in ctl.qid]
    ctl["rule"] = "1:1 nearest neighbour on log mean daily user views 2016-2019, without replacement, vital-articles level 4 pool"
    ctl.to_csv(DATA / "control_articles.csv", index=False)
    syl.to_csv(DATA / "syllabus_articles.csv", index=False)
    for lab, g in ctl.groupby(["control_set", "area"]):
        print(lab, "n=%d" % len(g), "median |log gap|=%.3f" % g.log_gap.abs().median(),
              "share within 0.25: %.2f" % (g.log_gap.abs() < 0.25).mean(),
              "hi:%d kn:%d" % ((g.hi_title != "").sum(), (g.kn_title != "").sum()))
    print("syllabus n per area:", syl.groupby("area").size().to_dict())


if __name__ == "__main__":
    main()
