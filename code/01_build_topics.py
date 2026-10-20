"""Step 1. Turn data/topics_raw.txt into data/syllabus_articles.csv.

For every hand-mapped topic: (a) check automatically whether its keyword occurs in the text of the
CBSE syllabus documents of 2020-21 and 2024-25 for that subject; (b) resolve the English Wikipedia
title through the MediaWiki API (following redirects, flagging missing and disambiguation pages);
(c) fetch the Hindi and Kannada titles from Wikidata sitelinks.
Usage:  python 01_build_topics.py
"""
import csv, re, sys
from collections import OrderedDict
from common import DATA, mw_api, chunks, cached_json

SYL = {  # subject -> (2020-21 text file, 2024-25 text file)
    "X-SCI": ("Science_Sec_2020-21.txt", "Science_Sec_2024-25.txt"),
    "X-MAT": ("Mathematics_Sec_2020-21.txt", "Maths_Sec_2024-25.txt"),
    "X-SST": ("Social_Science_Sec_2020-21.txt", "Social_Science_Sec_2024-25.txt"),
    "XII-PHY": ("Physics_Sr.Sec_2020-21.txt", "Physics_SrSec_2024-25.txt"),
    "XII-CHE": ("Chemistry_Sr.Sec_2020-21.txt", "Chemistry_SrSec_2024-25.txt"),
    "XII-BIO": ("Biology_Sr.Sec_2020-21.txt", "Biology_SrSec_2024-25.txt"),
    "XII-MAT": ("Mathematics_Sr.Sec_2020-21.txt", "Maths_SrSec_2024-25.txt"),
}
AREA = {"X-SCI": "SCI", "XII-PHY": "SCI", "XII-CHE": "SCI", "XII-BIO": "SCI",
        "X-MAT": "MAT", "XII-MAT": "MAT", "X-SST": "SST"}


def norm(t):
    t = t.lower().replace("’", "'").replace("‘", "'").replace("–", "-")
    return re.sub(r"\s+", " ", t)


def load_syllabus():
    out = {}
    for s, (a, b) in SYL.items():
        out[s] = tuple(norm((DATA / "syllabus" / f).read_text(encoding="utf8")) for f in (a, b))
    return out


