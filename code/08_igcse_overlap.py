"""Extension check: how many CBSE-syllabus articles (data/syllabus_articles.csv, kw column) are named in the
Cambridge IGCSE core science syllabi (PDFs in data/igcse/). Keyword = same rule as step 1. Writes data/igcse/overlap.csv."""
import glob, re, pypdf, pandas as pd
from pathlib import Path
D = Path(__file__).resolve().parent.parent / "data"
txt = {}
for f in sorted(glob.glob(str(D / "igcse" / "*.pdf"))):
    r = pypdf.PdfReader(f)
    t = " ".join((p.extract_text() or "") for p in r.pages).lower()
    t = re.sub(r"\s+", " ", t)
    subj = max(["physics", "chemistry", "biology"], key=lambda w: t[:6000].count(w))
    txt[subj] = t; print(Path(f).name, subj, len(t))
a = pd.read_csv(D / "syllabus_articles.csv")
area = {"physics": ["XII-PHY", "X-SCI"], "chemistry": ["XII-CHE", "X-SCI"], "biology": ["XII-BIO", "X-SCI"]}
out = []
for _, r in a.iterrows():
    kw = str(r.kw).replace("\\", "").lower()
    hit = {s: (kw in t) for s, t in txt.items()}
    out.append(dict(en_title=r.en_title, subject=r.subject, kw=kw, **{"igcse_" + s: v for s, v in hit.items()}))
o = pd.DataFrame(out); o.to_csv(D / "igcse" / "overlap.csv", index=False)
for s in txt:
    m = o.subject.str.contains({"physics": "PHY", "chemistry": "CHE", "biology": "BIO"}[s])
    print(s, "CBSE Class 12 articles:", m.sum(), "named in IGCSE text:", int(o.loc[m, "igcse_" + s].sum()))
sci = o[o.subject == "X-SCI"]
print("X-SCI articles:", len(sci), "named in at least one IGCSE science syllabus:", int(sci[[c for c in o if c.startswith("igcse_")]].any(axis=1).sum()))
