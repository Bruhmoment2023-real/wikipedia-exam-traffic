# Exploratory extension plan (rework v3) - written BEFORE any extension analysis was run

Written 2026-11-17 (IST evening). Hash and UTC time are in `PLAN-exploratory.sha256.txt`.
Status of the original frozen plan: `../02a-analysis-plan-FROZEN.md` is untouched (hash in `../results/plan_freeze.txt`).

## What was already known when this plan was written (full disclosure)
- The confirmatory English results of 17 Oct 2026 (D = -0.046, permutation p = 0.129, yearly gaps, robustness R1-R9,
  eve-of-paper results) were known to the author. So the extensions below are NOT blind to the main result. They are
  written down before they are run so that their definitions cannot be tuned to the outcome.
- Not yet looked at: desktop series for the full English sample, Hindi/Kannada beyond 6 pairs, social-science pairs beyond 8,
  agent types other than `user`, clickstream files, placebo-page series. The pull of the frozen design was resumed on
  17 Nov 2026 and its output had not been analysed when this file was written.

## Part A. Completion of the FROZEN design (confirmatory; no change of definitions)
A0. Resume `code/03_pull_pageviews.py --full` unchanged until every series named in its tiers exists (English desktop, Hindi,
    Kannada, social science, control set B). Rebuild panels (`04_build_panel.py full`) and run `05_analyze.py full all`
    unchanged. R5 (desktop/mobile), R9 (social science) and H3 (Hindi, Kannada) are then reported on the complete samples.
    The new numbers replace the 17 Oct ones for those rows only. The English main specification must reproduce exactly
    (same cache files); any difference is reported.
    One departure that cannot be avoided: the bootstrap random stream is consumed in the same order, so later rows' intervals
    may differ in the third decimal because earlier rows now use more pairs. Point estimates are unaffected.

## Part B. Exploratory extensions (all labelled exploratory in the manuscript; none changes the verdict on H1)
Common: English Wikipedia, science + mathematics, control set A, the 711 pairs of the main sample, agent `user`,
all-access unless stated, windows/baselines/years exactly as in the frozen plan (pre 2017-2020, post 2023-2026),
yearly gaps, D, pair bootstrap (2,000 draws, seed 20261013), exact year-level permutation test (one-sided, 70 splits).

E1 Placebo dates. Replace the exam window by a 49-day window anchored at F_y + s days, s in {-77, +77, +126}
   (F_y as in the frozen plan; baseline unchanged). These windows lie before, after and well after the true window and do not
   overlap it or the baseline. Expectation if the design measures exam traffic: pre-period gaps near zero and D near zero.
   Reported: yearly gaps, D, p for each of the three s. Also: (a) within-pre break, D_pb = mean(gap 2019, 2020) - mean(gap 2017, 2018);
   (b) leave-one-year-out D (drop each of the eight years in turn, 4+3 or 3+4 comparison, descriptive).
E2 Placebo pages.
   (a) Control set C (placebo pairs): for each set-A control c in the main sample choose the nearest unused neighbour c' on
       log mean daily user views 2016-2019 (`data/control_candidates.csv`) from the same area, excluding every syllabus
       article and every set-A and set-B control, processed in alphabetical order of c, no replacement, ties alphabetical.
       Pull c' (en, user, all-access, current title). Report (i) the control-vs-control gap (c minus c'), yearly and D: should be
       about zero; (ii) the main D recomputed with c' as the control of the syllabus article (second control; robustness).
   (b) Sign-flip randomisation: for each pair flip the sign of the pair's change in gap with probability 1/2, 5,000 draws,
       report the distribution of D and the share of draws at least as negative as observed. This treats pairs as exchangeable, so
       it ignores the shared-season structure; shown only to contrast with the year-level test.
E3 Bot / agent filter. Pull `automated` and `all-agents` series (en, all-access, current title only) for the 711 syllabus and
   711 set-A articles. Report: (i) automated share of all-agent views by year x group in each window and baseline;
   (ii) yearly gaps and D for user-only (current title), all-agents, automated-only; (iii) monthly user/all-agent ratio of the
   control group over 2015-2026 (look for the 2025 reclassification). Spider = all-agents - user - automated (derived).
E4 Access types. With the completed desktop series: (i) D and yearly gaps for desktop and for mobile (mobile = all - desktop),
   frozen R5, on all pairs with desktop series; (ii) mobile share of views by year x group; (iii) D_mobile - D_desktop with pair
   bootstrap and year-level permutation of the eight yearly differences (two-sided).
