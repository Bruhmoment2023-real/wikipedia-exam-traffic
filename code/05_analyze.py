"""Step 5. The analysis fixed in 02a-analysis-plan-FROZEN.md.

Usage:
  python 05_analyze.py full pre     # validation on exam years <= 2020 only (post data masked)
  python 05_analyze.py full all     # the full analysis
  (first argument: pilot or full = which panel to use)
Writes tables to results/ with the stage in the file name.
"""
import sys, json
import numpy as np
import pandas as pd
from itertools import combinations
from common import DATA, RESULTS

DAYS = pd.date_range("2015-07-01", "2026-09-30", freq="D")
FIRST = {2016: "2016-03-01", 2017: "2017-03-09", 2018: "2018-03-05", 2019: "2019-02-15", 2020: "2020-02-15",
         2021: "2021-05-04", 2022: "2022-04-26", 2023: "2023-02-15", 2024: "2024-02-15", 2025: "2025-02-15",
         2026: "2026-02-17"}
PRE, POST = [2017, 2018, 2019, 2020], [2023, 2024, 2025, 2026]
ASIDE = [2016, 2021, 2022]
RNG = np.random.default_rng(20261013)
NBOOT = 2000


def idx(a, b):
    """positions of days a..b inclusive"""
    return np.where((DAYS >= pd.Timestamp(a)) & (DAYS <= pd.Timestamp(b)))[0]


def windows(y, wdef="main", bdef="main"):
    F = pd.Timestamp(FIRST[y])
    if wdef == "main":
        w = idx(F - pd.Timedelta(days=28), F + pd.Timedelta(days=20))
    elif wdef == "late":
        w = idx(F - pd.Timedelta(days=14), F + pd.Timedelta(days=34))
    elif wdef == "calendar":
        w = idx("%d-02-01" % y, "%d-03-31" % y)
    elif wdef.startswith("as"):          # placebo: use another year's month-day for the first exam
        Fp = pd.Timestamp(FIRST[int(wdef[2:])]).replace(year=y)
        w = idx(Fp - pd.Timedelta(days=28), Fp + pd.Timedelta(days=20))
    if bdef == "main":
        b = idx("%d-07-01" % (y - 1), "%d-10-31" % (y - 1))
    elif bdef == "augsep":
        b = idx("%d-08-01" % (y - 1), "%d-09-30" % (y - 1))
    return w, b


def load(name, lang, stage):
    ix = pd.read_csv(DATA / ("panel_%s_%s_index.csv" % (name, lang)), dtype={"article": str}).fillna("")
    z = np.load(DATA / ("panel_%s_%s.npz" % (name, lang)))
    m = {"all": z["all_access"].astype(float), "desktop": z["desktop"].astype(float)}
    m["mobile"] = np.clip(m["all"] - m["desktop"], 0, None)
    nodesk = m["desktop"].sum(1) == 0          # desktop series not pulled (yet) for this article: leave out of R5
    m["desktop"][nodesk] = np.nan; m["mobile"][nodesk] = np.nan
    if stage == "pre":                    # blinding: nothing after 30 June 2020 can be read
        cut = idx("2020-07-01", "2026-09-30")
        for k in m:
            m[k][:, cut] = np.nan
    return ix, m


def uplift(mat, years, wdef="main", bdef="main", geo=False):
    U = np.full((mat.shape[0], len(years)), np.nan)
    base = np.full_like(U, np.nan)
    for j, y in enumerate(years):
        w, b = windows(y, wdef, bdef)
        if geo:
            U[:, j] = np.log1p(mat[:, w]).mean(1) - np.log1p(mat[:, b]).mean(1)
        else:
            mw, mb = mat[:, w].mean(1), mat[:, b].mean(1)
            with np.errstate(divide="ignore", invalid="ignore"):
                U[:, j] = np.log(mw) - np.log(mb)
        base[:, j] = mat[:, b].mean(1)
    U[~np.isfinite(U)] = np.nan
    return U, base


def pairs(ix, control="A_same_area", areas=("SCI", "MAT"), keep=None):
    """list of (row of syllabus article, row of its control)"""
    syl = ix[(ix.group == "syllabus") & ix.area.isin(areas) & ix.fetched]
    ctl = ix[(ix.group == control) & ix.fetched].drop_duplicates("matched_to").set_index("matched_to")
    out = []
    for i, r in syl.iterrows():
        if keep is not None and r.en_title not in keep:
            continue
        if r.matched_to in ctl.index:
            out.append((i, ix.index[ix.article == ctl.loc[r.matched_to, "article"]][0]))
    return np.array(out, dtype=int).reshape(-1, 2)


