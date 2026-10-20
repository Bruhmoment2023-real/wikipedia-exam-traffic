# Pipeline: exam-season Wikipedia traffic

Everything runs with the project's own Python environment:

    D:\Research-Publishing\05-wikipedia-exam-traffic\.venv\Scripts\python.exe <script>

Run from inside `code\`. No accounts, keys or paid services. All network calls go to Wikimedia
(Pageviews REST API, MediaWiki Action API, Wikidata, the public per-country files). Requests are
sequential, paced (`common.MIN_INTERVAL`), carry a descriptive User-Agent with a contact address, and
every response is cached under `data\cache\`, so re-running a step costs nothing and an interrupted
step resumes where it stopped.

| Step | Script | Reads | Writes | Network |
|---|---|---|---|---|
| 1 | `01_build_topics.py` | `data\topics_raw.txt`, `data\syllabus\*.txt` | `data\syllabus_articles.csv`, `data\topic_mapping_all_rows.csv` | about 40 calls |
| 2 | `02_build_controls.py` | step 1 output | `data\control_candidates.csv`, `data\control_articles.csv` | about 3,200 small calls (monthly views 2016-2019 only), about 25 min |
| 3 | `03_pull_pageviews.py --pilot` or `--full` | steps 1-2 | `data\titles_pilot.csv` / `titles_full.csv`, `data\cache\pv\...` | one call per title and access type, about 1.7 s each |
| 4 | `04_build_panel.py pilot` or `full` | cache | `data\panel_<name>_<lang>.npz` + `_index.csv` | none |
| 5 | `05_analyze.py <name> pre` then `05_analyze.py <name> all` | panels, `data\exam_dates.csv` | `results\*.csv` | none |
| 6 | `06_india_country.py download` then `analyze` | steps 1-2 | `data\cache\country_in\`, `results\R10_india_only.csv` | 72 files, about 410 MB transferred, India rows kept (27 MB) |
| 7 | `07_figures.py <name>` | panels, results | `results\fig*.png` | none |

`pre` in step 5 masks every day after 30 June 2020 before any number is computed; it was run first,
to validate the design, before the `all` stage was run (see `02a-analysis-plan-FROZEN.md` and
`results\plan_freeze.txt`).

## Hand-made inputs (the parts a reader must be able to audit)

- `data\topics_raw.txt` - every syllabus topic and the English article it was mapped to, with the rule
  (exact title / named concept with different wording / article broader or narrower).
- `data\exam_dates.csv` - CBSE exam dates with, for each row, whether it was read from a primary CBSE
  document (copies in `data\datesheets\`), a secondary news source, or memory (marked UNVERIFIED).
- `data\syllabus\` - the CBSE curriculum PDFs for 2020-21 and 2024-25 and their extracted text.

## Rules built into the code

- Article series = current title + old names left behind by renames since mid-June 2015 (English: redirect page id above
  47,000,000 and last revision = the automatic "moved page" edit) + the syllabus wording when it is a redirect. Hindi and Kannada: current title only in the full pull (up to three redirects in the pilot).
- Controls are matched on 2016-2019 traffic only.
- Random seeds are fixed (20261013).

## To change the scope

- Add or correct a topic: edit `data\topics_raw.txt`, then rerun steps 1-5 (cached calls are reused).
- Add Cambridge IGCSE or a state board: add sections to `topics_raw.txt` with a new subject code, add
  the syllabus text file to `SYL` in `01_build_topics.py`, and add the board's exam dates.

## Status notes (17 Oct 2026)
- User-Agent no longer carries a contact address (rule: no personal identifier in requests). Earlier pulls did.
- `08_igcse_overlap.py`: keyword overlap of the CBSE list with Cambridge IGCSE Physics/Chemistry/Biology 2023-25
  syllabi (`data/igcse/`). Coverage check only; IGCSE-only topics are not mapped to articles.
- Full pull: English all-access complete; Hindi about a third, Kannada about 10%; desktop only for the pilot's 148 articles.
  Resume with `03_pull_pageviews.py --full` (about 0.15 requests/s on the loaded laptop; roughly 8 hours left; strictly
  sequential per the API policy). Then `04_build_panel.py full`, `05_analyze.py full all`, `06_india_country.py analyze`,
  `07_figures.py full`.
- `05_analyze.py` sets desktop/mobile to NaN for articles whose desktop series has not been pulled.
