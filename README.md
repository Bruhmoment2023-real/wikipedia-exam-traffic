# Did students stop looking things up? Exam-season Wikipedia traffic for Indian school-syllabus topics before and after ChatGPT

Sean Solano Paul, Independent researcher, Bengaluru, India. Funding: none. Competing interests: none.

## Summary

Students in India revise for CBSE Class 10 and Class 12 board exams on fixed dates, and part of that
revision shows up as a rise in Wikipedia views of syllabus topics. This repository holds the code,
processed data and results for a study that uses the CBSE exam calendar to measure that rise and asks
whether it shrank after ChatGPT was released in November 2022. 711 English Wikipedia articles on the
CBSE science and mathematics syllabi are matched to non-syllabus control articles with the same
2016-2019 traffic, and each article's views in a seven-week exam window are compared with its views in
the previous July to October. The analysis plan was frozen before the post-period data were
downloaded (`docs/02a-analysis-plan-FROZEN.md`, `results/plan_freeze.txt`). The Hindi and Kannada
editions are pulled but not yet tested.

## Layout

| Path | Contents |
|---|---|
| `code/` | Numbered pipeline scripts `01`-`08` plus `common.py`; `code/README.md` gives inputs, outputs and network use of each step |
| `data/` | Syllabus-to-article mapping (`topics_raw.txt`, `syllabus_articles.csv`, `topic_mapping_all_rows.csv`), control articles, `exam_dates.csv`, title lists, daily page-view panels (`panel_*.npz` with `_index.csv`), `igcse/overlap.csv` |
| `data/cache/` | Cached Wikimedia API responses (page views, redirects, last revisions, sitelinks, India country rows) so that re-runs cost no network |
| `results/` | Result tables (CSV), figures (`fig1`-`fig4` PNG), run logs, `RESULTS-SUMMARY.md` |
| `docs/` | Prior-work review, study design, frozen analysis plan, data dictionary, references (`.bib`, `.ris`), `appendix/rerun.ps1` |
| `bibliometrics/` | Literature map (631 records): scripts, search protocol, cleaned corpus tables, figures |

## How to reproduce

Python 3.12. From the repository root:

```
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt     # Windows; use .venv/bin/ elsewhere
cd code
python 01_build_topics.py
python 02_build_controls.py
python 03_pull_pageviews.py --full        # or --pilot
python 04_build_panel.py full
python 05_analyze.py full pre             # validation stage: masks all days after 30 June 2020
python 05_analyze.py full all
python 06_india_country.py download       # then: python 06_india_country.py analyze
python 07_figures.py full
python 08_igcse_overlap.py
```

Steps 2, 3 and 6 call Wikimedia services and are slow (sequential, paced). Responses are cached under
`data/cache/`, so the shipped cache lets steps 3-7 run without the network for cached items.
Step 1 needs the CBSE syllabus text (see "Not included"). Random seed 20261013.
`docs/appendix/rerun.ps1` shows the order used on the author's machine; its paths are the author's
and need editing. See `code/README.md` for exact arguments.

The paper's Figures 1 and 2 (English, single panel) are drawn by `code/make_figs_v10.py` (numpy and Pillow) from
`data/panel_full_en.npz`, `data/panel_full_en_index.csv` and `results/yearly_gaps_full_all.csv`; set `PACK` and
`PAPER` at the top of the script to the repository root. Outputs: `results/fig1_seasonal_profile_en_v10.png`,
`results/fig2_yearly_gap_en_v10.png` and the plotted Figure 1 values `results/fig1_profile_values_v10.csv`.

## Data sources and licences

| Source | Used for | Licence / status |
|---|---|---|
| Wikimedia Pageviews REST API, per-article daily views | Outcome series (`data/cache/pv`, `panel_*`) | CC0 (Wikimedia analytics data) |
| Wikimedia public per-country page-view files (India rows only) | Country check (`data/cache/country_in`) | CC0 |
| MediaWiki Action API / Wikidata | Redirects, last revisions, sitelinks | Only titles and ids kept; Wikidata CC0 |
| CBSE exam dates (hand-entered in `data/exam_dates.csv`) | Exam windows | Facts read from CBSE datesheets; each row notes its source type |
| OpenAlex, Crossref, Semantic Scholar, ERIC, arXiv metadata | Literature map | Open metadata (OpenAlex CC0); see `LICENSE-DATA.md` |
| Author's derived data, results, figures | | CC BY 4.0 (`LICENSE-DATA.md`); code MIT (`LICENSE`) |

## Not included and why

- Abstract text of third-party papers (the `abstract`/`AB` columns and abstract-derived quote columns of the bibliographic tables, and abstract fields in the OpenAlex JSON). Identifiers, titles, years, venues, keywords and citation data are kept; re-fetch abstracts with the bibliometrics pipeline if needed.
- Per-paper reading notes on the literature (they contain quotations from copyrighted papers) and the literature gap-analysis note (scoping). The scripts that built the notes are kept; run them on your own copies of the papers.
- CBSE syllabus PDFs and text, CBSE datesheet PDFs and text (`data/syllabus/`, `data/datesheets/`): third-party documents, not clearly redistributable. Obtain from cbseacademic.nic.in; `exam_dates.csv` records the dates taken from them.
- Cambridge IGCSE past-paper PDFs (`data/igcse/`): copyrighted. Only `overlap.csv` (derived) is kept.
- Full-text PDFs and text of the cited papers (`lit/`, `bibliometrics/pdfs/`): copyrighted or licence-restricted. Fetch via DOIs in `docs/citations/references.bib`.
- Raw per-query API dumps of the literature search (`bibliometrics/data/raw/{arxiv,crossref,eric,openalex,s2}`): reproducible with `bibliometrics/python/pipeline.py`. The merged hit list `all_hits.csv` is kept with third-party email addresses redacted.
- Virtual environment, bytecode caches, and internal status/venue/outline files.
- No file larger than 50 MB was found; none excluded for size.

## Citation

See `CITATION.cff`. Solano Paul, S. (2026). *Did students stop looking things up? Exam-season Wikipedia traffic for Indian school-syllabus topics before and after ChatGPT* (code and data). Independent researcher. A Zenodo DOI will be added when the repository is made public.
