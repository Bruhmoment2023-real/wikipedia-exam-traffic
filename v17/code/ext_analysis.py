"""Exploratory extensions E1, E2, E3, E4, E6 (see ../PLAN-exploratory.md). Run: python ext_analysis.py <e1 e2b e4 e6 e2a e3 ...>

Uses the frozen pipeline's own functions (05_analyze.py) unchanged; only adds the placebo window definition.
Outputs go to ../results/. Seeds fixed (20261013 + section offset).
"""
import sys, gzip, json, importlib.util
from pathlib import Path
import numpy as np
import pandas as pd

PROJ = Path(r"D:\Research-Publishing\05-wikipedia-exam-traffic")
sys.path.insert(0, str(PROJ / "code"))
spec = importlib.util.spec_from_file_location("an", PROJ / "code" / "05_analyze.py")
an = importlib.util.module_from_spec(spec); spec.loader.exec_module(an)
spec3 = importlib.util.spec_from_file_location("pull03", PROJ / "code" / "03_pull_pageviews.py")
pull03 = importlib.util.module_from_spec(spec3); spec3.loader.exec_module(pull03)
RES = PROJ / "rework-v3" / "results"
DATAX = PROJ / "rework-v3" / "data"
RES.mkdir(exist_ok=True)
YEARS = list(range(2016, 2027))
PRE, POST = an.PRE, an.POST
POS = {d.strftime("%Y%m%d"): i for i, d in enumerate(an.DAYS)}

_orig_windows = an.windows


def windows_patched(y, wdef="main", bdef="main"):
    if wdef.startswith("shift"):
        s = int(wdef[5:])
        F = pd.Timestamp(an.FIRST[y]) + pd.Timedelta(days=s)
        w = an.idx(F - pd.Timedelta(days=28), F + pd.Timedelta(days=20))
        _, b = _orig_windows(y, "main", bdef)
        return w, b
    return _orig_windows(y, wdef, bdef)


an.windows = windows_patched


def load_series(path):
    v = np.zeros(len(an.DAYS), dtype=np.float32)
    with gzip.open(path, "rt") as f:
        for d, x in json.load(f):
            if d in POS:
                v[POS[d]] = x
    return v


def seed(k):
    an.RNG = np.random.default_rng(20261013 + k)


def main_setup():
    ix, m = an.load("full", "en", "all")
    P = an.pairs(ix)
    r = an.article_level(ix, m["all"], YEARS, PRE, POST, P)
    return ix, m, P, r


def yearly_rows(res, label):
    d = pd.DataFrame(res["rows"]); d.insert(0, "spec", label); return d


def contrast_row(res, label):
    return dict(spec=label, n_pairs=res["n_pairs"], D=res.get("D"), D_lo=res.get("D_lo"), D_hi=res.get("D_hi"),
                perm_p_one_sided=res.get("perm_p_one_sided"), perm_splits=res.get("perm_splits"),
                share_pairs_negative=res.get("share_pairs_negative"))


def perm_two_sided(pre, post):
    from itertools import combinations
    allv = np.array(list(pre) + list(post)); n, k = len(allv), len(post)
    obs = np.mean(post) - np.mean(pre); cnt = tot = 0
    for c in combinations(range(n), k):
        mk = np.zeros(n, bool); mk[list(c)] = True
        cnt += abs(allv[mk].mean() - allv[~mk].mean()) >= abs(obs) - 1e-12; tot += 1
    return cnt / tot


def e1(ix, m, P, r):
    seed(1)
    ys, cs = [], []
    for s in (-77, 77, 126):
        rr = an.article_level(ix, m["all"], YEARS, PRE, POST, P, wdef="shift%d" % s)
        ys.append(yearly_rows(rr, "E1 placebo window F%+d" % s)); cs.append(contrast_row(rr, "E1 placebo window F%+d" % s))
    ys.append(yearly_rows(r, "MAIN (true window)")); cs.append(contrast_row(r, "MAIN (true window)"))
    # (a) within-pre break
    G = r["G"]; jx = {y: YEARS.index(y) for y in YEARS}
    d = G[:, [jx[2019], jx[2020]]].mean(1) - G[:, [jx[2017], jx[2018]]].mean(1)
    bs = d[an.RNG.integers(0, len(d), (an.NBOOT, len(d)))].mean(1)
    cs.append(dict(spec="E1a within-pre break: mean(2019,2020) - mean(2017,2018)", n_pairs=len(d), D=d.mean(),
                   D_lo=np.percentile(bs, 2.5), D_hi=np.percentile(bs, 97.5)))
    # (b) leave one year out
    gy = {y: np.nanmean(G[:, jx[y]]) for y in PRE + POST}
    rows = []
    for drop in PRE + POST:
        pre = [gy[y] for y in PRE if y != drop]; post = [gy[y] for y in POST if y != drop]
        p, tot = an.perm_p(pre, post)
        rows.append(dict(dropped_year=drop, D=np.mean(post) - np.mean(pre), perm_p_one_sided=p, splits=tot))
    pd.DataFrame(rows).round(4).to_csv(RES / "E1b_leave_one_year_out.csv", index=False)
    pd.concat(ys).round(4).to_csv(RES / "E1_placebo_dates_yearly.csv", index=False)
    pd.DataFrame(cs).round(4).to_csv(RES / "E1_placebo_dates_contrasts.csv", index=False)
    print(pd.DataFrame(cs).round(3).to_string()); print(pd.DataFrame(rows).round(3).to_string())