E5 Clickstream (information-seeking paths). English Wikipedia monthly clickstream files for baseline month October (y-1) and exam
   month February (y), y = 2019, 2020, 2023, 2024, 2025, 2026 (files for 2018-10, 2019-02, 2019-10, 2020-02, 2022-10, 2023-02,
   2023-10, 2024-02, 2024-10, 2025-02, 2025-10, 2026-02; 2021 and 2022 exam years are set aside; clickstream starts Nov 2017 so
   2017 and 2018 have no baseline). Source classes by `prev`/`type`: SEARCH = prev "other-search"; DIRECT = "other-empty";
   LINK = type "link" (from another article); OTHER = remaining. Counts are per day (Oct 31 days, Feb 28 or 29). For the syllabus
   and set-A control groups: pooled counts per class; uplift per class = ln(Feb/day) - ln(Oct/day); group gap (syllabus - control);
   bootstrap over pairs (1,000 draws). Pre = 2019, 2020; post = 2023-2026; report each year and mean post - mean pre
   (descriptive, no p-value: only two pre years). Clickstream lists only pairs with >= 10 clicks, so counts are a lower bound
   and low-traffic articles drop out; reported with the coverage ratio (clickstream total / Pageviews total in the same month).
   Also descriptive: the 15 most frequent referring pages (LINK class) and next pages (outgoing) for syllabus articles in Feb 2020
   and Feb 2024; share of LINK traffic coming from other syllabus articles.
E6 Effect sizes with uncertainty at the season level. For the main D: (i) Welch t interval on the 4 + 4 yearly gaps;
   (ii) exact permutation interval by test inversion (two-sided p > 0.05); (iii) D as a share of the pre-period mean gap and
   exp(D) - 1; (iv) the same for the pooled estimator. Reported alongside, never instead of, the frozen permutation p.

## Rules for Part B
- No parameter is changed after seeing a result. If a definition above turns out to be unworkable (for example a file is
  missing) the change is written under "Amendments" below with the reason before the analysis is rerun.
- All results are reported, nulls included, in `results/` and in the appendix; the manuscript labels each as exploratory.
- No multiple-testing correction; p-values from Part B are descriptive.
- Reading rules fixed now: if the placebo windows show gaps or D as large as the real D, the manuscript says the design cannot
  separate the main D from background variation; if agent filtering moves D substantially, the manuscript says so.

## Not done, and why
- Other boards, other countries and other exams (ICSE/ISC, Karnataka PUC, state boards, GCSE/A-level, AP): each needs a verified
  topic mapping and primary-source date sheets, which free APIs do not supply. Listed as future work.

## Amendments
(none yet)

A1 (written 2026-11-17 before any placebo-page series was pulled): in E2a, if no unused candidate lies within 0.25 log points
   of c on 2016-2019 mean daily views (the same tolerance as the frozen matching report), c gets no placebo partner and drops out of
   E2a. Pull of E3 series uses the current title only; user-agent series used for comparison in E3 are likewise restricted to the
   current title (taken from the same cache as the main panel).

A2 (written 2026-11-17 ~20:50 IST, before any agent-type series was pulled, and after measuring API latency of 3-5 s per request,
   which makes the full E3 pull (2 x 1,422 series) take about 3 hours on top of the frozen pull): E3 uses a random sample of 250 of the
   main-sample pairs (numpy default_rng seed 20261014, drawn from the syllabus articles that have a set-A control), i.e. 500
   articles x 2 agent types = 1,000 series. All E3 statistics are computed on the pairs for which all three series exist.

A3 (written 2026-11-17 ~21:00 IST, before any of the affected series were analysed): the machine is CPU-saturated by other jobs and the
   Pageviews API answers in 3-8 s per request, so the 4,100 outstanding frozen-design series plus the extension series cannot all be
   fetched in one session. Fetch order (strictly sequential, one process): (1) Hindi and Kannada all-access series for science and
   mathematics pairs (frozen H3); (2) placebo-page series (E2a); (3) agent-type series for the 250-pair sample (E3); (4) English desktop
   series for the main-sample pairs in a seeded random order (seed 20261015), so that any prefix is a random sample of pairs (frozen R5,
   reported on the pairs completed and labelled as such); (5) social-science and control-set-B series (frozen R9, R3). Whatever has not
   been fetched when the draft is written is reported as not done, with the number of pairs completed.

A4 (written 2026-11-17 ~21:45 IST, before any of the affected series were fetched): after Hindi and Kannada, the three remaining
   fetch streams (English desktop series, placebo pages, agent-type sample) are fetched round-robin in chunks of 60 requests, each in a
   seeded random order of pairs (seed 20261015 for desktop, 20261016 for placebo pairs; E3 sample as in A2), so that stopping at any time
   leaves a random sample of pairs for each. Analyses use the pairs completed at the cut-off and report their number. Social-science and
   control-set-B series are fetched only if time remains (otherwise the 17 Oct results for R9 and R3 stand and are labelled incomplete).

A5 (written 2026-11-17 ~22:20 IST, after the clickstream results were seen and before this analysis was run): the clickstream totals showed
   a large fall in the level of syllabus-article traffic. E7 is added: for each article, L(a,y) = ln(mean daily 'user' views in the
   July-October baseline of exam year y), y = 2017 ... 2026; per group, the mean over the 711 main pairs of L(a,y) - L(a,2017); and the
   difference syllabus minus control, with a pair bootstrap (2,000 draws). Descriptive; it concerns levels, not the exam-season uplift.

A6 (written 2026-11-17 ~23:30 IST, before any of these series were analysed): the round-robin chunk sizes of A4 are changed to
   agent 120, placebo 60, desktop 40 requests per round, because the agent-type comparison needs about four series per pair and so
   about 400 series for 100 pairs. Pair order within each stream stays the seeded random order, so any prefix is still a random sample.