def parse_raw():
    rows, subj, unit = [], None, None
    for line in (DATA / "topics_raw.txt").read_text(encoding="utf8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = re.match(r"\[(.+?)\s*\|\s*(.+?)\]$", line)
        if m:
            subj, unit = m.group(1), m.group(2)
            continue
        kw = None
        if "## kw=" in line:
            line, kw = [x.strip() for x in line.split("## kw=")]
        if "=>" in line:
            topic, title = [x.strip() for x in line.split("=>")]
            rule = "R2 named concept, different wording"
            if title.startswith("~"):
                title, rule = title[1:], "R3 article broader or narrower than topic"
        else:
            topic, title, rule = line, line, "R1 exact title"
        rows.append(dict(subject=subj, area=AREA[subj], unit=unit, topic=topic, en_title_mapped=title,
                         rule=rule, kw=kw or re.escape(topic.lower())))
    return rows


def resolve_titles(lang, titles):
    """title -> dict(canonical, pageid, qid, disambig, missing). Follows redirects."""
    res = {}
    for batch in chunks(sorted(set(titles)), 50):
        key = lang + "|" + "|".join(batch)
        d = cached_json("resolve", key, lambda: mw_api(lang, action="query", titles="|".join(batch),
                                                       redirects=1, prop="pageprops|info",
                                                       ppprop="wikibase_item|disambiguation"))
        q = d["query"]
        nm = {x["from"]: x["to"] for x in q.get("normalized", [])}
        rd = {x["from"]: x["to"] for x in q.get("redirects", [])}
        pages = {p["title"]: p for p in q.get("pages", [])}
        for t in batch:
            t2 = nm.get(t, t)
            t3 = rd.get(t2, t2)
            p = pages.get(t3, {})
            pp = p.get("pageprops", {})
            res[t] = dict(canonical=t3, pageid=p.get("pageid"), qid=pp.get("wikibase_item"),
                          disambig="disambiguation" in pp, missing=p.get("missing", False),
                          redirected=(t2 != t3))
    return res


def sitelinks(qids):
    out = {}
    for batch in chunks(sorted(set(q for q in qids if q)), 50):
        d = cached_json("sitelinks", "|".join(batch),
                        lambda: mw_api("wikidata", action="wbgetentities", ids="|".join(batch),
                                       props="sitelinks", sitefilter="hiwiki|knwiki"))
        for q, e in d.get("entities", {}).items():
            sl = e.get("sitelinks", {})
            out[q] = (sl.get("hiwiki", {}).get("title"), sl.get("knwiki", {}).get("title"))
    return out


def main():
    rows = parse_raw()
    syl = load_syllabus()
    for r in rows:
        old, new = syl[r["subject"]]
        try:
            r["in_syllabus_2020_21"] = int(bool(re.search(r["kw"], old)))
            r["in_syllabus_2024_25"] = int(bool(re.search(r["kw"], new)))
        except re.error as e:
            sys.exit("bad regex %r: %s" % (r["kw"], e))
    res = resolve_titles("en", [r["en_title_mapped"] for r in rows])
    for r in rows:
        x = res[r["en_title_mapped"]]
        r.update(en_title=x["canonical"], en_pageid=x["pageid"], qid=x["qid"],
                 en_missing=int(bool(x["missing"])), en_disambig=int(x["disambig"]),
                 en_redirected=int(x["redirected"]))
    sl = sitelinks([r["qid"] for r in rows])
    for r in rows:
        hi, kn = sl.get(r["qid"], (None, None))
        r["hi_title"], r["kn_title"] = hi or "", kn or ""
        flags = []
        if r["rule"].startswith("R3"):
            flags.append("broader_or_narrower")
        if r["en_disambig"]:
            flags.append("disambiguation_page")
        if r["en_missing"]:
            flags.append("missing")
        if not r["in_syllabus_2020_21"] and not r["in_syllabus_2024_25"]:
            flags.append("keyword_not_in_syllabus_text")
        if r["in_syllabus_2020_21"] and not r["in_syllabus_2024_25"]:
            flags.append("dropped_from_syllabus_by_2024_25")
        if not r["in_syllabus_2020_21"] and r["in_syllabus_2024_25"]:
            flags.append("only_in_2024_25_text")
        r["flags"] = ";".join(flags)
        r["ambiguous"] = int(bool({"broader_or_narrower", "disambiguation_page"} & set(flags)))
    # de-duplicate on the resolved English article: keep the first mapping, note the others
    seen = OrderedDict()
    for r in rows:
        if r["en_missing"]:
            continue
        k = r["en_title"]
        if k in seen:
            seen[k]["also_mapped_from"] += "; %s:%s" % (r["subject"], r["topic"])
            # an article counts as "stable" if any mapping finds it in both syllabus years
            seen[k]["in_syllabus_2020_21"] |= r["in_syllabus_2020_21"]
            seen[k]["in_syllabus_2024_25"] |= r["in_syllabus_2024_25"]
        else:
            r["also_mapped_from"] = ""
            seen[k] = r
    cols = ["subject", "area", "unit", "topic", "en_title", "qid", "en_pageid", "hi_title", "kn_title", "rule",
            "ambiguous", "flags", "in_syllabus_2020_21", "in_syllabus_2024_25", "kw", "en_title_mapped",
            "en_redirected", "also_mapped_from"]
    with open(DATA / "syllabus_articles.csv", "w", newline="", encoding="utf8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(seen.values())
    with open(DATA / "topic_mapping_all_rows.csv", "w", newline="", encoding="utf8") as f:
        w = csv.DictWriter(f, fieldnames=cols[:-1] + ["en_missing", "en_disambig"], extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    n = len(seen)
    v = list(seen.values())
    print("topics mapped:", len(rows), "| unique existing en articles:", n)
    print("missing en titles:", [r["en_title_mapped"] for r in rows if r["en_missing"]])
    print("disambiguation pages:", [r["en_title"] for r in v if r["en_disambig"]])
    print("with hi:", sum(bool(r["hi_title"]) for r in v), "| with kn:", sum(bool(r["kn_title"]) for r in v))
    print("ambiguous:", sum(r["ambiguous"] for r in v))
    for fl in ("keyword_not_in_syllabus_text", "dropped_from_syllabus_by_2024_25", "only_in_2024_25_text"):
        print(fl, sum(fl in r["flags"] for r in v))
    from collections import Counter
    print(Counter(r["subject"] for r in v))


if __name__ == "__main__":
    main()
