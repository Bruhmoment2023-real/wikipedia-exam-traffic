"""Step 7. Figures (static PNG). Colours: syllabus = blue #2a78d6, control = orange #eb6834
(checked with the dataviz palette validator for colour-blind separation). One y-axis per chart.
Usage:  python 07_figures.py full
"""
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from importlib import import_module
from common import DATA, RESULTS

an = import_module("05_analyze")
BLUE, ORANGE, INK, MUTED, GRID, SURF = "#2a78d6", "#eb6834", "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
plt.rcParams.update({"font.size": 10, "axes.edgecolor": GRID, "axes.labelcolor": MUTED, "xtick.color": MUTED,
                     "ytick.color": MUTED, "axes.spines.top": False, "axes.spines.right": False,
                     "figure.facecolor": SURF, "axes.facecolor": SURF, "savefig.facecolor": SURF,
                     "axes.titlecolor": INK, "axes.titlesize": 11, "axes.titleweight": "bold", "axes.titlelocation": "left"})
LANGNAME = {"en": "English", "hi": "Hindi", "kn": "Kannada"}


def fig_profile(name):
    """Mean traffic index around the first exam day, syllabus vs control, before vs after."""
    ix, m = an.load(name, "en", "all")
    P = an.pairs(ix)
    mat = m["all"]
    rel = np.arange(-150, 121)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), sharey=True)
    for ax, (label, yrs) in zip(axes, [("Before: exam years 2017-2020", an.PRE), ("After: exam years 2023-2026", an.POST)]):
        for col, color, lab in ((0, BLUE, "Syllabus articles"), (1, ORANGE, "Matched control articles")):
            prof = []
            for y in yrs:
                F = np.where(an.DAYS == pd.Timestamp(an.FIRST[y]))[0][0]
                w, b = an.windows(y)
                base = mat[P[:, col]][:, b].mean(1)
                ok = base >= 5
                seg = mat[P[ok, col]][:, F + rel[0] - 3: F + rel[-1] + 4] / base[ok][:, None]
                k = np.ones(7) / 7
                sm = np.apply_along_axis(lambda v: np.convolve(v, k, mode="valid"), 1, seg)
                prof.append(np.exp(np.log(np.clip(sm, 1e-6, None)).mean(0)))   # geometric mean across articles
            pr = np.mean(prof, axis=0)
            ax.plot(rel, pr, color=color, lw=2, label=lab)
            ax.annotate(lab, (rel[-1], pr[-1]), xytext=(4, 0), textcoords="offset points", color=INK, fontsize=9, va="center")
        ax.axvspan(-28, 20, color=GRID, alpha=0.55, lw=0)
        ax.axvline(0, color=MUTED, lw=0.8, ls=":")
        ax.axhline(1, color=GRID, lw=1)
        ax.set_title(label)
        ax.set_xlabel("Days from the first CBSE board paper (shaded: exam window)")
        ax.grid(axis="y", color=GRID, lw=0.6)
        ax.set_xlim(rel[0], rel[-1] + 62)
    axes[0].set_ylabel("Daily views / article's own Jul-Oct average\n(7-day mean, geometric mean over articles)")
    axes[0].legend(frameon=False, loc="upper left", fontsize=9)
    fig.suptitle("English Wikipedia, science and mathematics: traffic through the exam year", x=0.01, ha="left", color=INK, fontweight="bold")
    fig.tight_layout()
    fig.savefig(RESULTS / "fig1_seasonal_profile_en.png", dpi=160)
    plt.close(fig)


