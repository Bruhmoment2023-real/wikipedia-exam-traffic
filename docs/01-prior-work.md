# 01 - Prior work and novelty verdict

Compiled 13 October 2026. For each item the line "Read:" says exactly what was opened:
**full text** (PDF downloaded to `lit/` and the relevant sections read), **abstract** (abstract only),
or **metadata** (existence confirmed in Crossref / arXiv / OpenAlex, nothing read).
OpenAlex returned HTTP 429 (rate limit) for every keyword search on this day, so the search ran on
the arXiv API and the Crossref API plus citation-following from the papers read. That is a real gap:
see "What the search did not cover" at the end.

## Novelty verdict (short)

- **The broad question is taken.** A February 2026 physics-education preprint (Ben-Zion, Michaeli and
  Finkelstein) already reports that page views of physics-concept Wikipedia articles fell between the
  2022-23 and 2024-25 academic years in seven languages including Hindi, and that Google searches for
  the same concepts fell in 20+ countries including India, while "the seasonal structure characteristic
  of academic activity remains robust". Sean's paper cannot claim to be first to ask whether students
  look things up less after ChatGPT, or first to look at Hindi Wikipedia.
- **What nobody appears to have done** (in what was searched):
  1. use a **published exam calendar with exact dates** (CBSE date sheets, which moved between March
     and mid-February across years) as the identifying signal on Wikipedia page views;
  2. measure the **size of the exam-season peak itself** (peak relative to the same article's quiet
     months) rather than the yearly level of traffic;
  3. compare against **matched non-syllabus control articles**, with **pre-2022 years as the baseline**
     (Ben-Zion et al. start in August 2022, so their "reference" year is already partly post-ChatGPT,
     and they have no control group);
  4. build the article list from a **whole school syllabus** (868 articles across seven subjects)
     rather than 62 hand-picked physics terms;
  5. include **Kannada**, or any Indian language other than Hindi.
- **Honest label: "new angle on a question others have opened", not "first".** The defensible
  contribution is the design (exam calendar + controls + pre-period), applied to India.
- A reviewer who knows Ben-Zion et al. will ask why this adds anything. The answer has to be the three
  design features above, and the fact that this design can separate "traffic fell" (which also fell
  for controls) from "the exam peak shrank".

## A. Closest work: generative AI and Wikipedia readership

**A1. Ben-Zion, Michaeli, Finkelstein (2026). "From Search to GenAI Queries: Global Trends in Physics
Information-Seeking Across Topics and Regions."** arXiv:2602.09550 (physics.ed-ph), v1 10 Feb 2026.
<https://arxiv.org/abs/2602.09550> - **Read: full text** (23 pp).
- Google Trends weekly relative search volume for 62 mechanics and electromagnetism topics, 15 Aug 2022
  to 14 Aug 2025, 20+ countries; Wikipedia page views for the same topics in seven languages
  (English, Hindi, Spanish, Arabic, Portuguese, Italian, German) as a cross-check.
- Finds large declines in search for most topics (for India, e.g. "Newton's laws of motion" -36%,
  "Kinetic energy" -18% between 2022-23 and 2024-25); English Wikipedia declines average about 20%,
  other languages more, "around or exceeding 50%" for some topics in Hindi.
- States that weekly series stay highly correlated across years, i.e. the academic seasonal pattern
  survives while the level falls. They do not test whether the peak-to-baseline ratio changed.
- No control articles; no pre-ChatGPT years; academic calendar used only as US semester markers on a
  figure; "the analysis does not attempt to align academic calendars across countries".
- **This is the paper Sean must cite first and distinguish from.**

**A2. Reeves, Yin, Simperl (2025). "Exploring the impact of ChatGPT on Wikipedia engagement."**
*Collective Intelligence*. DOI 10.1177/26339137251372599 (open access); preprint arXiv:2405.10205.
- **Read: full text of the arXiv version** (12 pp); journal abstract via OpenAlex.
- 12 language editions, 1 Jan 2021 - 1 Jan 2024, edition-level page views, visitors, edits, editors;
  six languages where ChatGPT was available and six where it was not; Wilcoxon tests and a panel
  regression with week-of-year and day-of-week terms.
- Finds no overall fall; views rose after launch, but rose less where ChatGPT was available.
- Edition-level totals only: no article-level or topic-level analysis, nothing on education.

**A3. Lyu, Siderius, Li, Acemoglu, Huttenlocher, Ozdaglar (2025). "Wikipedia Contributions in the Wake
of ChatGPT."** arXiv:2503.00757 (WWW '25 Companion). <https://arxiv.org/abs/2503.00757>
- **Read: full text** (4 pp).
- Difference-in-differences across articles: articles whose content is "similar" to what ChatGPT 3.5
  produces versus "dissimilar" articles, two-year window centred on November 2022.