def perm_p(vals_pre, vals_post):
    """one-sided exact permutation p-value that mean(post) - mean(pre) is this low or lower"""
    allv = np.array(list(vals_pre) + list(vals_post))
    n, k = len(allv), len(vals_post)
    obs = np.mean(vals_post) - np.mean(vals_pre)
    cnt = tot = 0
    for c in combinations(range(n), k):
        m = np.zeros(n, bool); m[list(c)] = True
        tot += 1
        cnt += (allv[m].mean() - allv[~m].mean()) <= obs + 1e-12
    return cnt / tot, tot


def article_level(ix, mat, years, pre, post, P, min_base=5.0, **kw):
    """returns dict with per-year table and the pre/post contrast"""
    U, base = uplift(mat, years, **kw)
    use_years = [y for y in years if y in pre + post]
    cols = [years.index(y) for y in use_years]
    ok = np.all(base[P[:, 0]][:, cols] >= min_base, axis=1) & np.all(base[P[:, 1]][:, cols] >= min_base, axis=1) \
        & np.all(np.isfinite(U[P[:, 0]][:, cols]), axis=1) & np.all(np.isfinite(U[P[:, 1]][:, cols]), axis=1)
    Pk = P[ok]
    if len(Pk) < 5:
        return dict(n_pairs=int(len(Pk)), rows=[], D=None)
    Us, Uc = U[Pk[:, 0]], U[Pk[:, 1]]
    G = Us - Uc
    boot = RNG.integers(0, len(Pk), size=(NBOOT, len(Pk)))
    rows = []
    for j, y in enumerate(years):
        g = G[:, j]
        if np.all(np.isnan(g)):
            continue
        bs = np.nanmean(g[boot], axis=1)
        rows.append(dict(year=y, role="pre" if y in pre else "post" if y in post else "set aside",
                         n_pairs=int(np.isfinite(g).sum()), uplift_syllabus=np.nanmean(Us[:, j]),
                         uplift_control=np.nanmean(Uc[:, j]), gap=np.nanmean(g), ci_lo=np.percentile(bs, 2.5),
                         ci_hi=np.percentile(bs, 97.5), median_gap=np.nanmedian(g)))
    out = dict(n_pairs=int(len(Pk)), rows=rows, D=None, Pk=Pk, G=G)
    if post and all(y in years for y in post):
        jp, jq = [years.index(y) for y in pre], [years.index(y) for y in post]
        d_pair = G[:, jq].mean(1) - G[:, jp].mean(1)
        bs = d_pair[boot].mean(1)
        gy_pre, gy_post = G[:, jp].mean(0), G[:, jq].mean(0)
        p, tot = perm_p(gy_pre, gy_post)
        # pre-trend: slope of yearly gap over pre years; dose: slope over post years
        out.update(D=float(d_pair.mean()), D_lo=float(np.percentile(bs, 2.5)), D_hi=float(np.percentile(bs, 97.5)),
                   perm_p_one_sided=p, perm_splits=tot, d_pair=d_pair,
                   pre_slope=float(np.polyfit(pre, gy_pre, 1)[0]), post_slope=float(np.polyfit(post, gy_post, 1)[0]),
                   share_pairs_negative=float((d_pair < 0).mean()))
    return out


def pooled(ix, mat, years, pre, post, P, **kw):
    rows = []
    def gap(Pb):
        res = []
        for y in years:
            w, b = windows(y, kw.get("wdef", "main"), kw.get("bdef", "main"))
            s = np.log(mat[Pb[:, 0]][:, w].sum() / len(w)) - np.log(mat[Pb[:, 0]][:, b].sum() / len(b))
            c = np.log(mat[Pb[:, 1]][:, w].sum() / len(w)) - np.log(mat[Pb[:, 1]][:, b].sum() / len(b))
            res.append((s, c))
        return np.array(res)
    g0 = gap(P)
    bs = np.array([gap(P[RNG.integers(0, len(P), len(P))]) for _ in range(400)])
    gb = bs[:, :, 0] - bs[:, :, 1]
    for j, y in enumerate(years):
        rows.append(dict(year=y, role="pre" if y in pre else "post" if y in post else "set aside", n_pairs=len(P),
                         uplift_syllabus=g0[j, 0], uplift_control=g0[j, 1], gap=g0[j, 0] - g0[j, 1],
                         ci_lo=np.nanpercentile(gb[:, j], 2.5), ci_hi=np.nanpercentile(gb[:, j], 97.5)))
    out = dict(n_pairs=len(P), rows=rows, D=None)
    if post and all(y in years for y in post):
        jp, jq = [years.index(y) for y in pre], [years.index(y) for y in post]
        g = g0[:, 0] - g0[:, 1]
        d = gb[:, jq].mean(1) - gb[:, jp].mean(1)
        p, tot = perm_p(g[jp], g[jq])
        out.update(D=float(g[jq].mean() - g[jp].mean()), D_lo=float(np.nanpercentile(d, 2.5)),
                   D_hi=float(np.nanpercentile(d, 97.5)), perm_p_one_sided=p, perm_splits=tot)
    return out