def e2b(r):
    seed(2)
    d = r["d_pair"]; obs = d.mean()
    flips = an.RNG.choice([-1.0, 1.0], size=(5000, len(d)))
    dist = (flips * d).mean(1)
    out = dict(observed_D=obs, share_draws_le_observed=float((dist <= obs).mean()), draw_sd=float(dist.std()),
               draw_p2_5=float(np.percentile(dist, 2.5)), draw_p97_5=float(np.percentile(dist, 97.5)))
    pd.DataFrame([out]).round(5).to_csv(RES / "E2b_signflip.csv", index=False); print(out)
    np.save(RES / "E2b_signflip_draws.npy", dist.astype(np.float32))


def e6(ix, m, P, r):
    from scipy import stats
    G = r["G"]; gy = {y: np.nanmean(G[:, YEARS.index(y)]) for y in PRE + POST}
    pre = np.array([gy[y] for y in PRE]); post = np.array([gy[y] for y in POST])
    out = []
    def block(label, pre, post):
        D = post.mean() - pre.mean()
        se = np.sqrt(pre.var(ddof=1) / 4 + post.var(ddof=1) / 4)
        df = se ** 4 / ((pre.var(ddof=1) / 4) ** 2 / 3 + (post.var(ddof=1) / 4) ** 2 / 3)
        t = stats.t.ppf(0.975, df)
        grid = np.arange(-0.4, 0.4, 0.0005); keep = []
        for dl in grid:
            if perm_two_sided(pre, post - dl) > 0.05:
                keep.append(dl)
        out.append(dict(estimator=label, D=D, welch_se=se, welch_df=df, welch_lo=D - t * se, welch_hi=D + t * se,
                        perm_inversion_lo=min(keep) if keep else np.nan, perm_inversion_hi=max(keep) if keep else np.nan,
                        perm_p_two_sided=perm_two_sided(pre, post), pre_mean_gap=pre.mean(), post_mean_gap=post.mean(),
                        D_over_pre_gap=D / pre.mean(), pct_change_in_ratio=np.expm1(D) * 100))
    block("article-level mean gap", pre, post)
    rp = an.pooled(ix, m["all"], YEARS, PRE, POST, P)
    gp = {r_["year"]: r_["gap"] for r_ in rp["rows"]}
    block("pooled", np.array([gp[y] for y in PRE]), np.array([gp[y] for y in POST]))
    o = pd.DataFrame(out); o.round(4).to_csv(RES / "E6_season_level_intervals.csv", index=False); print(o.round(3).T.to_string())


