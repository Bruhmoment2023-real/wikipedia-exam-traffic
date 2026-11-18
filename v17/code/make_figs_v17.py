"""Figures for the v17 manuscript, drawn from the result files and panels (matplotlib, 600 dpi).
Run: python make_figs_v17.py  (figures that lack their input are skipped and reported).
"""
import sys, importlib.util
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

PROJ = Path(r"D:\Research-Publishing\05-wikipedia-exam-traffic")
R0 = PROJ / "results"                    # frozen pipeline outputs (05_analyze.py)
RX = PROJ / "rework-v3" / "results"      # extension outputs
OUT = PROJ / "rework-v3" / "figures"; OUT.mkdir(exist_ok=True)
DPI = 600
for f in ("times.ttf", "timesbd.ttf", "timesi.ttf"):
    fm.fontManager.addfont(r"C:\Windows\Fonts\%s" % f)
plt.rcParams.update({"font.family": "Times New Roman", "font.size": 9, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.linewidth": 0.7, "xtick.major.width": 0.7, "ytick.major.width": 0.7, "legend.frameon": False,
                     "savefig.dpi": DPI, "figure.dpi": 150})
BLUE, ORANGE, INK, GREY, GREEN, PURPLE = "#2a78d6", "#eb6834", "#0b0b0b", "#8a8985", "#2f8f5b", "#7a4fb5"
PRE, POST, ASIDE = [2017, 2018, 2019, 2020], [2023, 2024, 2025, 2026], [2016, 2021, 2022]
done, skipped = [], []


def save(fig, name):
    p = OUT / (name + ".png"); fig.savefig(p, dpi=DPI, bbox_inches="tight", facecolor="white"); plt.close(fig); done.append(name)


def main_rows(df, lang="en", est="article-level"):
    d = df[df.spec.str.startswith("MAIN") & (df.lang == lang) & (df.estimator == est)]
    return d.set_index("year")


def shade_post(ax, ylim=None):
    ax.axvspan(2022.5, 2026.5, color="#efeeea", zorder=0)


def fig1():
    spec = importlib.util.spec_from_file_location("an", PROJ / "code" / "05_analyze.py")
    an = importlib.util.module_from_spec(spec); sys.path.insert(0, str(PROJ / "code")); spec.loader.exec_module(an)
    ix, m = an.load("full", "en", "all"); P = an.pairs(ix)
    rel = np.arange(-150, 121)
    fig, axs = plt.subplots(1, 2, figsize=(7.0, 2.9), sharey=True)
    for ax, (nm, yrs) in zip(axs, (("Before ChatGPT (exam years 2017-2020)", an.PRE), ("After ChatGPT (exam years 2023-2026)", an.POST))):
        for col, lab, c in ((0, "Syllabus articles", BLUE), (1, "Matched controls", ORANGE)):
            prof = []
            for y in yrs:
                F = an.idx(an.FIRST[y], an.FIRST[y])[0]
                w, b = an.windows(y)
                base = m["all"][P[:, col]][:, b].mean(1); ok = base >= 5
                seg = m["all"][P[ok, col]][:, F + rel[0] - 3: F + rel[-1] + 4] / base[ok][:, None]
                sm = np.apply_along_axis(lambda v: np.convolve(v, np.ones(7) / 7, mode="valid"), 1, seg)
                prof.append(np.exp(np.log(np.clip(sm, 1e-6, None)).mean(0)))
            ax.plot(rel, np.mean(prof, axis=0), color=c, lw=1.4, label=lab)
        ax.axvspan(-28, 20, color="#efeeea", zorder=0); ax.axvline(0, color=GREY, ls=":", lw=0.8)
        ax.set_title(nm, fontsize=9); ax.set_xlabel("Days from first CBSE paper"); ax.axhline(1, color=GREY, lw=0.5)
    axs[0].set_ylabel("Views relative to July-October baseline\n(geometric mean over articles)"); axs[0].legend(loc="lower left", fontsize=8)
    save(fig, "Fig1_seasonal_profile")


