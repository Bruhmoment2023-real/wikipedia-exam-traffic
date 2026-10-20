# 02 - Design, data documentation and threats to validity

Working title: *Did students stop looking things up? Exam-season Wikipedia traffic for school-syllabus
topics after ChatGPT.*

The research question, hypotheses and analysis plan are in **`02a-analysis-plan-FROZEN.md`**, which was
fixed (SHA-256 and UTC time in `results/plan_freeze.txt`) before any daily page-view series or any
post-2019 number from the Pageviews API had been downloaded. That file is the part suitable for
posting as a plan; read `04-venue.md` on why it should not be called a pre-registration. This file
documents the data, its known breaks, and what a referee will attack.

## 1. Design in six lines

- **Treated group**: 722 English Wikipedia articles mapped from the CBSE Class 10 and 12 science and
  mathematics syllabi (plus 146 social-science articles analysed separately).
- **Control group**: for each, a non-syllabus article from the same broad area with the same
  2016-2019 traffic.
- **Signal**: the CBSE board-exam calendar. Each year's exam window is anchored on the first paper.
- **Outcome**: exam-season uplift = log of mean daily views in the 7-week exam window minus log of
  mean daily views in the previous July-October.
- **Comparison**: (syllabus minus control) in 2023-2026 versus 2017-2020, shown year by year.
- **Editions**: English, Hindi, Kannada, through Wikidata sitelinks of the same articles.

## 2. Data sources (all free, no login)

### 2.1 Pageviews REST API (the main source)

- Endpoint used:
  `https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/{project}/{access}/{agent}/{article}/daily/{start}/{end}`
  - `project`: `en.wikipedia`, `hi.wikipedia`, `kn.wikipedia`
  - `access`: `all-access`, `desktop`, `mobile-web`, `mobile-app`
  - `agent`: `all-agents`, `user`, `spider`, `automated`. This project uses `user` only.
  - One call returns the whole daily series (about 4,100 days); it takes about 1.7 s.