def e4(ix, m, P):
    seed(4)
    ra = {k: an.article_level(ix, m[k], YEARS, PRE, POST, P) for k in ("desktop", "mobile", "all")}
    ys = pd.concat([yearly_rows(ra[k], "E4/R5 " + k) for k in ra]); cs = pd.DataFrame([contrast_row(ra[k], "E4/R5 " + k) for k in ra])
    # difference mobile - desktop on common pairs
    key = lambda res: {(a, b): i for i, (a, b) in enumerate(map(tuple, res["Pk"]))}
    km, kd = key(ra["mobile"]), key(ra["desktop"]); common = sorted(set(km) & set(kd))
    Gm = ra["mobile"]["G"][[km[c] for c in common]]; Gd = ra["desktop"]["G"][[kd[c] for c in common]]
    Gdiff = Gm - Gd
    gy = {y: np.nanmean(Gdiff[:, YEARS.index(y)]) for y in PRE + POST}
    pre = [gy[y] for y in PRE]; post = [gy[y] for y in POST]
    dpair = Gdiff[:, [YEARS.index(y) for y in POST]].mean(1) - Gdiff[:, [YEARS.index(y) for y in PRE]].mean(1)
    bs = dpair[an.RNG.integers(0, len(dpair), (an.NBOOT, len(dpair)))].mean(1)
    cs = pd.concat([cs, pd.DataFrame([dict(spec="E4 D_mobile - D_desktop (common pairs)", n_pairs=len(common), D=dpair.mean(),
                                          D_lo=np.percentile(bs, 2.5), D_hi=np.percentile(bs, 97.5),
                                          perm_p_two_sided=perm_two_sided(pre, post))])])
    # mobile share of all views by year x group in window and baseline
    rows = []
    Pk = ra["all"]["Pk"]
    ok = np.isfinite(m["desktop"][Pk[:, 0]].sum(1)) & np.isfinite(m["desktop"][Pk[:, 1]].sum(1))
    for y in YEARS:
        w, b = an.windows(y)
        for g, col in (("syllabus", 0), ("control", 1)):
            rows_ = Pk[ok, col]
            for nm, sl in (("window", w), ("baseline", b)):
                tot = np.nansum(m["all"][rows_][:, sl]); mob = np.nansum(m["mobile"][rows_][:, sl])
                rows.append(dict(year=y, group=g, period=nm, mobile_share=mob / tot))
    pd.DataFrame(rows).round(4).to_csv(RES / "E4_mobile_share.csv", index=False)
    ys.round(4).to_csv(RES / "E4_access_yearly.csv", index=False); cs.round(4).to_csv(RES / "E4_access_contrasts.csv", index=False)
    print(cs.round(3).to_string())


def e2a(ix, m, P, r):
    seed(5)
    pl = pd.read_csv(DATAX / "placebo_pairs.csv").fillna("")
    pl = pl[pl.placebo_C != ""]
    rows, mats = [], []
    ctl_row = {a: i for i, a in zip(ix.index[ix.group == "A_same_area"], ix.article[ix.group == "A_same_area"])}
    N = m["all"].shape[0]
    for j, rr in enumerate(pl.itertuples()):
        p = pull03.series_path("en.wikipedia", rr.placebo_C, "all-access")
        if not p.exists() or rr.control_A not in ctl_row:
            continue
        mats.append(load_series(p)); rows.append((ctl_row[rr.control_A], N + len(mats) - 1, rr.syllabus_article))
    M = np.vstack([m["all"], np.array(mats)])
    cc = np.array([(a, b) for a, b, _ in rows]); synrow = {t: i for i, t in zip(ix.index, ix.article)}
    # (i) control-vs-control (c minus c')
    r1 = an.article_level(ix, M, YEARS, PRE, POST, cc)
    # (ii) syllabus vs c'
    sp = np.array([(synrow[s], b) for a, b, s in rows if s in synrow])
    r2 = an.article_level(ix, M, YEARS, PRE, POST, sp)
    ys = pd.concat([yearly_rows(r1, "E2a(i) control A minus placebo C"), yearly_rows(r2, "E2a(ii) syllabus minus placebo C as control")])
    cs = pd.DataFrame([contrast_row(r1, "E2a(i) control A minus placebo C"), contrast_row(r2, "E2a(ii) syllabus vs control C")])
    # same pairs as r2 with the original control, for a like-for-like comparison
    orig = {int(a): int(b) for a, b in P}
    sp0 = np.array([(a, orig[a]) for a, _ in sp if a in orig])
    r3 = an.article_level(ix, M, YEARS, PRE, POST, sp0)
    ys = pd.concat([ys, yearly_rows(r3, "E2a(iii) same syllabus articles, original control A")])
    cs = pd.concat([cs, pd.DataFrame([contrast_row(r3, "E2a(iii) same syllabus articles, original control A")])])
    ys.round(4).to_csv(RES / "E2a_placebo_pages_yearly.csv", index=False); cs.round(4).to_csv(RES / "E2a_placebo_pages_contrasts.csv", index=False)
    print(cs.round(3).to_string())
    print(ys[ys.spec.str.startswith("E2a(i)")][["year", "gap", "ci_lo", "ci_hi"]].round(3).to_string())


