"""Step 3. Pull daily page views (agent = user) from the Wikimedia Pageviews API and cache them.

Resumable: every (project, title, access) series is written to its own small gzip file under
data/cache/pv/ and is never requested twice. Requests are strictly sequential with a pause
(common.MIN_INTERVAL) and a descriptive User-Agent, as the API access policy asks.

What is pulled for each article:
  * the current title, plus
  * redirects that may hold part of its traffic. The API counts views under the title that was
    requested, so a renamed article leaves its older views under the old title. For English we take
    every redirect created after mid-June 2015 (page id > 47,000,000: this captures every rename
    inside the data window) and the syllabus wording when the mapping went through a redirect.
    For Hindi and Kannada the pilot takes up to three redirects per article (alphabetical) to measure
    how much traffic sits on redirects; the full pull takes the current title only, to keep the run short.
  * access = all-access and desktop (mobile = all-access minus desktop). With --app the mobile-app
    series is pulled too (used for the pilot only).

Usage:
  python 03_pull_pageviews.py --pilot      # 50 syllabus articles + their controls, en/hi/kn, with app split
  python 03_pull_pageviews.py --full       # everything in data/syllabus_articles.csv and control_articles.csv
  python 03_pull_pageviews.py --full --limit 200   # stop after 200 new requests (for testing)
"""
import argparse, gzip, json, os, sys, time
from urllib.parse import quote
import pandas as pd
from common import DATA, CACHE, get, mw_api, cached_json, cache_path, chunks

START, END = "2015070100", "2026093000"
PV = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/{proj}/{access}/user/{title}/daily/" + START + "/" + END
EN_PAGEID_MID2015 = 47_000_000
PILOT_N, SEED = 50, 20261013


def redirects(lang, titles):
    """title -> list of (redirect title, pageid)."""
    out = {t: [] for t in titles}
    for batch in chunks(sorted(set(titles)), 50):
        def fetch():
            res, cont = {}, {}
            while True:
                d = mw_api(lang, action="query", titles="|".join(batch), prop="redirects",
                           rdlimit="max", rdprop="title|pageid", rdnamespace=0, **cont)
                nm = {x["to"]: x["from"] for x in d["query"].get("normalized", [])}
                for p in d["query"]["pages"]:
                    key = nm.get(p["title"], p["title"])
                    res.setdefault(key, []).extend([r["title"], r["pageid"]] for r in p.get("redirects", []))
                if "continue" in d:
                    cont = d["continue"]
                else:
                    return res
        res = cached_json("redirects", lang + "|" + "|".join(batch), fetch)
        for k, v in res.items():
            out[k] = [tuple(x) for x in v]
    return out


def move_leftovers(lang, titles):
    """Subset of redirect titles whose latest revision is the automatic 'moved page' edit, i.e. the
    redirect is the old name of a renamed article (so it holds the article's earlier page views)."""
    out = set()
    for batch in chunks(sorted(set(titles)), 50):
        d = cached_json("lastrev", lang + "|" + "|".join(batch),
                        lambda: mw_api(lang, action="query", titles="|".join(batch), prop="revisions", rvprop="comment|timestamp"))
        for p in d["query"].get("pages", []):
            for rv in p.get("revisions", []):
                if "moved page" in rv.get("comment", ""):
                    out.add(p["title"])
    return out


def series_path(proj, title, access):
    return cache_path("pv/" + proj + "/" + access, title, ext=".json.gz")


def pull(proj, title, access, counter):
    p = series_path(proj, title, access)
    if p.exists():
        return False
    r = get(PV.format(proj=proj, access=access, title=quote(title.replace(" ", "_"), safe="")), ok404=True)
    items = [] if r is None else [[i["timestamp"][:8], i["views"]] for i in r.json()["items"]]
    tmp = str(p) + ".tmp"
    with gzip.open(tmp, "wt") as f:
        json.dump(items, f)
    os.replace(tmp, p)
    counter[0] += 1
    return True


def article_table(pilot):
    syl = pd.read_csv(DATA / "syllabus_articles.csv", dtype=str).fillna("")
    ctl = pd.read_csv(DATA / "control_articles.csv", dtype=str).fillna("")
    syl["group"] = "syllabus"
    syl["matched_to"] = syl.en_title
    ctl["group"] = ctl.control_set
    ctl["en_title_mapped"] = ctl.en_title
    cols = ["group", "area", "en_title", "en_title_mapped", "hi_title", "kn_title", "matched_to", "qid"]
    df = pd.concat([syl[cols], ctl[cols]], ignore_index=True)
    if pilot:
        keep = set(syl.sample(PILOT_N, random_state=SEED).en_title)
        df = df[df.matched_to.isin(keep)]
    return df