def event_study(ix, mat, years, Pk, ref=2020):
    """two-way fixed effects regression with pair-clustered standard errors (statsmodels)."""
    import statsmodels.api as sm
    U, _ = uplift(mat, years)
    recs = []
    for k, (s, c) in enumerate(Pk):
        for j, y in enumerate(years):
            recs.append((k, 2 * k, y, 1, U[s, j])); recs.append((k, 2 * k + 1, y, 0, U[c, j]))
    d = pd.DataFrame(recs, columns=["pair", "art", "year", "syl", "U"]).dropna()
    d["U_dm"] = d.U - d.groupby("art").U.transform("mean")
    X = pd.DataFrame(index=d.index)
    for y in years:
        if y != ref:
            X["yr%d" % y] = (d.year == y).astype(float)
            X["syl_x_%d" % y] = ((d.year == y) & (d.syl == 1)).astype(float)
    X = X - X.groupby(d.art).transform("mean")
    fit = sm.OLS(d.U_dm, X).fit(cov_type="cluster", cov_kwds={"groups": d.pair})
    return [dict(year=y, beta=fit.params["syl_x_%d" % y], se=fit.bse["syl_x_%d" % y],
                 ci_lo=fit.conf_int().loc["syl_x_%d" % y, 0], ci_hi=fit.conf_int().loc["syl_x_%d" % y, 1])
            for y in years if y != ref]


def eve_spike(ix, mat, stage):
    """Secondary outcome: views on the three days before a subject's paper against the surrounding weeks."""
    ed = pd.read_csv(DATA / "exam_dates.csv", dtype=str).fillna("")
    syl = pd.read_csv(DATA / "syllabus_articles.csv", dtype=str).fillna("").set_index("en_title")
    subj_event = {"X-SCI": ("X", "science"), "X-MAT": ("X", "mathematics"), "X-SST": ("X", "social_science"),
                  "XII-PHY": ("XII", "physics"), "XII-CHE": ("XII", "chemistry"), "XII-BIO": ("XII", "biology"),
                  "XII-MAT": ("XII", "mathematics")}
    rows, crow, all_d = [], [], []
    for subj, (cl, ev) in subj_event.items():
        P = pairs(ix, areas=("SCI", "MAT", "SST"), keep=set(syl.index[syl.subject == subj]))
        if len(P) == 0:
            continue
        per_pair = {}                      # pair row -> {year: gap}
        for r in ed[(ed["class"] == cl) & (ed.event == ev)].itertuples():
            y = int(r.exam_year)
            if stage == "pre" and y > 2020:
                continue
            D = pd.Timestamp(r.date)
            eve = idx(D - pd.Timedelta(days=3), D - pd.Timedelta(days=1))
            ref = np.concatenate([idx(D - pd.Timedelta(days=24), D - pd.Timedelta(days=11)),
                                  idx(D + pd.Timedelta(days=4), D + pd.Timedelta(days=17))])
            with np.errstate(divide="ignore", invalid="ignore"):
                S = np.log(mat[:, eve].mean(1)) - np.log(mat[:, ref].mean(1))
            ok = (mat[P[:, 0]][:, ref].mean(1) >= 5) & (mat[P[:, 1]][:, ref].mean(1) >= 5) & np.isfinite(S[P[:, 0]]) & np.isfinite(S[P[:, 1]])
            g = S[P[ok, 0]] - S[P[ok, 1]]
            if len(g) < 5:
                continue
            for k, v in zip(P[ok, 0], g):
                per_pair.setdefault(int(k), {})[y] = v
            bs = g[RNG.integers(0, len(g), (NBOOT, len(g)))].mean(1)
            rows.append(dict(subject=subj, year=y, paper_date=r.date, n_pairs=len(g), spike_syllabus=S[P[ok, 0]].mean(),
                             spike_control=S[P[ok, 1]].mean(), gap=g.mean(), ci_lo=np.percentile(bs, 2.5),
                             ci_hi=np.percentile(bs, 97.5), date_verification=r.verification[:30]))
        # amendment A1: pre/post contrast of the eve-of-paper gap
        d = np.array([np.mean([v for y, v in g.items() if y >= 2023]) - np.mean([v for y, v in g.items() if 2017 <= y <= 2020])
                      for g in per_pair.values()
                      if any(y >= 2023 for y in g) and any(2017 <= y <= 2020 for y in g)])
        if len(d) >= 5:
            bs = d[RNG.integers(0, len(d), (NBOOT, len(d)))].mean(1)
            crow.append(dict(subject=subj, n_pairs=len(d), D_eve=d.mean(), lo=np.percentile(bs, 2.5), hi=np.percentile(bs, 97.5),
                             share_pairs_negative=(d < 0).mean()))
            all_d.append((subj, d))
    for label, keep in (("ALL subjects pooled", None), ("Science and maths pooled", ("X-SCI", "X-MAT", "XII-PHY", "XII-CHE", "XII-BIO", "XII-MAT"))):
        dd = [d for s_, d in all_d if keep is None or s_ in keep]
        if dd:
            d = np.concatenate(dd)
            bs = d[RNG.integers(0, len(d), (NBOOT, len(d)))].mean(1)
            crow.append(dict(subject=label, n_pairs=len(d), D_eve=d.mean(), lo=np.percentile(bs, 2.5), hi=np.percentile(bs, 97.5),
                             share_pairs_negative=(d < 0).mean()))
    pd.DataFrame(crow).round(4).to_csv(RESULTS / ("secondary_eve_contrast_%s.csv" % stage), index=False)
    return pd.DataFrame(rows)