def e3(ix, m, P):
    seed(3)
    N = len(ix); U = np.zeros((N, len(an.DAYS)), np.float32); A = U.copy(); T = U.copy(); have = np.zeros(N, bool)
    for i, a in enumerate(ix.article):
        if ix.group.iloc[i] not in ("syllabus", "A_same_area"):
            continue
        pu = pull03.series_path("en.wikipedia", a, "all-access")
        from common import cache_path
        pa = cache_path("pv_agent/automated", a, ext=".json.gz"); pt = cache_path("pv_agent/all-agents", a, ext=".json.gz")
        if pu.exists() and pa.exists() and pt.exists():
            U[i], A[i], T[i] = load_series(pu), load_series(pa), load_series(pt); have[i] = True
    P2 = np.array([(a, b) for a, b in P if have[a] and have[b]])
    out_c, out_y = [], []
    for nm, mat in (("user (current title only)", U), ("all-agents", T), ("automated only", A), ("spider+other = all-agents - user - automated", np.clip(T - U - A, 0, None))):
        rr = an.article_level(ix, mat, YEARS, PRE, POST, P2)
        out_y.append(yearly_rows(rr, "E3 " + nm)); out_c.append(contrast_row(rr, "E3 " + nm))
    # automated share by year x group, window and baseline
    rows = []
    for y in YEARS:
        w, b = an.windows(y)
        for g, col in (("syllabus", 0), ("control", 1)):
            rr_ = P2[:, col]
            for nm, sl in (("window", w), ("baseline", b)):
                rows.append(dict(year=y, group=g, period=nm, automated_share=A[rr_][:, sl].sum() / T[rr_][:, sl].sum(),
                                 user_share=U[rr_][:, sl].sum() / T[rr_][:, sl].sum()))
    pd.DataFrame(rows).round(4).to_csv(RES / "E3_automated_share.csv", index=False)
    # monthly user / all-agents for the control group (reclassification check)
    ctl = np.unique(P2[:, 1]); mon = pd.Series(an.DAYS.to_period("M").astype(str))
    dfm = pd.DataFrame({"month": mon, "user": U[ctl].sum(0), "automated": A[ctl].sum(0), "all_agents": T[ctl].sum(0)}).groupby("month").sum()
    dfm["user_over_all"] = dfm.user / dfm.all_agents; dfm["automated_over_all"] = dfm.automated / dfm.all_agents
    dfm.round(5).to_csv(RES / "E3_monthly_control_group.csv")
    dfs = pd.DataFrame({"month": mon, "user": U[P2[:, 0]].sum(0), "automated": A[P2[:, 0]].sum(0), "all_agents": T[P2[:, 0]].sum(0)}).groupby("month").sum()
    dfs["user_over_all"] = dfs.user / dfs.all_agents; dfs["automated_over_all"] = dfs.automated / dfs.all_agents
    dfs.round(5).to_csv(RES / "E3_monthly_syllabus_group.csv")
    pd.concat(out_y).round(4).to_csv(RES / "E3_agent_yearly.csv", index=False)
    cs = pd.DataFrame(out_c); cs.round(4).to_csv(RES / "E3_agent_contrasts.csv", index=False); print(cs.round(3).to_string())


def e7(ix, m, P, r):
    seed(7)
    Pk = r["Pk"]; ys = list(range(2017, 2027)); L = np.full((len(ix), len(ys)), np.nan)
    for j, y in enumerate(ys):
        w, b = an.windows(y); L[:, j] = np.log(m["all"][:, b].mean(1))
    S, C = L[Pk[:, 0]] - L[Pk[:, 0]][:, [0]], L[Pk[:, 1]] - L[Pk[:, 1]][:, [0]]
    D = S - C; boot = an.RNG.integers(0, len(Pk), (2000, len(Pk)))
    rows = []
    for j, y in enumerate(ys):
        bs = np.nanmean(D[:, j][boot], axis=1)
        rows.append(dict(exam_year=y, baseline="Jul-Oct %d" % (y - 1), syllabus_change_vs_2017=np.nanmean(S[:, j]), control_change_vs_2017=np.nanmean(C[:, j]),
                         relative_level_syl_minus_ctl=np.nanmean(D[:, j]), ci_lo=np.percentile(bs, 2.5), ci_hi=np.percentile(bs, 97.5)))
    o = pd.DataFrame(rows).round(4); o.to_csv(RES / "E7_baseline_levels.csv", index=False); print(o.to_string())


if __name__ == "__main__":
    todo = sys.argv[1:]
    ix, m, P, r = main_setup()
    print("main pairs", len(P), "D", round(r["D"], 4), "p", round(r["perm_p_one_sided"], 4))
    if "e1" in todo: e1(ix, m, P, r)
    if "e2b" in todo: e2b(r)
    if "e6" in todo: e6(ix, m, P, r)
    if "e4" in todo: e4(ix, m, P)
    if "e2a" in todo: e2a(ix, m, P, r)
    if "e3" in todo: e3(ix, m, P)
    if "e7" in todo: e7(ix, m, P, r)