def fig2_3():
    df = pd.read_csv(R0 / "yearly_gaps_full_all.csv"); d = main_rows(df)
    fig, ax = plt.subplots(figsize=(4.8, 3.0)); shade_post(ax)
    for y, r in d.iterrows():
        aside = y in ASIDE; ax.errorbar(y, r.gap, yerr=[[r.gap - r.ci_lo], [r.ci_hi - r.gap]], fmt="o", color=GREY if aside else BLUE, mfc="white" if aside else BLUE, ms=4.5, capsize=2, lw=1)
    ax.axhline(0, color=GREY, lw=0.6); ax.set_xticks(range(2016, 2027)); ax.set_xlabel("Exam year"); ax.set_ylabel("Syllabus minus control uplift (log points)")
    ax.set_xticklabels([str(y) for y in range(2016, 2027)], rotation=45)
    save(fig, "Fig2_yearly_gap")
    fig, ax = plt.subplots(figsize=(4.8, 3.0)); shade_post(ax)
    ax.plot(d.index, d.uplift_syllabus, "-o", color=BLUE, ms=4, lw=1.2, label="Syllabus articles"); ax.plot(d.index, d.uplift_control, "-o", color=ORANGE, ms=4, lw=1.2, label="Matched controls")
    ax.axhline(0, color=GREY, lw=0.6); ax.set_xticks(range(2016, 2027)); ax.set_xticklabels([str(y) for y in range(2016, 2027)], rotation=45)
    ax.set_xlabel("Exam year"); ax.set_ylabel("Exam-season uplift (log points)"); ax.legend(fontsize=8)
    save(fig, "Fig3_uplift_by_group")


def fig4():
    d = pd.read_csv(R0 / "secondary_eve_of_paper_full_all.csv")
    subs = [("X-SCI", "Class 10 Science"), ("X-MAT", "Class 10 Mathematics"), ("XII-PHY", "Class 12 Physics"), ("XII-CHE", "Class 12 Chemistry"), ("XII-BIO", "Class 12 Biology"), ("XII-MAT", "Class 12 Mathematics")]
    fig, axs = plt.subplots(2, 3, figsize=(7.0, 4.2), sharex=True, sharey=True)
    for ax, (k, nm) in zip(axs.ravel(), subs):
        s = d[d.subject == k].sort_values("year"); shade_post(ax)
        ax.errorbar(s.year, s.gap, yerr=[s.gap - s.ci_lo, s.ci_hi - s.gap], fmt="o-", color=BLUE, ms=3.5, lw=1, capsize=1.5); ax.axhline(0, color=GREY, lw=0.5); ax.set_title(nm, fontsize=8.5)
        ax.set_xticks([2017, 2020, 2023, 2026])
    for ax in axs[1]: ax.set_xlabel("Exam year")
    for ax in axs[:, 0]: ax.set_ylabel("Eve-of-paper spike,\nsyllabus minus control")
    save(fig, "Fig4_eve_of_paper")


def fig5():
    d = pd.read_csv(RX / "E1_placebo_dates_yearly.csv")
    fig, ax = plt.subplots(figsize=(5.4, 3.2)); shade_post(ax)
    cols = {"MAIN (true window)": (INK, "True window"), "E1 placebo window F-77": (GREEN, "Placebo: 77 days earlier"), "E1 placebo window F+77": (PURPLE, "Placebo: 77 days later"), "E1 placebo window F+126": (ORANGE, "Placebo: 126 days later")}
    for k, (c, lab) in cols.items():
        s = d[d.spec == k].set_index("year"); s = s.loc[[y for y in s.index if y not in ASIDE]]
        ax.plot(s.index, s.gap, "-o", color=c, ms=3.5, lw=1.2, label=lab)
    ax.axhline(0, color=GREY, lw=0.6); ax.set_xlabel("Exam year"); ax.set_ylabel("Syllabus minus control uplift (log points)"); ax.legend(fontsize=7.5, loc="lower left")
    ax.set_xticks([2017, 2018, 2019, 2020, 2023, 2024, 2025, 2026])
    save(fig, "Fig5_placebo_windows")


def fig6():
    df = pd.read_csv(R0 / "yearly_gaps_full_all.csv")
    fig, axs = plt.subplots(1, 3, figsize=(7.0, 2.6), sharey=False)
    for ax, (lang, nm) in zip(axs, (("en", "English"), ("hi", "Hindi"), ("kn", "Kannada"))):
        d = df[df.spec.str.startswith("MAIN") & (df.lang == lang) & (df.estimator == "pooled")].set_index("year")
        if len(d) == 0: ax.set_title(nm + " (no data)"); continue
        d = d.loc[[y for y in d.index if y not in ASIDE]]; shade_post(ax)
        ax.errorbar(d.index, d.gap, yerr=[d.gap - d.ci_lo, d.ci_hi - d.gap], fmt="o-", color=BLUE, ms=3.5, lw=1, capsize=1.5)
        ax.axhline(0, color=GREY, lw=0.5); ax.set_title("%s (%d pairs)" % (nm, int(d.n_pairs.iloc[0])), fontsize=8.5); ax.set_xticks([2017, 2020, 2023, 2026]); ax.set_xlabel("Exam year")
    axs[0].set_ylabel("Pooled gap (log points)")
    save(fig, "Fig6_languages_pooled")