def build_title_list(df, hi_kn_redirect_cap=0):
    """Rows: lang, article (canonical title), title (canonical or redirect), group, en_title, matched_to."""
    rows = []
    red_en = redirects("en", list(df.en_title))
    moved = move_leftovers("en", [t for v in red_en.values() for t, pid in v if pid > EN_PAGEID_MID2015])
    for r in df.itertuples():
        extra = {t for t, pid in red_en.get(r.en_title, []) if pid > EN_PAGEID_MID2015 and t in moved}
        if r.en_title_mapped != r.en_title:
            extra.add(r.en_title_mapped)
        for t in [r.en_title] + sorted(extra - {r.en_title}):
            rows.append(("en", r.en_title, t, r.group, r.en_title, r.matched_to, r.area))
    for lang, col in (("hi", "hi_title"), ("kn", "kn_title")):
        sub = df[(df[col] != "") & (df.group != "B_other_area")]
        red = redirects(lang, list(sub[col]))
        for r in sub.itertuples():
            a = getattr(r, col)
            for t in [a] + sorted({t for t, _ in red.get(a, [])} - {a})[:hi_kn_redirect_cap]:
                rows.append((lang, a, t, r.group, r.en_title, r.matched_to, r.area))
    return pd.DataFrame(rows, columns=["lang", "article", "title", "group", "en_title", "matched_to", "area"]).drop_duplicates(["lang", "title"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pilot", action="store_true")
    ap.add_argument("--full", action="store_true")
    ap.add_argument("--app", action="store_true", help="also pull the mobile-app series")
    ap.add_argument("--limit", type=int, default=10**9)
    a = ap.parse_args()
    if not (a.pilot or a.full):
        sys.exit("choose --pilot or --full")
    df = article_table(a.pilot)
    tl = build_title_list(df, hi_kn_redirect_cap=3 if a.pilot else 0)
    name = "pilot" if a.pilot else "full"
    tl.to_csv(DATA / ("titles_%s.csv" % name), index=False)
    if a.pilot:
        todo = [(r.lang + ".wikipedia", r.title, acc) for r in tl.itertuples()
                for acc in ("all-access", "desktop", "mobile-app")]
    else:
        # Priority order, so that an interrupted run still leaves a usable core:
        #  1 English all-access, science+maths, syllabus + control A   2 same for Hindi, Kannada
        #  3 English desktop for tier 1   4 social science (en, hi, kn all-access)   5 control B   6 English desktop, social science
        core = tl.area.isin(["SCI", "MAT"]) & tl.group.isin(["syllabus", "A_same_area"])
        sst = (tl.area == "SST") & tl.group.isin(["syllabus", "A_same_area"])
        tiers = [(core & (tl.lang == "en"), "all-access"), (core & (tl.lang == "hi"), "all-access"),
                 (core & (tl.lang == "kn"), "all-access"), (core & (tl.lang == "en"), "desktop"),
                 (sst, "all-access"), ((tl.group == "B_other_area") & (tl.lang == "en"), "all-access"),
                 (sst & (tl.lang == "en"), "desktop")]
        todo = [(r.lang + ".wikipedia", r.title, acc) for mask, acc in tiers for r in tl[mask].itertuples()]
        print("tier sizes:", [int(m.sum()) for m, _ in tiers], flush=True)
    n_missing = sum(not series_path(*x).exists() for x in todo)
    print("%s: %d articles, %d titles (incl. redirects), %d series, %d still to fetch"
          % (name, tl.article.nunique(), len(tl), len(todo), n_missing), flush=True)
    counter, t0 = [0], time.time()
    for i, x in enumerate(todo):
        if pull(*x, counter) and counter[0] % 250 == 0:
            el = time.time() - t0
            print("  fetched %d / %d new series, %.0f s elapsed, about %.0f min left"
                  % (counter[0], n_missing, el, (n_missing - counter[0]) * el / counter[0] / 60), flush=True)
        if counter[0] >= a.limit:
            print("stopped at --limit", flush=True)
            break
    print("done: %d new requests in %.0f s" % (counter[0], time.time() - t0), flush=True)


if __name__ == "__main__":
    main()