def fmt(res, label):
    df = pd.DataFrame(res["rows"])
    if len(df):
        df.insert(0, "spec", label)
    return df


def main(name, stage):
    years = [2016, 2017, 2018, 2019, 2020] if stage == "pre" else list(range(2016, 2027))
    pre, post = PRE, ([] if stage == "pre" else POST)
    syl = pd.read_csv(DATA / "syllabus_articles.csv", dtype=str).fillna("")
    strict = set(syl[(syl.in_syllabus_2020_21 == "1") & (syl.in_syllabus_2024_25 == "1") & (syl.ambiguous == "0")].en_title)
    yearly, contrasts, es_rows = [], [], []

    def run(label, lang, ix, mat, P, pre_=None, post_=None, yrs=None, pooled_too=False, **kw):
        pre_, post_ = pre_ or pre, (post if post_ is None else post_)
        yrs = yrs or years
        r = article_level(ix, mat, yrs, pre_, post_, P, **kw)
        d = fmt(r, label);
        if len(d):
            d.insert(1, "lang", lang); d.insert(2, "estimator", "article-level"); yearly.append(d)
        c = dict(spec=label, lang=lang, estimator="article-level", n_pairs=r["n_pairs"])
        for k in ("D", "D_lo", "D_hi", "perm_p_one_sided", "perm_splits", "pre_slope", "post_slope", "share_pairs_negative"):
            c[k] = r.get(k)
        contrasts.append(c)
        if pooled_too and len(P) >= 5:
            rp = pooled(ix, mat, yrs, pre_, post_, P, **{k: v for k, v in kw.items() if k in ("wdef", "bdef")})
            d = fmt(rp, label); d.insert(1, "lang", lang); d.insert(2, "estimator", "pooled"); yearly.append(d)
            c = dict(spec=label, lang=lang, estimator="pooled", n_pairs=rp["n_pairs"])
            for k in ("D", "D_lo", "D_hi", "perm_p_one_sided", "perm_splits"):
                c[k] = rp.get(k)
            contrasts.append(c)
        return r

    store = {}
    for lang in ("en", "hi", "kn"):
        try:
            ix, m = load(name, lang, stage)
        except FileNotFoundError:
            continue
        P = pairs(ix)
        r = run("MAIN science+maths, control A, all access", lang, ix, m["all"], P, pooled_too=True)
        store[lang] = (ix, r)
        if r.get("Pk") is not None and len(r["Pk"]) >= 20:
            for e in event_study(ix, m["all"], [y for y in years if y not in (ASIDE if stage != "pre" else [2016])], r["Pk"]):
                e.update(lang=lang); es_rows.append(e)
        run("R9 social science only", lang, ix, m["all"], pairs(ix, areas=("SST",)), pooled_too=True)
        if lang != "en":
            continue
        if stage != "pre":
            run("R1 drop 2020", lang, ix, m["all"], P, pre_=[2017, 2018, 2019])
            run("R2 add 2016 and 2022", lang, ix, m["all"], P, pre_=[2016, 2017, 2018, 2019, 2020], post_=[2022, 2023, 2024, 2025, 2026])
        run("R3 control set B (other areas)", lang, ix, m["all"], pairs(ix, control="B_other_area"))
        run("R4 strict syllabus list (in both syllabus years, unambiguous)", lang, ix, m["all"], pairs(ix, keep=strict))
        run("R5a desktop only", lang, ix, m["desktop"], P)
        run("R5b mobile only", lang, ix, m["mobile"], P)
        run("R6a window F-14..F+34", lang, ix, m["all"], P, wdef="late")
        run("R6b fixed calendar window 1 Feb-31 Mar", lang, ix, m["all"], P, wdef="calendar")
        run("R6c baseline Aug-Sep", lang, ix, m["all"], P, bdef="augsep")
        run("R7 geometric mean", lang, ix, m["all"], P, geo=True)
        for subj in sorted(syl.subject.unique()):
            run("R8 subject " + subj, lang, ix, m["all"], pairs(ix, areas=("SCI", "MAT", "SST"), keep=set(syl[syl.subject == subj].en_title)))
        # V2: does the peak follow the exam date?  own window versus the other regime's window
        v2 = []
        for y in [2017, 2018, 2019, 2020]:
            other = "as2019" if y in (2017, 2018) else "as2017"
            a = article_level(ix, m["all"], [y], [y], [], P)
            b = article_level(ix, m["all"], [y], [y], [], P, wdef=other)
            if a["rows"] and b["rows"]:
                v2.append(dict(year=y, gap_own_window=a["rows"][0]["gap"], own_lo=a["rows"][0]["ci_lo"], own_hi=a["rows"][0]["ci_hi"],
                               gap_other_regime_window=b["rows"][0]["gap"], other_lo=b["rows"][0]["ci_lo"], other_hi=b["rows"][0]["ci_hi"],
                               other_window_anchor="15 Feb" if other == "as2019" else "9 Mar"))
        pd.DataFrame(v2).to_csv(RESULTS / ("V2_peak_follows_exam_date_%s.csv" % stage), index=False)
        eve_spike(ix, m["all"], stage).to_csv(RESULTS / ("secondary_eve_of_paper_%s_%s.csv" % (name, stage)), index=False)

    # H3: language contrast on pairs present in both editions
    if stage != "pre" and "en" in store:
        for lang in ("hi", "kn"):
            if lang not in store or store[lang][1].get("d_pair") is None or store["en"][1].get("d_pair") is None:
                continue
            ixe, re_ = store["en"]; ixl, rl = store[lang]
            de = {ixe.en_title[i]: v for i, v in zip(re_["Pk"][:, 0], re_["d_pair"])}
            dl = {ixl.en_title[i]: v for i, v in zip(rl["Pk"][:, 0], rl["d_pair"])}
            common = sorted(set(de) & set(dl))
            if len(common) >= 5:
                diff = np.array([de[k] - dl[k] for k in common])
                bs = diff[RNG.integers(0, len(diff), (NBOOT, len(diff)))].mean(1)
                contrasts.append(dict(spec="H3 D(en) - D(%s), pairs in both editions" % lang, lang="en-" + lang,
                                      estimator="article-level", n_pairs=len(common), D=float(diff.mean()),
                                      D_lo=float(np.percentile(bs, 2.5)), D_hi=float(np.percentile(bs, 97.5))))
    Y = pd.concat(yearly, ignore_index=True) if yearly else pd.DataFrame()
    Y.round(4).to_csv(RESULTS / ("yearly_gaps_%s_%s.csv" % (name, stage)), index=False)
    C = pd.DataFrame(contrasts)
    C.round(4).to_csv(RESULTS / ("contrasts_%s_%s.csv" % (name, stage)), index=False)
    pd.DataFrame(es_rows).round(4).to_csv(RESULTS / ("event_study_regression_%s_%s.csv" % (name, stage)), index=False)
    pd.set_option("display.width", 250); pd.set_option("display.max_rows", 400); pd.set_option("display.max_columns", 30)
    print("=== yearly gaps, main spec ===")
    print(Y[Y.spec.str.startswith("MAIN")].round(3).to_string(index=False))
    print("=== contrasts ===")
    print(C.round(3).to_string(index=False))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