- Coverage: the reference page states the endpoints "serve data starting on July 1, 2015"
  (<https://doc.wikimedia.org/generated-data-platform/aqs/analytics-api/reference/page-views.html>).
  Pulled here: 1 July 2015 - 30 September 2026.
- Access rules followed
  (<https://doc.wikimedia.org/generated-data-platform/aqs/analytics-api/documentation/access-policy.html>):
  - a User-Agent header is required; clients without one "may be blocked without notice". The pipeline
    sends `WikiExamTraffic/0.1 (research on exam-season pageviews; project folder ...; no contact address by policy) python-requests/x`. (The pilot and the first part of the full pull, up to 17 Oct 2026, carried a contact address in the header; changed on 17 Oct 2026 to follow the pack's no-personal-identifier rule.)
  - "To stay within a safe request rate, wait for each request to finish before sending another
    request." The pipeline is strictly sequential with a 0.1 s pause and backs off on HTTP 429/5xx.
  - Data are CC0.
- Licence and reuse: the numbers can be republished; the cached responses are in `data/cache/pv/`.

### 2.2 What a "page view" is, and what `user` means

- Definition (<https://meta.wikimedia.org/wiki/Research:Page_view>): an HTML page request with status
  200/304 to a wiki content path, excluding previews; API requests count only when a mobile app uses
  them to show a page. Edit previews were excluded from 9 Feb 2017.
- Agent types (<https://wikitech.wikimedia.org/wiki/Data_Platform/Data_Lake/Traffic/BotDetection>):
  - `spider` = self-identified crawlers (user-agent based).
  - `automated` = traffic that does not identify itself but behaves like a bot (for example sessions
    with 800 or more views, or more than 30 views a minute). The page reports that in March 2020 the
    split was user 71.55%, spider 22.91%, automated 5.54%, and that labelling automated traffic
    lowers `user` views by about 5%, up to about 8%.
  - So before the `automated` label existed, that traffic sat inside `user`. The date the label
    starts is not given on the page; see section 3, break B1, for how it was checked.
- Redirects: the API counts a view under the title that was requested. A renamed article keeps its
  earlier views under the old name. This is why the pipeline adds old names left by renames.

### 2.3 Per-country data: "pageviews per country per project per page" (differential privacy)

This is the only public source that isolates India at article level. Three datasets, daily files,
read from the READMEs at `https://analytics.wikimedia.org/published/datasets/<name>/00_README.html`:

| Dataset | Dates | Rows released when | Noise | Notes |
|---|---|---|---|---|
| `country_project_page_historical_pre_2017` | 1 Jul 2015 - 8 Feb 2017 | more than 3,500 views | Laplace, scale 300 | no page ids; too coarse for this project |
| `country_project_page_historical` | 9 Feb 2017 - 5 Feb 2023 | more than 450 views | Laplace, scale 30, epsilon 1 | 95% of counts within about 90 of the truth |
| `country_project_page` | 6 Feb 2023 - present | more than 90 views in the lowest risk tier (550 and 1,000 in higher tiers) | Gaussian (zCDP) | counts only each device's first 10 distinct pages per day; stricter bot filter from 25 May 2023 |

- Columns: country, country code, project, page id, page title, Wikidata id, noisy count.
- Granularity: one file per day, every country not on the protection list, every project.
- Size: about 6 MB a day (historical) and 18-27 MB a day (current). All days for 2017-2026 would be
  roughly 40 GB, so only 72 sampled days were downloaded (about 410 MB transferred, India rows kept).
- What it means for this study:
  - **The release rules change on 6 February 2023, ten weeks after ChatGPT's launch and inside the
    2023 exam window.** Levels before and after cannot be compared. Seasonal ratios can be compared
    only when both windows of an exam year sit inside one regime, so 2023 is unusable.
  - Only high-traffic article-days appear. On 5 March 2019, 150 of the 868 syllabus articles had a
    released India row (threshold 450); on 1 March 2024, 506 did (threshold 90). The India check is
    therefore a check on the most-viewed syllabus articles, with values below 450 discarded in both
    regimes.
  - Hindi rows exist (412 Hindi-Wikipedia rows for India on 5 Mar 2019); Kannada rows are too small
    to be released.
- A by-country endpoint also exists in the Pageviews API, but for whole projects, not articles.

### 2.4 Bulk dumps (not used)

- `dumps.wikimedia.org/other/pageview_complete/` (from December 2007) and `/other/pageviews/` (hourly,
  "filtered to human traffic", from May 2015). Hourly files are tens of MB each; an 11-year pull is
  hundreds of GB. Not downloaded. They would be needed only for an hour-of-day analysis (for example
  views during Indian evening hours), which is a possible extension on a bigger machine.
- Monthly clickstream (referrer -> article) exists for English, Russian, German, Spanish and Japanese
  only (per the dumps index page), so it cannot separate search referrals for Hindi or Kannada.

### 2.5 Syllabus documents and topic mapping

- CBSE curriculum PDFs, downloaded from `cbseacademic.nic.in` (2020-21 and 2024-25 editions of
  Secondary Science, Mathematics, Social Science and Senior Secondary Physics, Chemistry, Biology,
  Mathematics): `data/syllabus/`.
- Topic names only were taken. The hand mapping is `data/topics_raw.txt`; the resolved list is
  `data/syllabus_articles.csv` (868 unique articles from 871 mappings). Columns record the rule
  (R1 exact title, R2 named concept with different wording, R3 article broader or narrower) and flags.
- Automatic checks on every mapping:
  - a keyword for the topic is searched in the text of both syllabus editions for that subject;
  - 81 articles: keyword not found in either text (the topic is textbook-chapter content that the
    syllabus document does not name, e.g. "Xylem", "Tyndall effect"); these are still in the main
    sample but excluded in robustness check R4;
  - 133 articles: found in 2020-21 but not in 2024-25. This list reproduces the 2022-23
    "rationalisation" (periodic classification, sources of energy, polymers, chemistry in everyday
    life, solid state...). **These topics left the syllabus at the same time as ChatGPT arrived**,
    so their exam peak should fall for a reason unrelated to AI; R4 removes them;
  - 10 articles flagged ambiguous (broader/narrower).
- Hindi and Kannada: 669 and 321 of the 868 syllabus articles have a sitelink.
- **Not included: Cambridge IGCSE.** Its topics overlap almost entirely with the CBSE list, its
  candidates in India are few compared with CBSE's (CBSE Class 10 had about 2.4 million registered
  candidates in 2025 per the English Wikipedia infobox - not verified against CBSE), and its exam
  series (March, May-June, October-November) would need separate windows. It is a natural extension:
  see `code/README.md`.

### 2.6 Controls

- Candidate pool: English Wikipedia "Vital articles, Level 4" lists (about 10,000 articles sorted by
  subject). Excluded: syllabus articles, and any article whose title occurs anywhere in the 14
  syllabus texts.
- Control A (same area) and Control B (other areas); matching on log mean daily views 2016-2019.
  Match quality: median absolute log gap 0.002-0.015; at least 98% of control-A pairs within 0.25
  (`results/log_02_controls.txt`).
- Limits of the control group:
  - "Not on the CBSE syllabus" does not mean "not studied": a vital science article (say "Quasar") is
    read by students somewhere. It only needs to lack a *CBSE February-March* peak.
  - Controls are also exposed to ChatGPT. The design does not estimate the effect of AI on traffic
    levels; it estimates the change in the exam-season component relative to the control.

### 2.7 Exam dates

- `data/exam_dates.csv`, one row per date with its verification status. Primary CBSE date sheets were
  recovered from the Internet Archive for 2017, 2020, 2021 (planned), 2023, 2024, 2025 and 2026
  (`data/datesheets/`); scanned ones were read page by page.
- **Not verified from a primary document**: 2016 (first exam 1 March - from memory), 2018 (5 March -
  news reports), 2019 (15/21 February - a news site's reproduction of the date sheet), 2022 term 2
  (26 April - a news site's table).
- Known oddities to state in the paper:
  - Class 10 board exams were optional until 2017 and compulsory again from 2018 (from memory -
    **unverified**; the Wikipedia article on the exam says the CCE scheme was replaced from 2017-18).
  - 2018: paper leaks (Class 12 Economics re-held 25 April 2018; Class 10 Mathematics affected),
    confirmed by a CBSE press release in `data/datesheets/2018_new_exam_date.pdf`.
  - 2020: papers after 18 March were postponed (unverified detail); 2021: boards cancelled;
    2022: two-term system, term 1 multiple-choice papers in Nov-Dec 2021, term 2 in Apr-Jun 2022.
  - 2026: first year of two board exams for Class 10 (a second sitting later in the year).
- Other boards (state boards, ICSE, Karnataka SSLC and PUC) are not modelled. Karnataka's own calendar
  matters most for the Kannada edition and is the first thing to add.

## 3. Known breaks in the series, and what the design does about each

| # | Break | When | Effect | Handling |
|---|---|---|---|---|
| B1 | `automated` agent label introduced; before it, undeclared bots count as `user` | around April-May 2020 (to be confirmed, see pilot notes below) | `user` levels drop about 5% | affects both groups; outcome is a within-year ratio; 2020's windows are both before it, 2021-22 are set aside |
| B2 | Bot-detection logic updated, March-August 2025 traffic reclassified (Wikimedia, Oct 2025) | 2025 | `user` series for 2025 may be revised; bursts of evasive bots (largely from Brazil) in May-June 2025 | exam window (Jan-Mar 2025) is mostly before the reclassified months; baseline for exam year 2026 is Jul-Oct 2025, inside the affected period, so **2026 is the least trustworthy year**; geometric-mean check R7 dampens bursts |
| B3 | Per-country data change rules | 6 Feb 2023 | no level comparison across it | India check uses within-regime years only |
| B4 | Mobile shift: readers move from desktop to mobile web and apps | gradual, whole period | composition change | desktop and mobile analysed separately (R5); app views counted in all-access |
| B5 | Google AI Overviews in India (English and Hindi) | announced August 2024 (Google India blog and news reports; exact day not checked) | fewer search click-throughs | exam seasons 2025 and 2026 carry ChatGPT **and** AI Overviews; 2023 and 2024 carry ChatGPT only. The design cannot separate the two after 2024 |
| B6 | Article renames and redirects | any time | views split across titles | old names from renames since 2015 are summed in; other redirects are not (limitation) |
| B7 | COVID-19 school closures | Mar 2020 - early 2022 | traffic surge, cancelled exams | 2021 and 2022 set aside; 2020 windows precede the lockdown; R1 drops 2020 |
| B8 | Syllabus "rationalisation" | 2022-23 onwards | some topics no longer examined | R4 strict list |
| B9 | Exam calendar moved from March to mid-February | 2019 | window moves relative to other seasonal events (US/UK school terms) | windows are anchored on each year's own first paper; a fixed-calendar window is check R6 |
| B10 | News events on particular articles (elections, anniversaries) | irregular | spikes | science and maths are the primary sample; social science separate; geometric mean check |

## 4. Threats to validity: what a referee will attack

1. **Page views are global, not Indian.** English Wikipedia's exam-season pattern mixes Indian
   students with everyone else. Defences available: (a) the window is the *CBSE* calendar, which no
   other large exam system shares (US AP exams are in May, UK GCSEs May-June); (b) the peak moved
   when CBSE moved its calendar (validation V2); (c) the eve-of-paper spike on exact CBSE dates;
   (d) Hindi and Kannada editions are read almost only in India; (e) the India-only check R10.
   None of these makes the English estimate an India estimate. Say so.
2. **Many things changed after 2022.** ChatGPT, then Gemini and others, AI Overviews in India from
   August 2024, YouTube and coaching apps, cheaper mobile data, the syllabus cut, and exam-pattern
   changes (more competency questions). The design identifies a change in the exam peak of syllabus
   articles relative to controls. It does not identify the cause. "After ChatGPT" is a date, not a
   proven mechanism.
3. **Only eight exam seasons.** Four before, four after. The honest sample size for a before/after
   claim is 8, which is why the plan uses a year-level permutation test whose smallest possible
   one-sided p-value is 1/70 = 0.014, and shows every year.
4. **Pre-trends.** If the gap was already falling in 2017-2020 (for example because students were
   moving to YouTube), a lower post-period gap proves nothing new. The event-study table is the check.
5. **The window is a choice.** A 7-week window anchored on the first paper, and a July-October
   baseline. R6 varies both.
6. **Control contamination.** Some controls are on other syllabi or are studied at university; this
   biases the gap towards zero in every year, and matters only if it changes over time.
7. **Mapping is hand-made by one person (with AI assistance).** 868 mappings, 10 flagged ambiguous,
   81 not literally in the syllabus text. A second person should check a random 10%.
8. **Differential traffic composition.** Syllabus articles may get more of their traffic from Google
   than controls do; then AI Overviews would hit their *level* harder all year. The outcome is a
   ratio within the year, which removes a constant proportional loss, but not a loss that is larger
   in exam season (which is exactly the effect of interest, whatever the channel).
9. **Bots.** A scraper burst inside one window of one year moves an arithmetic mean. R7.
10. **Low counts in Kannada.** Most Kannada articles get a handful of views a day. Article-level logs
    are unusable below about 5 views a day; the pooled estimator is used and its intervals are wide.
11. **Researcher degrees of freedom.** The plan was fixed before the post-period data were seen, but
    only locally and on the same day; a sceptic has to take that on trust plus a file hash. The real
    remedy is the 2027 season.
12. **What page views cannot show.** A view is not learning. Fewer views in exam season could mean
    students ask a chatbot, or use an app, or that Google answers on the results page. It is a
    measure of where students go, not of what they know.

## 5. Ethics

- Aggregate public data only; no individuals, no accounts, no scraping beyond documented APIs.
- The per-country files are differentially private by construction.
- No human participants, so no consent or ethics-board question arises. A journal may still ask for a
  one-line ethics statement; this is it.

## 6. Verification update, 17 Oct 2026

- **B1 (automated label date)**: the Wikitech bot-detection page was re-read; it gives no introduction date,
  only a March 2020 comparison ("Effect of automated-traffic detection on Pageview metric - March 2020") and
  says the method "changes the agent_type field of some pageviews from user to automated". The date is
  therefore **not verified**. Consequence: the `user` series before and after the change is not strictly
  comparable; because the outcome is a within-year ratio and both groups are affected alike, the design
  is robust to a proportional shift, not to one that differs between exam season and baseline.
- **B5 (AI Overviews India)**: news reports (Business Today 16 Aug 2024, Inc42, IndiaAI) and a Google India
  blog post say AI Overviews expanded in August 2024 to India (English; Hindi reported), plus the UK, Japan,
  Indonesia, Mexico and Brazil, gradually over weeks. Search snippets only; the Google blog page was not
  opened in full. Kannada: no evidence of launch found (not checked).
- The 2025 bot-reclassification statement comes from the WMF Diff post of 17 Oct 2025 (read through a
  summary tool on 13 Oct, not verbatim).
- **Exam dates**: 2016, 2018, 2019 and 2022 term 2 remain without a primary CBSE document (Wayback
  availability lookups for guessed 2016/2019 URLs returned no snapshot). These years enter the main contrast
  (2018, 2019). Mitigation: V2 (peak follows exam date) and robustness check R1/R6 (fixed calendar window).
