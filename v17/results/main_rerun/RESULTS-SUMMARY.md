# RESULTS SUMMARY (run of 17 Oct 2026, IST; script `05_analyze.py full all`)

Plan: `02a-analysis-plan-FROZEN.md` (hash in `plan_freeze.txt`). All numbers are from `yearly_gaps_full_all.csv`,
`contrasts_full_all.csv`, `event_study_regression_full_all.csv`, `secondary_eve_*`, `R10_india_only.csv`.
Unit: gap = exam-season uplift of syllabus article minus uplift of its matched control, in natural-log points
(0.05 is roughly 5%). D = mean post-year gap (2023-26) minus mean pre-year gap (2017-20).

**What was complete when this ran.** English: all 711 science/maths pairs (all-access views). Hindi: 6 pairs
only (article-level), 19 pooled. Kannada: 0 usable pairs. The Hindi and Kannada pull (about 0.17 requests/s on the
loaded laptop) was still running; the Hindi and Kannada results below are NOT a test of H3.

## English, main specification (711 pairs, science + maths, control A, all access)
- Pre-period validation (V1) passes: gap is positive in every pre year with intervals above zero:
  2017 0.114, 2018 0.104, 2019 0.059, 2020 0.093 (CI half-widths about 0.02-0.03). Syllabus articles do have a
  larger exam-season rise than matched controls, before ChatGPT.
- Post years: 2023 0.059 [0.041, 0.076]; 2024 0.118 [0.099, 0.137]; 2025 -0.003 [-0.023, 0.017]; 2026 0.014 [-0.005, 0.034].
- Set-aside years: 2021 -0.054, 2022 -0.024 (both negative, as expected in COVID years).
- Contrast D = **-0.046** (pair-bootstrap 95% CI -0.059 to -0.033). Year-level permutation test (8 years, 70 splits):
  one-sided **p = 0.129**; pooled estimator D = -0.049, p = 0.100. Plan rule (p <= 0.05) is **not met**.
- H2 (steady shrinkage) is **not supported**: 2024 is as large as the pre years; the fall is in 2023 (partly) and 2025-26.
- The gap fall is concentrated in 2025 and 2026, the two years with the least reliable data (bot reclassification,
  AI Overviews in India from Aug 2024). Both groups' raw uplifts are negative in 2025-26
  (syllabus -0.026/-0.053; control -0.023/-0.067), i.e. the exam-season rise itself disappeared for both, which
  points to a level shift between baseline (Jul-Oct) and exam months, not a syllabus-specific loss.
- Pre-trend: event-study coefficients (reference 2020) for 2017-2019 are +0.021, +0.011, -0.034 (the 2019 one is
  just significant), so the gap was already drifting down; this limits any causal reading.
- Event-study coefficients, post: 2023 -0.034 (CI -0.060 to -0.008), 2024 +0.025 (-0.001 to 0.051),
  2025 -0.096 (-0.124 to -0.068), 2026 -0.079 (-0.106 to -0.051).

## Robustness (English; D with permutation p)
- R1 drop 2020: -0.045, p 0.200. R2 add 2016 and 2022: -0.066, p 0.036 (252 splits).
- R3 control set B (other areas, 40 pairs): -0.111, p 0.071. R4 strict syllabus list (528): -0.050, p 0.100.
- R5 desktop only (40 pairs with desktop series pulled so far): +0.003, p 0.54; mobile only: -0.082, p 0.057.
  Small subset; desktop-vs-mobile for the full sample waits for the desktop pull.
- R6 windows: -0.053 / -0.063 / baseline Aug-Sep -0.037 (p 0.07-0.14). R7 geometric mean: -0.050, p 0.086.
- R8 by subject: Class 12 Biology -0.099 (p 0.029), Chemistry -0.046, Physics -0.029, Maths -0.006, Class 10 Science -0.040,
  Class 10 Maths +0.015. R9 social science (8 pairs): -0.246, p 0.014 (elections/news; few articles).
- Sign is negative in every specification except desktop-only and Class 10 maths; p-values never go below the
  permutation floor in the main specification.
- R10 India-only (differentially private country files, 6 sampled days per window, only articles above the release
  threshold): gaps 2018 0.079, 2019 0.147, 2020 0.207 (pre); 2024 0.209 (n=12 syllabus); 2025-26 have 4 and 1 articles -
  unusable. Too thin to say anything.
- V2 (peak follows exam date): English gaps in own versus other-regime window are almost identical in 2017-2018, a little
  higher in own window for 2020 and lower for 2019. Windows overlap heavily, so this does not clearly show the peak moved with
  the date. Weak validation.

## Secondary: eve-of-paper spike (D_eve, 2023-26 minus pre)
- All subjects pooled -0.005 [-0.021, 0.011]; science+maths -0.005. By subject: Class 10 Maths -0.051 (CI excludes 0),
  Class 12 Biology -0.033 (CI just excludes 0), Class 12 Chemistry +0.043, Maths +0.027, Physics -0.005. No consistent decline.

## Hindi and Kannada
- Hindi (6 pairs): D = +0.138, CI -0.24 to +0.54, p 0.87. Kannada: nothing. H3 untested. Needs the rest of the pull.

## Verdict (report whichever way it comes out)
- English: a small fall in the syllabus-minus-control exam-season gap (about 4-5 log points), most of it in 2025-26, with
  a pre-trend, a non-monotone path, and a year-level p of 0.13. Under the plan this is "suggestive / no detectable change",
  not support for H1. Whether it reflects ChatGPT, AI Overviews, data reclassification or the 2025-26 level shift cannot be
  separated with this design.