def fig7():
    d = pd.read_csv(RX / "E4_access_yearly.csv")
    fig, ax = plt.subplots(figsize=(5.0, 3.0)); shade_post(ax)
    for k, c, lab in (("E4/R5 desktop", ORANGE, "Desktop"), ("E4/R5 mobile", BLUE, "Mobile (all access minus desktop)"), ("E4/R5 all", INK, "All access")):
        s = d[d.spec == k].set_index("year"); s = s.loc[[y for y in s.index if y not in ASIDE]]
        ax.errorbar(s.index, s.gap, yerr=[s.gap - s.ci_lo, s.ci_hi - s.gap], fmt="o-", color=c, ms=3.2, lw=1, capsize=1.2, label="%s (%d pairs)" % (lab, int(s.n_pairs.iloc[0])))
    ax.axhline(0, color=GREY, lw=0.6); ax.set_xlabel("Exam year"); ax.set_ylabel("Syllabus minus control uplift (log points)"); ax.legend(fontsize=7.5)
    save(fig, "Fig7_desktop_mobile")


def fig8():
    m1 = pd.read_csv(RX / "E3_monthly_control_group.csv"); m2 = pd.read_csv(RX / "E3_monthly_syllabus_group.csv")
    fig, axs = plt.subplots(1, 2, figsize=(7.0, 2.8))
    x = pd.to_datetime(m1.month.astype(str) + "-01")
    axs[0].plot(x, m1.automated_over_all * 100, color=ORANGE, lw=1.2, label="Matched controls"); axs[0].plot(x, m2.automated_over_all * 100, color=BLUE, lw=1.2, label="Syllabus articles")
    axs[0].set_ylabel("Automated share of all-agent views (%)"); axs[0].legend(fontsize=8); axs[0].set_xlabel("Month")
    axs[1].plot(x, m1.user_over_all * 100, color=ORANGE, lw=1.2); axs[1].plot(x, m2.user_over_all * 100, color=BLUE, lw=1.2)
    axs[1].set_ylabel("'User' share of all-agent views (%)"); axs[1].set_xlabel("Month")
    save(fig, "Fig8_agent_shares")


def fig9():
    g = pd.read_csv(RX / "E5_clickstream_gaps.csv"); sh = pd.read_csv(RX / "E5_clickstream_class_shares.csv")
    fig, axs = plt.subplots(1, 2, figsize=(7.0, 3.0))
    s = sh[sh.group == "syllabus"].copy(); s["lab"] = s.month
    for c, col, nm in (("SEARCH_share", BLUE, "Search engines"), ("DIRECT_share", ORANGE, "Direct / no referrer"), ("LINK_share", GREEN, "Links from other articles"), ("OTHER_share", GREY, "Other")):
        axs[0].plot(range(len(s)), s[c] * 100, "-o", color=col, ms=3, lw=1, label=nm)
    axs[0].set_xticks(range(len(s))); axs[0].set_xticklabels(s.lab, rotation=60, fontsize=6.5); axs[0].set_ylabel("Share of syllabus-article clicks (%)"); axs[0].legend(fontsize=7)
    for c, col, nm in (("SEARCH", BLUE, "Search"), ("DIRECT", ORANGE, "Direct"), ("LINK", GREEN, "Links")):
        d = g[g.cls == c]; axs[1].errorbar(d.year + {"SEARCH": -0.15, "DIRECT": 0, "LINK": 0.15}[c], d.gap, yerr=[d.gap - d.ci_lo, d.ci_hi - d.gap], fmt="o", color=col, ms=3.5, capsize=1.5, label=nm)
    axs[1].set_xticks([2019, 2020, 2023, 2024, 2025, 2026]); axs[1].axhline(0, color=GREY, lw=0.6); axs[1].set_xlabel("Exam year (February vs previous October)"); axs[1].set_ylabel("Syllabus minus control uplift (log points)"); axs[1].legend(fontsize=7)
    save(fig, "Fig9_clickstream")


if __name__ == "__main__":
    for f in (fig1, fig2_3, fig4, fig5, fig6, fig7, fig8, fig9):
        try:
            f()
        except Exception as e:
            skipped.append((f.__name__, repr(e)[:150]))
    print("done:", done); print("skipped:", skipped)
