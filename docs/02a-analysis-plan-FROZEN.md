# Analysis plan, frozen before the post-2022 page-view data were examined

Frozen on 2026-10-13 (India time). The SHA-256 of this file and the time of freezing are recorded in
`results/plan_freeze.txt`. Any later change is listed under "Amendments" at the bottom with a reason,
and the original text above it is left untouched.

**What had been seen when this was frozen (full disclosure).**
- Monthly English page views for January 2016 - December 2019 only, used to match controls.
- No daily series, and nothing after December 2019, from the Pageviews API.
- One exception: to test whether the per-country files were usable, two single days of the
  per-country data were downloaded (5 March 2019 and 1 March 2024). For 1 March 2024 the row counts
  and the eight most-viewed syllabus articles in India were printed. No seasonal comparison was made.
- The prior-work reading (which reports falling views for physics articles, see `01-prior-work.md`).

## 1. Question

Did the exam-season rise in Wikipedia page views of school-syllabus articles get smaller after
generative AI chatbots became widely available (ChatGPT, 30 November 2022), compared with matched
non-syllabus articles, and does the change differ between English, Hindi and Kannada Wikipedia?

## 2. Hypotheses

- **H1 (main).** In English Wikipedia, the gap between the exam-season uplift of syllabus articles and
  of matched control articles is smaller in the exam years 2023-2026 than in 2017-2020.
- **H2 (dose).** The gap shrinks progressively: 2023 > 2024 > 2025 > 2026.
- **H3 (language).** The shrinkage is smaller in Hindi and in Kannada than in English.
- **H0.** No change in the gap. A null or an opposite-signed result will be reported as such.

## 3. Units and samples

- **Syllabus articles**: `data/syllabus_articles.csv` (868 English articles mapped from topic names in
  the CBSE Class 10 Science, Mathematics and Social Science syllabi and the Class 12 Physics,
  Chemistry, Biology and Mathematics syllabi; Hindi and Kannada versions through Wikidata sitelinks).
- **Control set A**: one non-syllabus article per syllabus article, same broad area (science,
  mathematics, social science), nearest neighbour on log mean daily views 2016-2019
  (`data/control_articles.csv`, built by `code/02_build_controls.py`).
- **Control set B**: same rule, but drawn from other areas (arts, philosophy and religion, everyday
  life), for a random half of the syllabus articles. Robustness only.
- **Primary sample: science and mathematics articles (areas SCI and MAT).** Social-science articles
  (Indian politics, parties, the Election Commission, Gandhi) are hit by news events and by the 2019
  and 2024 general elections, which fall in or next to the exam window, so they are analysed
  separately as a secondary sample.
- **Traffic**: agent type `user` only. All access types for the main analysis; desktop and mobile
  (all-access minus desktop) separately as robustness.
- **Series per article** = views of the current title + views of redirects created after June 2015
  (to capture renames) + the syllabus wording where the mapping used a redirect.
- **Inclusion rule for article-level analysis**: mean daily views of at least 5 in every baseline
  period used (see below). Articles below that enter only the pooled analysis (section 5b).

## 4. Time definitions

- **Exam year y** runs from 1 July of year y-1 to 30 June of year y.
- **First exam day F_y** (CBSE, earlier of Class 10 and Class 12; `data/exam_dates.csv`):
  2016: 1 Mar (unverified) | 2017: 9 Mar | 2018: 5 Mar | 2019: 15 Feb | 2020: 15 Feb |
  2021: cancelled | 2022: 26 Apr (term 2 of a two-term year) | 2023: 15 Feb | 2024: 15 Feb |
  2025: 15 Feb | 2026: 17 Feb.
- **Exam window W_y**: the 49 days from F_y - 28 to F_y + 20 (seven full weeks: four weeks of revision
  and the first three weeks of papers).
- **Baseline window B_y**: 1 July to 31 October of year y-1 (start of the school year, before the
  winter pre-board season).
- **Exam-season uplift** of article a in year y:
  U(a,y) = ln(mean daily views in W_y) - ln(mean daily views in B_y).
- **Pre-period years**: 2017, 2018, 2019, 2020. **Post-period years**: 2023, 2024, 2025, 2026.
  (ChatGPT's launch on 30 Nov 2022 falls after B_2023 and before W_2023, so 2023 is the first treated
  season.)
- **Years set aside**: 2021 (boards cancelled; baseline inside the first COVID year) and 2022 (two-term
  year with term-2 papers in April-June; baseline Jul-Oct 2021 still COVID-affected) are excluded from
  estimation and shown in figures as hollow points. 2016 is shown but not used in the main contrast
  because its first-exam date is not yet verified from a primary document and its baseline is the
  first four months of the dataset.
- The 2020 exam window (18 Jan - 6 Mar 2020) ends before India's lockdown (late March 2020), and its
  baseline is Jul-Oct 2019, so 2020 is kept as a pre-year; dropping it is robustness check R1.

## 5. Estimation

**5a. Article level (main).** For each language edition separately:

1. Paired gap for pair p in year y: G(p,y) = U(syllabus article, y) - U(its matched control, y).
2. Year-level gap: Gbar(y) = mean of G(p,y) over pairs, with a 95% confidence interval from a
   bootstrap that resamples pairs (2,000 draws). These per-year values are the main exhibit
   (an event-study plot with 2020 as the reference year).
3. Pre/post contrast: D = mean of Gbar(y) over post years - mean over pre years. Uncertainty two ways:
   (i) pair-cluster bootstrap of D (each pair carries all its years); (ii) a year-level permutation
   test that treats the 8 yearly values as the observations (70 possible splits into 4+4), because
   the number of independent time periods is 8, not the number of articles.
4. Event-study regression for the same thing with fixed effects:
   U(a,y) = article effect + year effect + sum over y of beta_y x [syllabus] x [year = y] + error,
   reference year 2020, standard errors clustered by matched pair. beta for 2017-2019 are the
   pre-trend check; a visible pre-trend will be reported as a limit on interpretation.
5. H2: slope of Gbar(y) across 2023-2026, descriptive only (four points).
6. H3: D(en) - D(hi) and D(en) - D(kn), pair-cluster bootstrap, restricted to pairs present in both
   editions.

No single pooled p-value will be presented as the headline; the per-year estimates and the
year-level permutation p-value are the headline.

**5b. Pooled (for low-traffic editions, and as a cross-check).** For each group g (syllabus, control):
U_pool(g,y) = ln(sum of views of all articles in W_y / 49) - ln(sum of views in B_y / 123).
Gap, contrast and bootstrap exactly as above, resampling articles.

## 6. Secondary outcome: the eve-of-paper spike (India-specific timing)

For subjects with a known paper date P in year y (Class 10 Science, Mathematics, Social Science;
Class 12 Physics, Chemistry, Biology, Mathematics):
S(a,y) = ln(mean views on days P-3..P-1) - ln(mean views on days P-24..P-11 and P+4..P+17).
Compared with the article's matched control on the same dates. Years available: 2017, 2019 (part),
2020, 2023-2026. Labelled secondary because several pre-period paper dates come from secondary
sources. Its value is that only Indian board candidates produce a spike on those exact dates.

## 7. Validation done on the pre-period only, before the post-period is opened

- V1: syllabus articles have a clearly positive gap over controls in 2017-2020.
- V2: the peak moves with the exam date (March in 2017-2018, mid-February from 2019): uplift computed
  in each year's own window versus the other regime's window.
- V3: an eve-of-paper spike exists in 2017-2020.
If V1 fails the design has no signal to study and the verdict is no-go.

## 8. Robustness checks (all will be reported, whatever they show)

- R1 drop 2020. R2 add 2016 and 2022. R3 control set B. R4 only syllabus articles whose keyword is
  found in both the 2020-21 and the 2024-25 syllabus text and that are not flagged ambiguous (removes
  topics cut in the 2022-23 "rationalisation"). R5 desktop only; mobile only. R6 other windows
  (F-14..F+34; fixed calendar 1 Feb - 31 Mar) and other baselines (Aug-Sep only). R7 geometric mean
  (mean of ln(1+views)) instead of arithmetic mean. R8 by subject. R9 social science separately.
  R10 India-only counts from the per-country differential-privacy files for the articles that clear
  the release threshold (pre: 2018-2020; post: 2024-2026; 2023 unusable because its baseline and exam
  window fall under different release rules).

## 9. What would count as support

H1 is supported only if the post-period yearly gaps lie below the pre-period ones with a year-level
permutation p of at most 0.05 (the smallest attainable one-sided value is 1/70), no pre-trend of
similar size, and the sign survives R1, R3, R4 and R5. Anything weaker is reported as "suggestive"
or "no detectable change".

## Amendments

(none at the time of freezing)

**A1 - recorded 2026-10-13T17:44:39Z UTC, after the pilot (50 pairs) had been analysed for exam years 2016-2020 only
(script stage `pre`, which masks every day after 30 June 2020) and before any post-2020 result had
been computed.**
- What the pilot's pre-period showed: the windowed uplift gap (section 5) is small, about 0.03-0.10
  log points with 40 pairs, because control articles also rise in February-March relative to
  July-October. The eve-of-paper spike (section 6) is larger and sharper (Class 10 Science gap
  0.14-0.26 log points with 12 pairs).
- No definition is changed. One thing is added so that the secondary outcome has a pre/post contrast
  defined in advance: for each subject, D_eve = mean of the yearly eve-of-paper gaps over 2023-2026
  minus the mean over the pre-period years with a known paper date (2017-2020); and an all-subject
  version that pools pairs. Uncertainty: pair bootstrap; per-year values shown.
- Redirect handling was narrowed for cost reasons before any outcome was computed: English series add
  only old names left behind by renames since mid-2015 (not every recent redirect); Hindi and Kannada
  use the current title only in the full pull. In the pilot, 1.5% (en), 2.9% (hi) and 4.9% (kn) of
  views sat on the redirect titles that were pulled.
- Disclosure: while checking the pilot panel, the overall desktop and mobile-app shares of all views
  (whole period pooled, no before/after split) were printed.