- Finds larger falls in edits and views for similar articles, mostly among newly created popular ones.
- Closest in *method* (article-level DiD with a control group). The grouping variable is similarity to
  ChatGPT output, not syllabus membership, and there is no seasonal outcome.

**A4. Khosravi, Yoganarasimhan (2026). "Impact of AI Search Summaries on Website Traffic: Evidence from
Google AI Overviews and Wikipedia."** arXiv:2602.18455 (v6, Sept 2026).
- **Read: full text, sections 1-2** (32 pp; estimation sections skimmed).
- Monthly clickstream referrals from search engines, Dec 2023 - Dec 2024; English articles (treated by
  the US default rollout of AI Overviews on 15 May 2024) versus the same articles in German and French.
- Finds English search referrals fell 5.45% (vs German) and 4.82% (vs French).
- Matters here because it shows the second shock (AI answers inside Google) is measurable and separate
  from ChatGPT. The public clickstream covers only a few languages (not Hindi or Kannada).

**A5. Wikimedia Foundation, Marshall Miller (17 Oct 2025). "New User Trends on Wikipedia."** Diff blog.
<https://diff.wikimedia.org/2025/10/17/new-user-trends-on-wikipedia/> - **Read: page text, through
an automated summary of the page** (not a verbatim reading; quotations should be re-checked by Sean).
- After bot-detection logic was updated, human page views were "roughly 8%" lower than in the same
  months of 2024; traffic for March-August 2025 was reclassified; much of an apparent rise in May-June
  2025, largely from Brazil, was bots built to evade detection. The Foundation attributes the decline
  to generative AI in search and to social video.
- This is both prior evidence and a data-quality warning for 2025 (see `02-design.md`).

## B. Generative AI and other knowledge sites

**B1. del Rio-Chanona, Laurentsyeva, Wachs (2024). "Large language models reduce public knowledge
sharing on online Q&A platforms."** *PNAS Nexus*. DOI 10.1093/pnasnexus/pgae400.
- **Read: full text of the 2023 arXiv version** (arXiv:2307.07367, 19 pp), journal version: metadata.
- Stack Overflow posting versus Russian- and Chinese-language counterparts and mathematics forums;
  DiD estimate of about a 16% fall after ChatGPT, rising to about 25% within six months.
- The template for "treated platform versus less-exposed comparison" that this project borrows.

**B2. Burtch, Lee, Chen (2024). "The consequences of generative AI for online knowledge communities."**
*Scientific Reports*. DOI 10.1038/s41598-024-61221-0. - **Read: metadata only.**

**B3. Helic, Santos (2025). "Stack Overflow Is Not Dead Yet: Crowd Answers Still Matter."**
arXiv:2509.05879. - **Read: abstract and method paragraph.** Uses week-of-year and day-of-week
controls for seasonality in a DiD around the launch.

**B4. Han, Kim, Yun (2026). "The Uneven Decline of Collective Knowledge Production: Evidence from Stack
Overflow After Generative AI."** arXiv:2609.36069. - **Read: abstract.** Easy questions fall,
hard ones become relatively more common.

**B5. Kim, Vitale, Hemphill (2026). "Navigating the Changing Landscape of Online Knowledge Consumption
and Production in the Age of Generative AI."** arXiv:2609.38563. - **Read: abstract.**

## C. The academic calendar as a signal in online traces (the identification idea)

**C1. Arslan, Tiwari, Piech (2020). "Using Google Search Trends to Estimate Global Patterns in
Learning."** *Proc. Learning @ Scale 2020*. DOI 10.1145/3386527.3405913. - **Read: metadata only**
(described in A1 as showing that computer-science searches in 120+ countries follow academic calendars
and dropped at the March 2020 school closures).

**C2. Gillis, Garrison (2022). "Confounding Effect of Undergraduate Semester-Driven 'Academic' Internet
Searches on the Ability to Detect True Disease Seasonality in Google Trends Data."** *JMIR
Infodemiology* 2, e34464. DOI 10.2196/34464. - **Read: metadata only** (described in A1 as showing
"academic cycling" of technical search terms with peaks at exam periods).

**C3. Bilen, Matros (2021). "Online cheating amid COVID-19."** *Journal of Economic Behavior &
Organization*. DOI 10.1016/j.jebo.2020.12.004. - **Read: metadata only** (described in A1 as hourly
Google Trends spikes for physics terms during unproctored online AP exams in 2020). Relevant to the
eve-of-paper outcome: exam timing shows up in search at fine resolution.

