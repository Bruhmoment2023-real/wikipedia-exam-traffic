# Archive v17: completed analysis and exploratory extensions (November 2026)

Contents
- `PLAN-exploratory.md` and `PLAN-exploratory.sha256.txt`: the time-stamped plan for the exploratory extensions (E1-E7), written before the extension analyses were run, with its labelled amendments A1-A6. `frozen_code_hashes.txt`: SHA-256 of the unchanged frozen scripts `code/03_pull_pageviews.py`, `04_build_panel.py`, `05_analyze.py` in the repository root (they still match). The frozen plan itself is `docs/02a-analysis-plan-FROZEN.md`.
- `code/`: extension scripts. `ext_pull.py` and `queue_pull.py` fetch the additional page-view series (agent types, placebo pages); `ext_analysis.py` runs E1-E4, E6; `ext_click.py` runs E5 and E7 on the clickstream files; `make_figs_v17.py` draws the figures of the paper; `dl_clickstream.sh` downloads the 12 English clickstream monthly files.
- `data/`: rebuilt panels (`panel_full_{en,hi,kn}.npz` with index files), `placebo_pairs.csv`, `e3_sample_titles.csv`, and the complete cached Wikimedia page-view responses of the November rerun (`pv_cache/` for all-access, desktop and mobile-app views; `pv_agent_cache/` for the `all-agents` and `automated` series).
- `clickstream_filtered/`: the English clickstream rows used (arrivals at the 711 syllabus and 711 control articles) for 12 monthly files, taken from the Wikimedia clickstream dumps (CC0).
- `results/main_rerun/`: the frozen pipeline rerun of 18 November 2026 on the completed pull (Hindi and Kannada tested, desktop and mobile on 155 pairs). The English main specification reproduces the October numbers exactly (711 pairs, D = -0.046, permutation p = 0.129). The files in the repository root `results/` are the earlier October run.
- `results/extensions/`: tables and logs of E1-E7.
- `figures/`: Figures 1-9 of the paper (600 dpi).

Reproduction: place the files of `data/` and the cached responses where the frozen scripts expect them (`data/cache/pv`, `data/cache/pv_agent`), then run `code/04_build_panel.py full`, `code/05_analyze.py full all`, and the extension scripts. Paths at the top of each script are the author's D: paths and must be edited to the repository location. Random seed 20261013 as in the main pipeline.

Not included: the 12 raw clickstream files (4.9 GB in total; `dl_clickstream.sh` downloads them from dumps.wikimedia.org), CBSE syllabus and datesheet documents (see the repository README), and abstracts or full text of third-party papers.