def fig_gaps(name):
    Y = pd.read_csv(RESULTS / ("yearly_gaps_%s_all.csv" % name))
    Y = Y[Y.spec.str.startswith("MAIN")]
    langs = [l for l in ("en", "hi", "kn") if l in set(Y.lang)]
    fig, axes = plt.subplots(1, len(langs), figsize=(4.2 * len(langs), 4.0), sharey=False)
    axes = np.atleast_1d(axes)
    for ax, lang in zip(axes, langs):
        d = Y[Y.lang == lang]
        est = "article-level" if (d.estimator == "article-level").any() else "pooled"
        d = d[d.estimator == est].sort_values("year")
        ax.axhline(0, color=MUTED, lw=0.8)
        ax.axvspan(2022.4, 2026.6, color=GRID, alpha=0.5, lw=0)
        for r in d.itertuples():
            solid = r.role in ("pre", "post")
            ax.plot([r.year, r.year], [r.ci_lo, r.ci_hi], color=BLUE, lw=2, alpha=1 if solid else 0.45)
            ax.plot(r.year, r.gap, "o", ms=8, mfc=BLUE if solid else SURF, mec=BLUE, mew=1.8)
        ax.set_title("%s (%s, %d pairs)" % (LANGNAME[lang], est, d.n_pairs.max()))
        ax.set_xticks(range(2016, 2027, 2))
        ax.set_xlabel("Exam year (shaded: after ChatGPT's launch)")
        ax.grid(axis="y", color=GRID, lw=0.6)
    axes[0].set_ylabel("Exam-season uplift, syllabus minus control\n(log points; 0.10 = about 10%)")
    fig.suptitle("Gap in exam-season uplift by year. Hollow points: years set aside (2016, 2021, 2022). Bars: 95% bootstrap intervals",
                 x=0.01, ha="left", color=INK, fontsize=10, fontweight="bold")
    fig.tight_layout()
    fig.savefig(RESULTS / "fig2_yearly_gap_by_language.png", dpi=160)
    plt.close(fig)


def fig_levels(name):
    """Uplift of each group separately (so a reader can see which group moved)."""
    Y = pd.read_csv(RESULTS / ("yearly_gaps_%s_all.csv" % name))
    d = Y[Y.spec.str.startswith("MAIN") & (Y.lang == "en") & (Y.estimator == "article-level")].sort_values("year")
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.axhline(0, color=MUTED, lw=0.8)
    ax.axvspan(2022.4, 2026.6, color=GRID, alpha=0.5, lw=0)
    for col, color, lab in (("uplift_syllabus", BLUE, "Syllabus articles"), ("uplift_control", ORANGE, "Matched controls")):
        ax.plot(d.year, d[col], "-o", color=color, lw=2, ms=7, label=lab)
        ax.annotate(lab, (d.year.iloc[-1], d[col].iloc[-1]), xytext=(8, 0), textcoords="offset points", color=INK, fontsize=9, va="center")
    ax.set_xlim(2015.6, 2028.6)
    ax.set_xticks(range(2016, 2027))
    ax.set_ylabel("Exam-season uplift (log points)")
    ax.set_xlabel("Exam year (2016, 2021, 2022 are set-aside years)")
    ax.set_title("English Wikipedia, science and mathematics: uplift of each group")
    ax.grid(axis="y", color=GRID, lw=0.6)
    ax.legend(frameon=False, loc="lower left", fontsize=9)
    fig.tight_layout()
    fig.savefig(RESULTS / "fig3_uplift_each_group_en.png", dpi=160)
    plt.close(fig)


def fig_eve(name):
    S = pd.read_csv(RESULTS / ("secondary_eve_of_paper_%s_all.csv" % name))
    if S.empty:
        return
    subs = sorted(S.subject.unique())
    fig, axes = plt.subplots(1, len(subs), figsize=(2.5 * len(subs), 3.6), sharey=True)
    for ax, s in zip(np.atleast_1d(axes), subs):
        d = S[S.subject == s].sort_values("year")
        ax.axhline(0, color=MUTED, lw=0.8)
        ax.axvspan(2022.4, 2026.6, color=GRID, alpha=0.5, lw=0)
        ax.vlines(d.year, d.ci_lo, d.ci_hi, color=BLUE, lw=2)
        ax.plot(d.year, d.gap, "o", color=BLUE, ms=6)
        ax.set_title(s, fontsize=10)
        ax.set_xticks([2017, 2020, 2023, 2026])
        ax.grid(axis="y", color=GRID, lw=0.6)
    np.atleast_1d(axes)[0].set_ylabel("Eve-of-paper spike, syllabus minus control\n(log points)")
    fig.suptitle("Views on the three days before a subject's CBSE paper, relative to the surrounding weeks (English)",
                 x=0.01, ha="left", color=INK, fontsize=10, fontweight="bold")
    fig.tight_layout()
    fig.savefig(RESULTS / "fig4_eve_of_paper_spike.png", dpi=160)
    plt.close(fig)


if __name__ == "__main__":
    n = sys.argv[1] if len(sys.argv) > 1 else "full"
    for f in (fig_profile, fig_gaps, fig_levels, fig_eve):
        try:
            f(n)
            print("ok", f.__name__)
        except Exception as e:
            print("FAILED", f.__name__, repr(e))