**C4. Mittermeier, Roll, Matthews, Grenyer (2019). "A season for all things: Phenological imprints in
Wikipedia usage and their relevance to conservation."** *PLOS Biology*. DOI
10.1371/journal.pbio.3000146. - **Read: metadata only** (cited in A2). Shows seasonality in
Wikipedia page views is an established measurement object, for species articles.

- So: exam-calendar seasonality is established for **Google Trends** (C1-C3) and seasonality is
  established for **Wikipedia** in other domains (C4), and A1 notes academic seasonality in passing.
  **No study was found that uses a school board's dated exam timetable to identify student traffic in
  Wikipedia page views, before or after ChatGPT.** That absence is from a limited search and should be
  stated as "we found none", not "none exists".

## D. Who reads Wikipedia, and why (background for the mechanism)

**D1. Singer, Lemmerich, West, Zia, Wulczyn, Strohmaier, Leskovec (2017). "Why We Read Wikipedia."**
*WWW 2017*. DOI 10.1145/3038912.3052716; arXiv:1702.05379. - **Read: full text, relevant sections.**
Survey of about 30,000 English Wikipedia readers; "work or school" is one of seven motivations, and
those readers spend longer on single articles, focused on topics such as science.

**D2. Lemmerich, Saez-Trumper, West, Zia (2019). "Why the World Reads Wikipedia: Beyond English
Speakers."** *WSDM 2019*; arXiv:1812.00474. - **Read: full text, relevant sections.** 14 languages
including Hindi (3,064 responses). Work/school tasks average 18% of stated motivations; Hindi readers
report "intrinsic learning" in 48% of responses and in-depth reading 68% of the time.

**D3. Piccardi, Gerlach, Arora, West (2023). "A Large-Scale Characterization of How Readers Browse
Wikipedia."** *ACM Transactions on the Web*; arXiv:2112.11848. - **Read: abstract.** Most sessions are
single page loads arriving from search engines, which is why changes in search (AI Overviews) matter.

## E. What the search did not cover (say this in the paper)

- OpenAlex keyword search failed all day (HTTP 429). Semantic Scholar and Google Scholar were not
  queried. SSRN, EdArXiv and SocArXiv were not searched directly.
- No search in Hindi or Kannada, and none of Indian education journals.
- The Wikimedia Research newsletter and Wikimedia's own research reports were not searched.
- Before relying on the novelty claim, rerun at least: Google Scholar "Wikipedia" + "exam" + "page views";
  "Wikipedia" + "CBSE"; forward citations of A1, A2 and A3; and the OpenAlex queries in
  `lit/oa.py`. Search logs for today are in `lit/search_*.txt`.

## F. One-paragraph positioning Sean can argue in his own words (bullets, not text to copy)

- Others showed levels fell (A1) or did not fall at the edition level (A2); article-level DiD exists for
  ChatGPT-similar content (A3) and for AI Overviews (A4).
- None uses the timing of exams. Exam timing is a signal that only students generate, and in India it
  is dated to the day and shifted by three weeks in 2019.
- This paper asks a narrower question than "did traffic fall": did the part of traffic that is
  plausibly exam revision fall relative to the same article's ordinary traffic and relative to
  similar articles that are not on the syllabus.

## G. Search update, 17 Oct 2026 (logs: `lit/search_arxiv3_followup.txt`, `lit/search_crossref3_followup.txt`)
- arXiv API (abstract-field queries on Wikipedia + ChatGPT + views; + generative AI + readership): only Reeves et al.
  (2405.10205) and an unrelated language-bias paper (2303.16281) returned. Metadata only.
- Crossref (three queries): nothing new on exam seasons or ChatGPT and Wikipedia views; the Khosravi & Yoganarasimhan SSRN
  version (10.2139/ssrn.6164926) appears. Metadata only.
- OpenAlex: one full-text probe worked (no new relevant hit); Semantic Scholar returned HTTP 429, not retried (no key allowed).
- **Novelty verdict unchanged**: no study found that uses a school-board exam timetable to measure the exam-season peak in
  Wikipedia views with matched controls before and after ChatGPT; closest remains Ben-Zion et al. (2602.09550). "We found
  none" is the correct wording. The exam-season gap result is also weak (`results/RESULTS-SUMMARY.md`), so novelty is in the design.
- Wikimedia's own statements: Diff post 17 Oct 2025 re-read via summary tool: human pageviews down "roughly 8%"; traffic for
  March-August 2025 reclassified; unusual traffic "mostly originating from Brazil" from about May 2025; decline attributed to generative AI and social media.
