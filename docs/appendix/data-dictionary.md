# Data dictionary - 05-wikipedia-exam-traffic

Generated 2026-10-17 from the files on disk by `python\depth_appendix.py`. Inventory columns are read from the files; meanings are copied from the paper's own documentation or the fixed glossary, otherwise marked 'meaning not documented'. Large raw dumps (raw API responses, cached downloads, PDFs, virtual environments) are summarised, not listed.

## Documentation that already exists in the folder (authoritative for the paper's own data)
- `code\README.md`

## Bibliometrics layer (made by the literature-mapping pipeline)

| Path | What it is |
|---|---|
| `bibliometrics\data\clean\master.csv` | one row per corpus record after screening and hand-screening (the main table) |
| `bibliometrics\data\clean\bibliometrix_input.csv / bibliometrix_M.rds` | the same records in bibliometrix's field-tag format (AU, TI, SO, PY, TC, DE, ID, CR, C1 ...) |
| `bibliometrics\data\clean\citation_edges.csv` | direct-citation links between corpus records (citing, cited) |
| `bibliometrics\data\clean\cited_references.csv` | the references cited most often by the corpus, resolved to metadata |
| `bibliometrics\data\clean\corpus_final.jsonl.gz / corpus_stage1.jsonl.gz` | full OpenAlex JSON records after / before the last screening pass |
| `bibliometrics\data\clean\screening_log_*.csv` | every screening decision with its reason |
| `bibliometrics\data\clean\unresolved_candidates.csv` | records found by a search but not matched in OpenAlex (kept for audit) |
| `bibliometrics\data\raw\` | raw API responses per query (crossref, s2, eric, arxiv) + all_hits.csv + query_log.csv; OpenAlex records as .jsonl.gz |
| `bibliometrics\tables\` | numbers behind every figure (R_*.csv from bibliometrix, py_*.csv from Python), PRISMA counts, logs |

Access/pull date for all bibliometrics data: see `bibliometrics\data\clean\prisma_search.json` (field `date`); sources: Crossref REST API, Semantic Scholar API, ERIC API, arXiv API, OpenAlex API, OpenCitations API (all free, no key, no personal identifier sent). Known problems: OpenAlex affiliation/abstract/reference gaps for Indian journals, books and law; duplicate preprint/published versions merged by title only; keywords are machine-assigned.

## File inventory

### `bibliometrics\config.json`
- size 26 KB; modified 2026-10-17

### `bibliometrics\data\api_log.json`
- size 248 KB; modified 2026-10-17

### `bibliometrics\data\clean\bibliometrix_M.rds`
- size 638 KB; modified 2026-10-17

### `bibliometrics\data\clean\bibliometrix_input.csv`
- size 2189 KB; modified 2026-10-17; rows 631
- columns / contents:
  - `AU` (str; e.g. 'LIM S'): bibliometrix: authors (short form)
  - `AF` (str; e.g. 'SOOK LIM'): bibliometrix: authors (full names)
  - `TI` (str; e.g. 'HOW AND WHY DO COLLEGE STUDENTS USE WIKI'): bibliometrix: title (upper case)
  - `SO` (str; e.g. 'JOURNAL OF THE AMERICAN SOCIETY FOR INFO'): bibliometrix: source (journal) name
  - `JI` (str; e.g. 'JOURNAL OF THE AMERICAN SOCIETY FOR INFO')  - *meaning not documented here (see the files above / the code that writes it)*
  - `J9` (str; e.g. 'JOURNAL OF THE AMERICAN SOCIETY FOR INFO'): bibliometrix: abbreviated journal
  - `DT` (str; e.g. 'ARTICLE'): bibliometrix: document type
  - `DE` (str; e.g. 'WIKIPEDIA;UNIVERSITY STUDENTS;INFORMATIO'): bibliometrix: author/OpenAlex keywords
  - `ID` (str; e.g. 'PERCEPTION;SAMPLE (MATERIAL);QUALITY (PH'): bibliometrix: keywords-plus (here OpenAlex concepts/topics)
  - `AB` (str; e.g. 'ABSTRACT THE PURPOSES OF THIS STUDY WERE'): bibliometrix: abstract
  - `C1` (str; e.g. 'ST. CATHERINE UNIVERSITY, USA'): bibliometrix: author affiliations
  - `RP` (str; e.g. 'ST. CATHERINE UNIVERSITY, USA'): bibliometrix: reprint (corresponding-author) address
  - `CR` (str; e.g. 'WANG G, 2006, JOURNAL OF PROTEOME RESEAR'): bibliometrix: cited references, one label per reference, separated by ;
  - `TC` (int64; e.g. '178'): bibliometrix: total citations (OpenAlex)
  - `PY` (int64; e.g. '2009'): bibliometrix: publication year
  - `DI` (str; e.g. '10.1002/ASI.21142'): bibliometrix: DOI
  - `LA` (str; e.g. 'ENGLISH'): bibliometrix: language
  - `UT` (str; e.g. 'W4235537536')  - *meaning not documented here (see the files above / the code that writes it)*
  - `DB` (str; e.g. 'ISI'): bibliometrix: database label
  - `SR` (str; e.g. 'LIM S, 2009, JOURNAL OF THE AMERICAN SOC'): bibliometrix: short reference key
  - `SR_FULL` (str; e.g. 'LIM S, 2009, JOURNAL OF THE AMERICAN SOC')  - *meaning not documented here (see the files above / the code that writes it)*
  - `AU_UN` (str; e.g. 'ST. CATHERINE UNIVERSITY')  - *meaning not documented here (see the files above / the code that writes it)*
  - `AU1_UN` (str; e.g. 'ST. CATHERINE UNIVERSITY')  - *meaning not documented here (see the files above / the code that writes it)*
  - `AU_CO` (str; e.g. 'USA')  - *meaning not documented here (see the files above / the code that writes it)*
  - `AU1_CO` (str; e.g. 'USA')  - *meaning not documented here (see the files above / the code that writes it)*
  - `SUBLIT` (str; e.g. 'C_student_information_seeking')  - *meaning not documented here (see the files above / the code that writes it)*
  - `LCS` (int64; e.g. '33'): bibliometrix: local citation score (citations from inside the corpus)
  - `NR` (int64; e.g. '37')  - *meaning not documented here (see the files above / the code that writes it)*
  - `id_oa` (str; e.g. 'W4235537536')  - *meaning not documented here (see the files above / the code that writes it)*

### `bibliometrics\data\clean\citation_edges.csv`
- size 18 KB; modified 2026-10-17; rows 747
- columns / contents:
  - `citing` (str; e.g. 'W4235537536'): OpenAlex id of the citing record (inside the corpus)
  - `cited` (str; e.g. 'W109422130'): OpenAlex id of the cited record (in or outside the corpus)

### `bibliometrics\data\clean\cited_references.csv`
- size 1017 KB; modified 2026-10-17; rows 3978
- columns / contents:
  - `oa_id` (str; e.g. 'W1972644898'): OpenAlex work id (W...)
  - `local_citations` (int64; e.g. '40'): citations received from other records inside this corpus
  - `in_corpus` (int64; e.g. '0'): 1 if the cited work is itself a corpus record
  - `first_author` (str; e.g. 'Jim Giles'): first author's name
  - `year` (str; e.g. '2005.0'): publication year
  - `title` (str; e.g. 'Internet encyclopaedias go head to head'): work title (OpenAlex)
  - `source` (str; e.g. 'Nature'): journal / repository name
  - `doi` (str; e.g. '10.1038/438900a'): DOI, lower-case, no URL prefix
  - `global_citations` (int64; e.g. '1978'): OpenAlex citation count
  - `cr_label` (str; e.g. 'GILES J, 2005, NATURE, V438, P900, DOI 1'): bibliometrix-style cited-reference label

### `bibliometrics\data\clean\corpus_final.jsonl.gz`
- size 2060 KB; modified 2026-10-17

### `bibliometrics\data\clean\corpus_stage1.jsonl.gz`
- size 1933 KB; modified 2026-10-17

### `bibliometrics\data\clean\evidence_candidates.json`
- size 134 KB; modified 2026-10-17

### `bibliometrics\data\clean\evidence_notes.json`
- size 38 KB; modified 2026-10-17

### `bibliometrics\data\clean\handscreen_exclusions.json`
- size 14 KB; modified 2026-10-17

### `bibliometrics\data\clean\handscreen_titles.tsv`
- size 137 KB; modified 2026-10-17; rows 760
- columns / contents:
  - `oa_id` (str; e.g. 'W4390908403'): OpenAlex work id (W...)
  - `year` (int64; e.g. '2024'): publication year
  - `cites` (int64; e.g. '91')  - *meaning not documented here (see the files above / the code that writes it)*
  - `origin` (str; e.g. 'search'): search | snowball-backward | snowball-forward | seed
  - `sublit` (str; e.g. 'A_genai_knowledge_platforms'): primary sub-literature assigned by the screening rules
  - `source` (str; e.g. 'F1000Research'): journal / repository name
  - `title` (str; e.g. 'Academic publisher guidelines on AI usag'): work title (OpenAlex)

### `bibliometrics\data\clean\master.csv`
- size 1643 KB; modified 2026-10-17; rows 631
- columns / contents:
  - `oa_id` (str; e.g. 'W4235537536'): OpenAlex work id (W...)
  - `doi` (str; e.g. '10.1002/asi.21142'): DOI, lower-case, no URL prefix
  - `title` (str; e.g. 'How and why do college students use Wiki'): work title (OpenAlex)
  - `year` (int64; e.g. '2009'): publication year
  - `date` (str; e.g. '2009-07-06'): publication date
  - `type` (str; e.g. 'article'): OpenAlex work type (article, review, preprint, book-chapter ...)
  - `language` (str; e.g. 'en'): ISO language code
  - `source` (str; e.g. 'Journal of the American Society for Info'): journal / repository name
  - `source_type` (str; e.g. 'journal'): journal, repository, book series ...
  - `publisher` (str; e.g. 'Wiley')  - *meaning not documented here (see the files above / the code that writes it)*
  - `issn` (str; e.g. '1532-2882')  - *meaning not documented here (see the files above / the code that writes it)*
  - `authors` (str; e.g. 'Sook Lim'): author display names, '; '-separated
  - `n_authors` (int64; e.g. '1'): number of authors
  - `first_author` (str; e.g. 'Sook Lim'): first author's name
  - `institutions` (str; e.g. 'ST. CATHERINE UNIVERSITY'): author institutions, '; '-separated
  - `countries` (str; e.g. 'US'): ISO-2 country codes of author affiliations, '; '-separated (empty when OpenAlex has no affiliation data)
  - `first_author_country` (str; e.g. 'US')  - *meaning not documented here (see the files above / the code that writes it)*
  - `corresponding_country` (str; e.g. 'US')  - *meaning not documented here (see the files above / the code that writes it)*
  - `international_collab` (int64; e.g. '0')  - *meaning not documented here (see the files above / the code that writes it)*
  - `cited_by_count` (int64; e.g. '178'): citations counted by OpenAlex at pull date
  - `fwci` (str; e.g. '41.0824'): field-weighted citation impact (OpenAlex; 1 = world average for field/year/type)
  - `local_citations` (int64; e.g. '33'): citations received from other records inside this corpus
  - `n_refs` (int64; e.g. '37'): number of references in OpenAlex
  - `is_oa` (bool; e.g. 'False'): open-access flag (OpenAlex)
  - `oa_status` (str; e.g. 'closed'): gold/green/hybrid/bronze/closed
  - `oa_url` (str; e.g. ''): best open-access landing page
  - `best_pdf_url` (str; e.g. ''): direct PDF link, if known
  - `best_oa_landing` (str; e.g. '')  - *meaning not documented here (see the files above / the code that writes it)*
  - `all_pdf_urls` (str; e.g. '')  - *meaning not documented here (see the files above / the code that writes it)*
  - `sublit` (str; e.g. 'C_student_information_seeking'): primary sub-literature assigned by the screening rules
  - `sublits_all` (str; e.g. 'C_student_information_seeking'): every sub-literature whose rule matched, '; '-separated
  - `origin` (str; e.g. 'search'): search | snowball-backward | snowball-forward | seed
  - `found_in` (str; e.g. 's2'): databases that returned the record (crossref, s2, eric, arxiv, seed)
  - `relevance` (float64; e.g. '9.0'): rule-based topical score (core-term hits weighted); higher = closer to the paper's topic
  - `primary_topic` (str; e.g. 'Wikis in Education and Collaboration')  - *meaning not documented here (see the files above / the code that writes it)*
  - `subfield` (str; e.g. 'Communication')  - *meaning not documented here (see the files above / the code that writes it)*
  - `field` (str; e.g. 'Social Sciences')  - *meaning not documented here (see the files above / the code that writes it)*
  - `domain` (str; e.g. 'Social Sciences')  - *meaning not documented here (see the files above / the code that writes it)*
  - `keywords` (str; e.g. 'Wikipedia; university students; informat'): OpenAlex machine-assigned keywords
  - `topics` (str; e.g. 'Wikis in Education and Collaboration; Li'): OpenAlex topics
  - `concepts` (str; e.g. 'Perception; Sample (material); Quality ('): OpenAlex concepts
  - `abstract` (str; e.g. 'Abstract The purposes of this study were'): abstract text (rebuilt from OpenAlex inverted index or taken from S2/ERIC/Crossref)
  - `has_abstract` (int64; e.g. '1'): 1 if an abstract is present
  - `is_retracted` (bool; e.g. 'False'): OpenAlex retraction flag
  - `sr` (str; e.g. 'LIM S, 2009, JOURNAL OF THE AMERICAN SOC'): short reference key used by bibliometrix
  - `crossref_cited_by` (str; e.g. '144.0'): Crossref is-referenced-by count
  - `crossref_n_refs` (str; e.g. '43.0')  - *meaning not documented here (see the files above / the code that writes it)*
  - `s2_citation_count` (str; e.g. '211.0'): Semantic Scholar citation count
  - `s2_pdf_url` (str; e.g. '')  - *meaning not documented here (see the files above / the code that writes it)*

### `bibliometrics\data\clean\master.rds`
- size 484 KB; modified 2026-10-17

### `bibliometrics\data\clean\prisma_search.json`
- size 1 KB; modified 2026-10-17

### `bibliometrics\data\clean\prisma_snowball.json`
- size 3 KB; modified 2026-10-17

### `bibliometrics\data\clean\refs_stats.json`
- size 0 KB; modified 2026-10-17

### `bibliometrics\data\clean\screening_log_search.csv`
- size 258 KB; modified 2026-10-17; rows 1276
- columns / contents:
  - `key` (str; e.g. 'doi:10.1001/jamanetworkopen.2025.42281')  - *meaning not documented here (see the files above / the code that writes it)*
  - `title` (str; e.g. 'Use of Generative AI for Mental Health A'): work title (OpenAlex)
  - `dbs` (str; e.g. 's2')  - *meaning not documented here (see the files above / the code that writes it)*
  - `sublits_queried` (str; e.g. 'C_student_information_seeking')  - *meaning not documented here (see the files above / the code that writes it)*
  - `oa_id` (str; e.g. 'W4416008628'): OpenAlex work id (W...)
  - `decision` (str; e.g. 'included')  - *meaning not documented here (see the files above / the code that writes it)*
  - `reason` (str; e.g. '')  - *meaning not documented here (see the files above / the code that writes it)*
  - `sublit` (str; e.g. 'C_student_information_seeking'): primary sub-literature assigned by the screening rules

### `bibliometrics\data\clean\screening_log_snowball.csv`
- size 322 KB; modified 2026-10-17; rows 2327
- columns / contents:
  - `key` (str; e.g. 'W16674111')  - *meaning not documented here (see the files above / the code that writes it)*
  - `kind` (str; e.g. 'back')  - *meaning not documented here (see the files above / the code that writes it)*
  - `oa_id` (str; e.g. 'W16674111'): OpenAlex work id (W...)
  - `title` (str; e.g. 'Label-Free Protein Quantification Using '): work title (OpenAlex)
  - `decision` (str; e.g. 'excluded')  - *meaning not documented here (see the files above / the code that writes it)*
  - `reason` (str; e.g. 'offtopic_fails_inclusion_rule')  - *meaning not documented here (see the files above / the code that writes it)*
  - `sublit` (str; e.g. ''): primary sub-literature assigned by the screening rules

### `bibliometrics\data\clean\snowball_central_papers.csv`
- size 3 KB; modified 2026-10-17; rows 28
- columns / contents:
  - `oa_id` (str; e.g. 'W4235537536'): OpenAlex work id (W...)
  - `title` (str; e.g. 'How and why do college students use Wiki'): work title (OpenAlex)
  - `year` (int64; e.g. '2009'): publication year
  - `local_cites` (int64; e.g. '28')  - *meaning not documented here (see the files above / the code that writes it)*
  - `cited_by` (int64; e.g. '178')  - *meaning not documented here (see the files above / the code that writes it)*
  - `relevance` (float64; e.g. '9.0'): rule-based topical score (core-term hits weighted); higher = closer to the paper's topic

### `bibliometrics\data\clean\unresolved_candidates.csv`
- size 12 KB; modified 2026-10-17; rows 56
- columns / contents:
  - `key` (str; e.g. 'doi:10.14429/djlit.29.4.256')  - *meaning not documented here (see the files above / the code that writes it)*
  - `title` (str; e.g. 'Library Information-Seeking Behaviour am'): work title (OpenAlex)
  - `first_author` (str; e.g. 'Sookhtanlo'): first author's name
  - `year` (float64; e.g. '2009.0'): publication year
  - `dbs` (str; e.g. 's2')  - *meaning not documented here (see the files above / the code that writes it)*
  - `eric` (str; e.g. '')  - *meaning not documented here (see the files above / the code that writes it)*
  - `sublits_q` (str; e.g. 'C_student_information_seeking')  - *meaning not documented here (see the files above / the code that writes it)*

### `bibliometrics\evidence-table.csv`
- size 46 KB; modified 2026-10-17; rows 58
- columns / contents:
  - `rank` (int64; e.g. '1')  - *meaning not documented here (see the files above / the code that writes it)*
  - `citation` (str; e.g. 'Neal Reeves, Wenjie Yin, Elena Paslaru B')  - *meaning not documented here (see the files above / the code that writes it)*
  - `year` (int64; e.g. '2025'): publication year
  - `doi_or_link` (str; e.g. 'https://doi.org/10.1177/2633913725137259')  - *meaning not documented here (see the files above / the code that writes it)*
  - `open_access_link` (str; e.g. 'https://doi.org/10.1177/2633913725137259')  - *meaning not documented here (see the files above / the code that writes it)*
  - `oa_status` (str; e.g. 'diamond'): gold/green/hybrid/bronze/closed
  - `pdf_in_folder` (str; e.g. 'Reeves_2025_Exploring-the-impact-of-Chat')  - *meaning not documented here (see the files above / the code that writes it)*
  - `sub_literature` (str; e.g. 'A_genai_knowledge_platforms')  - *meaning not documented here (see the files above / the code that writes it)*
  - `study_type` (str; e.g. 'Observational / econometric analysis')  - *meaning not documented here (see the files above / the code that writes it)*
  - `country_or_setting` (str; e.g. 'United Kingdom, Germany')  - *meaning not documented here (see the files above / the code that writes it)*
  - `data` (str; e.g. 'not stated in abstract')  - *meaning not documented here (see the files above / the code that writes it)*
  - `method` (str; e.g. 'regression analysis')  - *meaning not documented here (see the files above / the code that writes it)*
  - `main_finding_from_abstract` (str; e.g. 'Conclusions: Our results suggest that wh')  - *meaning not documented here (see the files above / the code that writes it)*
  - `read_status` (str; e.g. 'abstract read')  - *meaning not documented here (see the files above / the code that writes it)*
  - `relation_to_seans_paper` (str; e.g. 'Evidence on whether generative AI and AI')  - *meaning not documented here (see the files above / the code that writes it)*
  - `local_citations` (int64; e.g. '3'): citations received from other records inside this corpus
  - `global_citations_openalex` (int64; e.g. '5')  - *meaning not documented here (see the files above / the code that writes it)*
  - `openalex_id` (str; e.g. 'W4414535549')  - *meaning not documented here (see the files above / the code that writes it)*

### `data\control_articles.csv`
- size 302 KB; modified 2026-10-13; rows 1290
- columns / contents:
  - `control_set` (str; e.g. 'A_same_area')  - *meaning not documented here (see the files above / the code that writes it)*
  - `matched_to` (str; e.g. 'Malaria')  - *meaning not documented here (see the files above / the code that writes it)*
  - `area` (str; e.g. 'SCI')  - *meaning not documented here (see the files above / the code that writes it)*
  - `subject` (str; e.g. 'XII-BIO')  - *meaning not documented here (see the files above / the code that writes it)*
  - `en_title` (str; e.g. 'Mercury (planet)')  - *meaning not documented here (see the files above / the code that writes it)*
  - `qid` (str; e.g. 'Q308')  - *meaning not documented here (see the files above / the code that writes it)*
  - `en_pageid` (int64; e.g. '19694')  - *meaning not documented here (see the files above / the code that writes it)*
  - `pre_views` (float64; e.g. '4083.14')  - *meaning not documented here (see the files above / the code that writes it)*
  - `matched_pre_views` (float64; e.g. '4097.82')  - *meaning not documented here (see the files above / the code that writes it)*
  - `log_gap` (float64; e.g. '-0.004')  - *meaning not documented here (see the files above / the code that writes it)*
  - `hi_title` (str; e.g. 'बुध (ग्रह)')  - *meaning not documented here (see the files above / the code that writes it)*
  - `kn_title` (str; e.g. 'ಬುಧ')  - *meaning not documented here (see the files above / the code that writes it)*
  - `rule` (str; e.g. '1:1 nearest neighbour on log mean daily ')  - *meaning not documented here (see the files above / the code that writes it)*

### `data\control_candidates.csv`
- size 112 KB; modified 2026-10-13; rows 2246
- columns / contents:
  - `area` (str; e.g. 'SCI')  - *meaning not documented here (see the files above / the code that writes it)*
  - `en_title` (str; e.g. 'Occupational safety and health')  - *meaning not documented here (see the files above / the code that writes it)*
  - `qid` (str; e.g. 'Q629029')  - *meaning not documented here (see the files above / the code that writes it)*
  - `en_pageid` (int64; e.g. '35319154')  - *meaning not documented here (see the files above / the code that writes it)*
  - `pre_views` (float64; e.g. '1272.5277207392196')  - *meaning not documented here (see the files above / the code that writes it)*

### `data\datesheets\2017_X.txt`
- size 3 KB; modified 2026-10-13
- columns / contents:
  - (could not read: ParserError)

### `data\datesheets\2017_XII.txt`
- size 8 KB; modified 2026-10-13
- columns / contents:
  - (could not read: ParserError)

### `data\datesheets\2017_corrigendum.txt`
- size 1 KB; modified 2026-10-13; rows 27
- columns / contents:
  - `CBSE/AS/COORD/2017                     Date: 24.01.2017 ` (str; e.g. 'CORRIGENDUM ')  - *meaning not documented here (see the files above / the code that writes it)*

### `data\datesheets\2018_XII_revision.txt`
- size 0 KB; modified 2026-10-13
- columns / contents:
  - (could not read: EmptyDataError)

### `data\datesheets\2018_X_C.txt`
- size 3 KB; modified 2026-10-13
- columns / contents:
  - (could not read: ParserError)

### `data\datesheets\2018_new_exam_date.txt`
- size 0 KB; modified 2026-10-13
- columns / contents:
  - (could not read: EmptyDataError)

### `data\datesheets\2020_X.txt`
- size 0 KB; modified 2026-10-13
- columns / contents:
  - (could not read: EmptyDataError)

### `data\datesheets\2020_XII.txt`
- size 0 KB; modified 2026-10-13
- columns / contents:
  - (could not read: EmptyDataError)

### `data\datesheets\2021_XII_planned.txt`
- size 7 KB; modified 2026-10-13
- columns / contents:
  - (could not read: ParserError)

### `data\datesheets\2021_X_planned.txt`
- size 4 KB; modified 2026-10-13
- columns / contents:
  - (could not read: ParserError)

### `data\datesheets\2022_term1_X.txt`
- size 0 KB; modified 2026-10-13
- columns / contents:
  - (could not read: EmptyDataError)

### `data\datesheets\2022_term1_XII.txt`
- size 0 KB; modified 2026-10-13
- columns / contents:
  - (could not read: EmptyDataError)

### `data\datesheets\2023.txt`
- size 0 KB; modified 2026-10-13
- columns / contents:
  - (could not read: EmptyDataError)

### `data\datesheets\2024_XII_rev.txt`
- size 0 KB; modified 2026-10-13
- columns / contents:
  - (could not read: EmptyDataError)

### `data\datesheets\2024_X_rev.txt`
- size 0 KB; modified 2026-10-13
- columns / contents:
  - (could not read: EmptyDataError)

### `data\datesheets\2025.txt`
- size 0 KB; modified 2026-10-13
- columns / contents:
  - (could not read: EmptyDataError)

### `data\datesheets\2026_XII_rev.txt`
- size 0 KB; modified 2026-10-13
- columns / contents:
  - (could not read: EmptyDataError)

### `data\datesheets\2026_X_rev.txt`
- size 0 KB; modified 2026-10-13
- columns / contents:
  - (could not read: EmptyDataError)

### `data\exam_dates.csv`
- size 10 KB; modified 2026-10-13; rows 87
- columns / contents:
  - `exam_year` (int64; e.g. '2016')  - *meaning not documented here (see the files above / the code that writes it)*
  - `class` (str; e.g. 'X')  - *meaning not documented here (see the files above / the code that writes it)*
  - `event` (str; e.g. 'first_exam')  - *meaning not documented here (see the files above / the code that writes it)*
  - `date` (str; e.g. '2016-03-01'): publication date
  - `verification` (str; e.g. 'UNVERIFIED (from memory; no primary docu')  - *meaning not documented here (see the files above / the code that writes it)*
  - `source` (str; e.g. 'needs a primary source before publicatio'): journal / repository name

### `data\igcse\overlap.csv`
- size 49 KB; modified 2026-10-17; rows 868
- columns / contents:
  - `en_title` (str; e.g. 'Chemical equation')  - *meaning not documented here (see the files above / the code that writes it)*
  - `subject` (str; e.g. 'X-SCI')  - *meaning not documented here (see the files above / the code that writes it)*
  - `kw` (str; e.g. 'chemical equation')  - *meaning not documented here (see the files above / the code that writes it)*
  - `igcse_physics` (bool; e.g. 'False')  - *meaning not documented here (see the files above / the code that writes it)*
  - `igcse_biology` (bool; e.g. 'True')  - *meaning not documented here (see the files above / the code that writes it)*
  - `igcse_chemistry` (bool; e.g. 'False')  - *meaning not documented here (see the files above / the code that writes it)*

### `data\panel_full_en.npz`
- size 12091 KB; modified 2026-10-17
- columns / contents:
  - all_access: array shape (2158, 4110) dtype float32  - *meaning not documented here (see the files above / the code that writes it)*
  - desktop: array shape (2158, 4110) dtype float32  - *meaning not documented here (see the files above / the code that writes it)*

### `data\panel_full_en_index.csv`
- size 168 KB; modified 2026-10-17; rows 2158
- columns / contents:
  - `article` (str; e.g. 'Chemical equation')  - *meaning not documented here (see the files above / the code that writes it)*
  - `group` (str; e.g. 'syllabus')  - *meaning not documented here (see the files above / the code that writes it)*
  - `en_title` (str; e.g. 'Chemical equation')  - *meaning not documented here (see the files above / the code that writes it)*
  - `matched_to` (str; e.g. 'Chemical equation')  - *meaning not documented here (see the files above / the code that writes it)*
  - `area` (str; e.g. 'SCI')  - *meaning not documented here (see the files above / the code that writes it)*
  - `fetched` (bool; e.g. 'True')  - *meaning not documented here (see the files above / the code that writes it)*
  - `n_redirect_titles` (int64; e.g. '0')  - *meaning not documented here (see the files above / the code that writes it)*
  - `total_views` (float64; e.g. '1657220.0')  - *meaning not documented here (see the files above / the code that writes it)*
  - `share_on_current_title` (str; e.g. '1.0')  - *meaning not documented here (see the files above / the code that writes it)*

### `data\panel_full_hi.npz`
- size 741 KB; modified 2026-10-17
- columns / contents:
  - all_access: array shape (1364, 4110) dtype float32  - *meaning not documented here (see the files above / the code that writes it)*
  - desktop: array shape (1364, 4110) dtype float32  - *meaning not documented here (see the files above / the code that writes it)*

### `data\panel_full_hi_index.csv`
- size 126 KB; modified 2026-10-17; rows 1364
- columns / contents:
  - `article` (str; e.g. 'रासायनिक समीकरण')  - *meaning not documented here (see the files above / the code that writes it)*
  - `group` (str; e.g. 'syllabus')  - *meaning not documented here (see the files above / the code that writes it)*
  - `en_title` (str; e.g. 'Chemical equation')  - *meaning not documented here (see the files above / the code that writes it)*
  - `matched_to` (str; e.g. 'Chemical equation')  - *meaning not documented here (see the files above / the code that writes it)*
  - `area` (str; e.g. 'SCI')  - *meaning not documented here (see the files above / the code that writes it)*
  - `fetched` (bool; e.g. 'True')  - *meaning not documented here (see the files above / the code that writes it)*
  - `n_redirect_titles` (int64; e.g. '0')  - *meaning not documented here (see the files above / the code that writes it)*
  - `total_views` (float64; e.g. '474432.0')  - *meaning not documented here (see the files above / the code that writes it)*
  - `share_on_current_title` (str; e.g. '1.0')  - *meaning not documented here (see the files above / the code that writes it)*

### `data\panel_full_kn.npz`
- size 134 KB; modified 2026-10-17
- columns / contents:
  - all_access: array shape (671, 4110) dtype float32  - *meaning not documented here (see the files above / the code that writes it)*
  - desktop: array shape (671, 4110) dtype float32  - *meaning not documented here (see the files above / the code that writes it)*

### `data\panel_full_kn_index.csv`
- size 59 KB; modified 2026-10-17; rows 671
- columns / contents:
  - `article` (str; e.g. 'ರಾಸಾಯನಿಕ ಕ್ರಿಯೆ')  - *meaning not documented here (see the files above / the code that writes it)*
  - `group` (str; e.g. 'syllabus')  - *meaning not documented here (see the files above / the code that writes it)*
  - `en_title` (str; e.g. 'Chemical reaction')  - *meaning not documented here (see the files above / the code that writes it)*
  - `matched_to` (str; e.g. 'Chemical reaction')  - *meaning not documented here (see the files above / the code that writes it)*
  - `area` (str; e.g. 'SCI')  - *meaning not documented here (see the files above / the code that writes it)*
  - `fetched` (bool; e.g. 'False')  - *meaning not documented here (see the files above / the code that writes it)*
  - `n_redirect_titles` (int64; e.g. '0')  - *meaning not documented here (see the files above / the code that writes it)*
  - `total_views` (float64; e.g. '0.0')  - *meaning not documented here (see the files above / the code that writes it)*
  - `share_on_current_title` (str; e.g. '')  - *meaning not documented here (see the files above / the code that writes it)*

### `data\panel_pilot_en.npz`
- size 2616 KB; modified 2026-10-13
- columns / contents:
  - all_access: array shape (148, 4110) dtype float32  - *meaning not documented here (see the files above / the code that writes it)*
  - desktop: array shape (148, 4110) dtype float32  - *meaning not documented here (see the files above / the code that writes it)*
  - mobile_app: array shape (148, 4110) dtype float32  - *meaning not documented here (see the files above / the code that writes it)*

### `data\panel_pilot_en_index.csv`
- size 12 KB; modified 2026-10-13; rows 148
- columns / contents:
  - `article` (str; e.g. 'Chemical equation')  - *meaning not documented here (see the files above / the code that writes it)*
  - `group` (str; e.g. 'syllabus')  - *meaning not documented here (see the files above / the code that writes it)*
  - `en_title` (str; e.g. 'Chemical equation')  - *meaning not documented here (see the files above / the code that writes it)*
  - `matched_to` (str; e.g. 'Chemical equation')  - *meaning not documented here (see the files above / the code that writes it)*
  - `area` (str; e.g. 'SCI')  - *meaning not documented here (see the files above / the code that writes it)*
  - `fetched` (bool; e.g. 'True')  - *meaning not documented here (see the files above / the code that writes it)*
  - `n_redirect_titles` (int64; e.g. '0')  - *meaning not documented here (see the files above / the code that writes it)*
  - `total_views` (float64; e.g. '1657220.0')  - *meaning not documented here (see the files above / the code that writes it)*
  - `share_on_current_title` (float64; e.g. '1.0')  - *meaning not documented here (see the files above / the code that writes it)*

### `data\panel_pilot_hi.npz`
- size 509 KB; modified 2026-10-13
- columns / contents:
  - all_access: array shape (70, 4110) dtype float32  - *meaning not documented here (see the files above / the code that writes it)*
  - desktop: array shape (70, 4110) dtype float32  - *meaning not documented here (see the files above / the code that writes it)*
  - mobile_app: array shape (70, 4110) dtype float32  - *meaning not documented here (see the files above / the code that writes it)*

### `data\panel_pilot_hi_index.csv`
- size 8 KB; modified 2026-10-13; rows 70
- columns / contents:
  - `article` (str; e.g. 'रासायनिक समीकरण')  - *meaning not documented here (see the files above / the code that writes it)*
  - `group` (str; e.g. 'syllabus')  - *meaning not documented here (see the files above / the code that writes it)*
  - `en_title` (str; e.g. 'Chemical equation')  - *meaning not documented here (see the files above / the code that writes it)*
  - `matched_to` (str; e.g. 'Chemical equation')  - *meaning not documented here (see the files above / the code that writes it)*
  - `area` (str; e.g. 'SCI')  - *meaning not documented here (see the files above / the code that writes it)*
  - `fetched` (bool; e.g. 'True')  - *meaning not documented here (see the files above / the code that writes it)*
  - `n_redirect_titles` (int64; e.g. '0')  - *meaning not documented here (see the files above / the code that writes it)*
  - `total_views` (float64; e.g. '474432.0')  - *meaning not documented here (see the files above / the code that writes it)*
  - `share_on_current_title` (float64; e.g. '1.0')  - *meaning not documented here (see the files above / the code that writes it)*

### `data\panel_pilot_kn.npz`
- size 119 KB; modified 2026-10-13
- columns / contents:
  - all_access: array shape (31, 4110) dtype float32  - *meaning not documented here (see the files above / the code that writes it)*
  - desktop: array shape (31, 4110) dtype float32  - *meaning not documented here (see the files above / the code that writes it)*
  - mobile_app: array shape (31, 4110) dtype float32  - *meaning not documented here (see the files above / the code that writes it)*

### `data\panel_pilot_kn_index.csv`
- size 3 KB; modified 2026-10-13; rows 31
- columns / contents:
  - `article` (str; e.g. 'ಸೋಡಿಯಂ ಬೈ ಕಾರ್ಬೋನೇಟ್')  - *meaning not documented here (see the files above / the code that writes it)*
  - `group` (str; e.g. 'syllabus')  - *meaning not documented here (see the files above / the code that writes it)*
  - `en_title` (str; e.g. 'Sodium bicarbonate')  - *meaning not documented here (see the files above / the code that writes it)*
  - `matched_to` (str; e.g. 'Sodium bicarbonate')  - *meaning not documented here (see the files above / the code that writes it)*
  - `area` (str; e.g. 'SCI')  - *meaning not documented here (see the files above / the code that writes it)*
  - `fetched` (bool; e.g. 'True')  - *meaning not documented here (see the files above / the code that writes it)*
  - `n_redirect_titles` (int64; e.g. '1')  - *meaning not documented here (see the files above / the code that writes it)*
  - `total_views` (float64; e.g. '17138.0')  - *meaning not documented here (see the files above / the code that writes it)*
  - `share_on_current_title` (float64; e.g. '0.70037343914109')  - *meaning not documented here (see the files above / the code that writes it)*

### `data\syllabus\Biology_Sr.Sec_2020-21.txt`
- size 27 KB; modified 2026-10-13
- columns / contents:
  - (could not read: ParserError)

### `data\syllabus\Biology_SrSec_2024-25.txt`
- size 23 KB; modified 2026-10-13
- columns / contents:
  - (could not read: ParserError)

### `data\syllabus\Chemistry_Sr.Sec_2020-21.txt`
- size 36 KB; modified 2026-10-13
- columns / contents:
  - (could not read: ParserError)

### `data\syllabus\Chemistry_SrSec_2024-25.txt`
- size 29 KB; modified 2026-10-13
- columns / contents:
  - (could not read: ParserError)

### `data\syllabus\Mathematics_Sec_2020-21.txt`
- size 24 KB; modified 2026-10-13
- columns / contents:
  - (could not read: ParserError)

### `data\syllabus\Mathematics_Sr.Sec_2020-21.txt`
- size 22 KB; modified 2026-10-13
- columns / contents:
  - (could not read: ParserError)

### `data\syllabus\Maths_Sec_2024-25.txt`
- size 18 KB; modified 2026-10-13
- columns / contents:
  - (could not read: ParserError)

### `data\syllabus\Maths_SrSec_2024-25.txt`
- size 19 KB; modified 2026-10-13
- columns / contents:
  - (could not read: ParserError)

### `data\syllabus\Physics_Sr.Sec_2020-21.txt`
- size 37 KB; modified 2026-10-13
- columns / contents:
  - (could not read: ParserError)

### `data\syllabus\Physics_SrSec_2024-25.txt`
- size 37 KB; modified 2026-10-13
- columns / contents:
  - (could not read: ParserError)

### `data\syllabus\Science_Sec_2020-21.txt`
- size 22 KB; modified 2026-10-13
- columns / contents:
  - (could not read: ParserError)

### `data\syllabus\Science_Sec_2024-25.txt`
- size 18 KB; modified 2026-10-13
- columns / contents:
  - (could not read: ParserError)

### `data\syllabus\Social_Science_Sec_2020-21.txt`
- size 42 KB; modified 2026-10-13
- columns / contents:
  - (could not read: ParserError)

### `data\syllabus\Social_Science_Sec_2024-25.txt`
- size 111 KB; modified 2026-10-13
- columns / contents:
  - (could not read: ParserError)

### `data\syllabus_articles.csv`
- size 184 KB; modified 2026-10-13; rows 868
- columns / contents:
  - `subject` (str; e.g. 'X-SCI')  - *meaning not documented here (see the files above / the code that writes it)*
  - `area` (str; e.g. 'SCI')  - *meaning not documented here (see the files above / the code that writes it)*
  - `unit` (str; e.g. 'Chemical reactions')  - *meaning not documented here (see the files above / the code that writes it)*
  - `topic` (str; e.g. 'Chemical equation')  - *meaning not documented here (see the files above / the code that writes it)*
  - `en_title` (str; e.g. 'Chemical equation')  - *meaning not documented here (see the files above / the code that writes it)*
  - `qid` (str; e.g. 'Q182527')  - *meaning not documented here (see the files above / the code that writes it)*
  - `en_pageid` (int64; e.g. '199040')  - *meaning not documented here (see the files above / the code that writes it)*
  - `hi_title` (str; e.g. 'रासायनिक समीकरण')  - *meaning not documented here (see the files above / the code that writes it)*
  - `kn_title` (str; e.g. '')  - *meaning not documented here (see the files above / the code that writes it)*
  - `rule` (str; e.g. 'R1 exact title')  - *meaning not documented here (see the files above / the code that writes it)*
  - `ambiguous` (int64; e.g. '0')  - *meaning not documented here (see the files above / the code that writes it)*
  - `flags` (str; e.g. '')  - *meaning not documented here (see the files above / the code that writes it)*
  - `in_syllabus_2020_21` (int64; e.g. '1')  - *meaning not documented here (see the files above / the code that writes it)*
  - `in_syllabus_2024_25` (int64; e.g. '1')  - *meaning not documented here (see the files above / the code that writes it)*
  - `kw` (str; e.g. 'chemical\\ equation')  - *meaning not documented here (see the files above / the code that writes it)*
  - `en_title_mapped` (str; e.g. 'Chemical equation')  - *meaning not documented here (see the files above / the code that writes it)*
  - `en_redirected` (int64; e.g. '0')  - *meaning not documented here (see the files above / the code that writes it)*
  - `also_mapped_from` (str; e.g. '')  - *meaning not documented here (see the files above / the code that writes it)*
  - `pre_views` (float64; e.g. '576.713210130048')  - *meaning not documented here (see the files above / the code that writes it)*

### `data\titles_full.csv`
- size 410 KB; modified 2026-10-17; rows 4319
- columns / contents:
  - `lang` (str; e.g. 'en')  - *meaning not documented here (see the files above / the code that writes it)*
  - `article` (str; e.g. 'Chemical equation')  - *meaning not documented here (see the files above / the code that writes it)*
  - `title` (str; e.g. 'Chemical equation'): work title (OpenAlex)
  - `group` (str; e.g. 'syllabus')  - *meaning not documented here (see the files above / the code that writes it)*
  - `en_title` (str; e.g. 'Chemical equation')  - *meaning not documented here (see the files above / the code that writes it)*
  - `matched_to` (str; e.g. 'Chemical equation')  - *meaning not documented here (see the files above / the code that writes it)*
  - `area` (str; e.g. 'SCI')  - *meaning not documented here (see the files above / the code that writes it)*

### `data\titles_pilot.csv`
- size 39 KB; modified 2026-10-13; rows 374
- columns / contents:
  - `lang` (str; e.g. 'en')  - *meaning not documented here (see the files above / the code that writes it)*
  - `article` (str; e.g. 'Chemical equation')  - *meaning not documented here (see the files above / the code that writes it)*
  - `title` (str; e.g. 'Chemical equation'): work title (OpenAlex)
  - `group` (str; e.g. 'syllabus')  - *meaning not documented here (see the files above / the code that writes it)*
  - `en_title` (str; e.g. 'Chemical equation')  - *meaning not documented here (see the files above / the code that writes it)*
  - `matched_to` (str; e.g. 'Chemical equation')  - *meaning not documented here (see the files above / the code that writes it)*
  - `area` (str; e.g. 'SCI')  - *meaning not documented here (see the files above / the code that writes it)*

### `data\topic_mapping_all_rows.csv`
- size 171 KB; modified 2026-10-13; rows 871
- columns / contents:
  - `subject` (str; e.g. 'X-SCI')  - *meaning not documented here (see the files above / the code that writes it)*
  - `area` (str; e.g. 'SCI')  - *meaning not documented here (see the files above / the code that writes it)*
  - `unit` (str; e.g. 'Chemical reactions')  - *meaning not documented here (see the files above / the code that writes it)*
  - `topic` (str; e.g. 'Chemical equation')  - *meaning not documented here (see the files above / the code that writes it)*
  - `en_title` (str; e.g. 'Chemical equation')  - *meaning not documented here (see the files above / the code that writes it)*
  - `qid` (str; e.g. 'Q182527')  - *meaning not documented here (see the files above / the code that writes it)*
  - `en_pageid` (int64; e.g. '199040')  - *meaning not documented here (see the files above / the code that writes it)*
  - `hi_title` (str; e.g. 'रासायनिक समीकरण')  - *meaning not documented here (see the files above / the code that writes it)*
  - `kn_title` (str; e.g. '')  - *meaning not documented here (see the files above / the code that writes it)*
  - `rule` (str; e.g. 'R1 exact title')  - *meaning not documented here (see the files above / the code that writes it)*
  - `ambiguous` (int64; e.g. '0')  - *meaning not documented here (see the files above / the code that writes it)*
  - `flags` (str; e.g. '')  - *meaning not documented here (see the files above / the code that writes it)*
  - `in_syllabus_2020_21` (int64; e.g. '1')  - *meaning not documented here (see the files above / the code that writes it)*
  - `in_syllabus_2024_25` (int64; e.g. '1')  - *meaning not documented here (see the files above / the code that writes it)*
  - `kw` (str; e.g. 'chemical\\ equation')  - *meaning not documented here (see the files above / the code that writes it)*
  - `en_title_mapped` (str; e.g. 'Chemical equation')  - *meaning not documented here (see the files above / the code that writes it)*
  - `en_redirected` (int64; e.g. '0')  - *meaning not documented here (see the files above / the code that writes it)*
  - `en_missing` (int64; e.g. '0')  - *meaning not documented here (see the files above / the code that writes it)*
  - `en_disambig` (int64; e.g. '0')  - *meaning not documented here (see the files above / the code that writes it)*

### `data\topics_raw.txt`
- size 40 KB; modified 2026-10-13
- columns / contents:
  - (could not read: ParserError)

### `lit\1702.05379.txt`
- size 63 KB; modified 2026-10-13
- columns / contents:
  - (could not read: ParserError)

### `lit\1812.00474.txt`
- size 53 KB; modified 2026-10-13
- columns / contents:
  - (could not read: ParserError)

### `lit\2112.11848.txt`
- size 81 KB; modified 2026-10-13
- columns / contents:
  - (could not read: ParserError)

### `lit\2307.07367.txt`
- size 49 KB; modified 2026-10-13
- columns / contents:
  - (could not read: ParserError)

### `lit\2405.10205.txt`
- size 61 KB; modified 2026-10-13
- columns / contents:
  - (could not read: ParserError)

### `lit\2503.00757.txt`
- size 22 KB; modified 2026-10-13
- columns / contents:
  - (could not read: ParserError)

### `lit\2509.05879.txt`
- size 143 KB; modified 2026-10-13
- columns / contents:
  - (could not read: ParserError)

### `lit\2602.09550.txt`
- size 80 KB; modified 2026-10-13
- columns / contents:
  - (could not read: ParserError)

### `lit\2602.18455.txt`
- size 79 KB; modified 2026-10-13
- columns / contents:
  - (could not read: ParserError)

### `lit\2609.36069.txt`
- size 65 KB; modified 2026-10-13
- columns / contents:
  - (could not read: ParserError)

### `lit\2609.38563.txt`
- size 88 KB; modified 2026-10-13
- columns / contents:
  - (could not read: ParserError)

### `lit\aqs_spec.json`
- size 10 KB; modified 2026-10-13

### `lit\reeves.json`
- size 23 KB; modified 2026-10-13

### `lit\search1.txt`
- size 2 KB; modified 2026-10-13; rows 55
- columns / contents:
  - `retry HTTP Error 429: Too Many Requests` (str; e.g. 'retry HTTP Error 429: Too Many Requests')  - *meaning not documented here (see the files above / the code that writes it)*

### `lit\search_arxiv.txt`
- size 3 KB; modified 2026-10-13
- columns / contents:
  - (could not read: ParserError)

### `lit\search_arxiv2.txt`
- size 3 KB; modified 2026-10-13
- columns / contents:
  - (could not read: ParserError)

### `lit\search_arxiv3_followup.txt`
- size 0 KB; modified 2026-10-17
- columns / contents:
  - (could not read: ParserError)

### `lit\search_crossref.txt`
- size 13 KB; modified 2026-10-13
- columns / contents:
  - (could not read: ParserError)

### `lit\search_crossref3_followup.txt`
- size 3 KB; modified 2026-10-17
- columns / contents:
  - (could not read: ParserError)

### `results\R10_india_only.csv`
- size 1 KB; modified 2026-10-17; rows 6
- columns / contents:
  - `exam_year` (int64; e.g. '2018')  - *meaning not documented here (see the files above / the code that writes it)*
  - `regime` (str; e.g. 'historical (>450, Laplace)')  - *meaning not documented here (see the files above / the code that writes it)*
  - `days_exam` (int64; e.g. '6')  - *meaning not documented here (see the files above / the code that writes it)*
  - `days_base` (int64; e.g. '6')  - *meaning not documented here (see the files above / the code that writes it)*
  - `n_syllabus` (int64; e.g. '46')  - *meaning not documented here (see the files above / the code that writes it)*
  - `n_control` (int64; e.g. '17')  - *meaning not documented here (see the files above / the code that writes it)*
  - `uplift_syllabus` (float64; e.g. '0.0757')  - *meaning not documented here (see the files above / the code that writes it)*
  - `uplift_control` (float64; e.g. '-0.0028')  - *meaning not documented here (see the files above / the code that writes it)*
  - `gap` (str; e.g. '0.0786')  - *meaning not documented here (see the files above / the code that writes it)*
  - `ci_lo` (str; e.g. '-0.0798')  - *meaning not documented here (see the files above / the code that writes it)*
  - `ci_hi` (str; e.g. '0.2376')  - *meaning not documented here (see the files above / the code that writes it)*
  - `n_syllabus_any_exam_day` (int64; e.g. '153')  - *meaning not documented here (see the files above / the code that writes it)*

### `results\V2_peak_follows_exam_date_all.csv`
- size 1 KB; modified 2026-10-17; rows 4
- columns / contents:
  - `year` (int64; e.g. '2017'): publication year
  - `gap_own_window` (float64; e.g. '0.1143083031361282')  - *meaning not documented here (see the files above / the code that writes it)*
  - `own_lo` (float64; e.g. '0.0868503642222535')  - *meaning not documented here (see the files above / the code that writes it)*
  - `own_hi` (float64; e.g. '0.1405143988593289')  - *meaning not documented here (see the files above / the code that writes it)*
  - `gap_other_regime_window` (float64; e.g. '0.1099757900727269')  - *meaning not documented here (see the files above / the code that writes it)*
  - `other_lo` (float64; e.g. '0.0859489324539254')  - *meaning not documented here (see the files above / the code that writes it)*
  - `other_hi` (float64; e.g. '0.1383063149235117')  - *meaning not documented here (see the files above / the code that writes it)*
  - `other_window_anchor` (str; e.g. '15 Feb')  - *meaning not documented here (see the files above / the code that writes it)*

### `results\V2_peak_follows_exam_date_pre.csv`
- size 1 KB; modified 2026-10-13; rows 4
- columns / contents:
  - `year` (int64; e.g. '2017'): publication year
  - `gap_own_window` (float64; e.g. '0.0895814401042037')  - *meaning not documented here (see the files above / the code that writes it)*
  - `own_lo` (float64; e.g. '0.0002170847997845')  - *meaning not documented here (see the files above / the code that writes it)*
  - `own_hi` (float64; e.g. '0.1714619067547931')  - *meaning not documented here (see the files above / the code that writes it)*
  - `gap_other_regime_window` (float64; e.g. '0.0879533157655905')  - *meaning not documented here (see the files above / the code that writes it)*
  - `other_lo` (float64; e.g. '-0.0116463644960095')  - *meaning not documented here (see the files above / the code that writes it)*
  - `other_hi` (float64; e.g. '0.1855587416265665')  - *meaning not documented here (see the files above / the code that writes it)*
  - `other_window_anchor` (str; e.g. '15 Feb')  - *meaning not documented here (see the files above / the code that writes it)*

### `results\contrasts_full_all.csv`
- size 3 KB; modified 2026-10-17; rows 28
- columns / contents:
  - `spec` (str; e.g. 'MAIN science+maths, control A, all acces')  - *meaning not documented here (see the files above / the code that writes it)*
  - `lang` (str; e.g. 'en')  - *meaning not documented here (see the files above / the code that writes it)*
  - `estimator` (str; e.g. 'article-level')  - *meaning not documented here (see the files above / the code that writes it)*
  - `n_pairs` (int64; e.g. '711')  - *meaning not documented here (see the files above / the code that writes it)*
  - `D` (str; e.g. '-0.0455')  - *meaning not documented here (see the files above / the code that writes it)*
  - `D_lo` (str; e.g. '-0.0593')  - *meaning not documented here (see the files above / the code that writes it)*
  - `D_hi` (str; e.g. '-0.0326')  - *meaning not documented here (see the files above / the code that writes it)*
  - `perm_p_one_sided` (str; e.g. '0.1286')  - *meaning not documented here (see the files above / the code that writes it)*
  - `perm_splits` (str; e.g. '70.0')  - *meaning not documented here (see the files above / the code that writes it)*
  - `pre_slope` (str; e.g. '-0.011')  - *meaning not documented here (see the files above / the code that writes it)*
  - `post_slope` (str; e.g. '-0.0254')  - *meaning not documented here (see the files above / the code that writes it)*
  - `share_pairs_negative` (str; e.g. '0.616')  - *meaning not documented here (see the files above / the code that writes it)*

### `results\contrasts_pilot_pre.csv`
- size 1 KB; modified 2026-10-13; rows 25
- columns / contents:
  - `spec` (str; e.g. 'MAIN science+maths, control A, all acces')  - *meaning not documented here (see the files above / the code that writes it)*
  - `lang` (str; e.g. 'en')  - *meaning not documented here (see the files above / the code that writes it)*
  - `estimator` (str; e.g. 'article-level')  - *meaning not documented here (see the files above / the code that writes it)*
  - `n_pairs` (int64; e.g. '40')  - *meaning not documented here (see the files above / the code that writes it)*
  - `D` (str; e.g. '')  - *meaning not documented here (see the files above / the code that writes it)*
  - `D_lo` (str; e.g. '')  - *meaning not documented here (see the files above / the code that writes it)*
  - `D_hi` (str; e.g. '')  - *meaning not documented here (see the files above / the code that writes it)*
  - `perm_p_one_sided` (str; e.g. '')  - *meaning not documented here (see the files above / the code that writes it)*
  - `perm_splits` (str; e.g. '')  - *meaning not documented here (see the files above / the code that writes it)*
  - `pre_slope` (str; e.g. '')  - *meaning not documented here (see the files above / the code that writes it)*
  - `post_slope` (str; e.g. '')  - *meaning not documented here (see the files above / the code that writes it)*
  - `share_pairs_negative` (str; e.g. '')  - *meaning not documented here (see the files above / the code that writes it)*

### `results\event_study_regression_full_all.csv`
- size 0 KB; modified 2026-10-17; rows 7
- columns / contents:
  - `year` (int64; e.g. '2017'): publication year
  - `beta` (float64; e.g. '0.0214')  - *meaning not documented here (see the files above / the code that writes it)*
  - `se` (float64; e.g. '0.0161')  - *meaning not documented here (see the files above / the code that writes it)*
  - `ci_lo` (float64; e.g. '-0.0102')  - *meaning not documented here (see the files above / the code that writes it)*
  - `ci_hi` (float64; e.g. '0.053')  - *meaning not documented here (see the files above / the code that writes it)*
  - `lang` (str; e.g. 'en')  - *meaning not documented here (see the files above / the code that writes it)*

### `results\event_study_regression_pilot_pre.csv`
- size 0 KB; modified 2026-10-13; rows 3
- columns / contents:
  - `year` (int64; e.g. '2017'): publication year
  - `beta` (float64; e.g. '-0.0097')  - *meaning not documented here (see the files above / the code that writes it)*
  - `se` (float64; e.g. '0.0447')  - *meaning not documented here (see the files above / the code that writes it)*
  - `ci_lo` (float64; e.g. '-0.0974')  - *meaning not documented here (see the files above / the code that writes it)*
  - `ci_hi` (float64; e.g. '0.078')  - *meaning not documented here (see the files above / the code that writes it)*
  - `lang` (str; e.g. 'en')  - *meaning not documented here (see the files above / the code that writes it)*

### `results\india_country_rows.csv`
- size 822 KB; modified 2026-10-17; rows 20491
- columns / contents:
  - `exam_year` (int64; e.g. '2018')  - *meaning not documented here (see the files above / the code that writes it)*
  - `window` (str; e.g. 'exam')  - *meaning not documented here (see the files above / the code that writes it)*
  - `date` (str; e.g. '2018-02-21'): publication date
  - `page_id` (int64; e.g. '22834')  - *meaning not documented here (see the files above / the code that writes it)*
  - `group` (str; e.g. 'syllabus')  - *meaning not documented here (see the files above / the code that writes it)*
  - `n` (int64; e.g. '594')  - *meaning not documented here (see the files above / the code that writes it)*

### `results\log_02_controls.txt`
- size 1 KB; modified 2026-10-13
- columns / contents:
  - (could not read: ParserError)

### `results\log_03_full.txt`
- size 2 KB; modified 2026-10-17; rows 21
- columns / contents:
  - `tier sizes: [1509` (str; e.g. 'full: 4192 articles')  - *meaning not documented here (see the files above / the code that writes it)*
  - ` 1105` (str; e.g. ' 4319 titles (incl. redirects)')  - *meaning not documented here (see the files above / the code that writes it)*
  - ` 515` (str; e.g. ' 6146 series')  - *meaning not documented here (see the files above / the code that writes it)*
  - ` 1509` (str; e.g. ' 5781 still to fetch')  - *meaning not documented here (see the files above / the code that writes it)*
  - ` 733` (str; e.g. '')  - *meaning not documented here (see the files above / the code that writes it)*
  - ` 457` (str; e.g. '')  - *meaning not documented here (see the files above / the code that writes it)*
  - ` 318]` (str; e.g. '')  - *meaning not documented here (see the files above / the code that writes it)*

### `results\log_03_pilot.txt`
- size 1 KB; modified 2026-10-13; rows 8
- columns / contents:
  - `pilot: 249 articles` (str; e.g. '  fetched 250 / 1113 new series')  - *meaning not documented here (see the files above / the code that writes it)*
  - ` 374 titles (incl. redirects)` (str; e.g. ' 447 s elapsed')  - *meaning not documented here (see the files above / the code that writes it)*
  - ` 1122 series` (str; e.g. ' about 26 min left')  - *meaning not documented here (see the files above / the code that writes it)*
  - ` 1113 still to fetch` (str; e.g. '')  - *meaning not documented here (see the files above / the code that writes it)*

### `results\log_05_full_all.txt`
- size 13 KB; modified 2026-10-17; rows 83
- columns / contents:
  - `D:\Research-Publishing\05-wikipedia-exam-traffic\code\05_analyze.py:149: RuntimeWarning: divide by zero encountered in log` (str; e.g. ' b].sum() / len(b))')  - *meaning not documented here (see the files above / the code that writes it)*

### `results\log_06_country_download.txt`
- size 5 KB; modified 2026-10-13; rows 71
- columns / contents:
  - `  2018-02-21  India rows kept: 5348  (transferred so far: 2 MB)` (str; e.g. '  2018-02-27  India rows kept: 5450  (tr')  - *meaning not documented here (see the files above / the code that writes it)*

### `results\log_06_india_analyze.txt`
- size 1 KB; modified 2026-10-17
- columns / contents:
  - (could not read: ParserError)

### `results\plan_freeze.txt`
- size 0 KB; modified 2026-10-17; rows 6
- columns / contents:
  - `Plan frozen: 2026-10-13T16:47:14Z UTC` (str; e.g. '2b3fd663e887ed6563f3b0cc4b5a9d4ceb5ee8ef')  - *meaning not documented here (see the files above / the code that writes it)*

### `results\secondary_eve_contrast_all.csv`
- size 0 KB; modified 2026-10-17; rows 9
- columns / contents:
  - `subject` (str; e.g. 'X-SCI')  - *meaning not documented here (see the files above / the code that writes it)*
  - `n_pairs` (int64; e.g. '181')  - *meaning not documented here (see the files above / the code that writes it)*
  - `D_eve` (float64; e.g. '-0.0212')  - *meaning not documented here (see the files above / the code that writes it)*
  - `lo` (float64; e.g. '-0.0471')  - *meaning not documented here (see the files above / the code that writes it)*
  - `hi` (float64; e.g. '0.0056')  - *meaning not documented here (see the files above / the code that writes it)*
  - `share_pairs_negative` (float64; e.g. '0.5635')  - *meaning not documented here (see the files above / the code that writes it)*

### `results\secondary_eve_contrast_pre.csv`
- size 0 KB; modified 2026-10-13
- columns / contents:
  - (could not read: EmptyDataError)

### `results\secondary_eve_of_paper_full_all.csv`
- size 8 KB; modified 2026-10-17; rows 49
- columns / contents:
  - `subject` (str; e.g. 'X-SCI')  - *meaning not documented here (see the files above / the code that writes it)*
  - `year` (int64; e.g. '2017'): publication year
  - `paper_date` (str; e.g. '2017-03-22')  - *meaning not documented here (see the files above / the code that writes it)*
  - `n_pairs` (int64; e.g. '181')  - *meaning not documented here (see the files above / the code that writes it)*
  - `spike_syllabus` (float64; e.g. '0.1376103877770523')  - *meaning not documented here (see the files above / the code that writes it)*
  - `spike_control` (float64; e.g. '0.0431437759154372')  - *meaning not documented here (see the files above / the code that writes it)*
  - `gap` (float64; e.g. '0.094466611861615')  - *meaning not documented here (see the files above / the code that writes it)*
  - `ci_lo` (float64; e.g. '0.0663333821807552')  - *meaning not documented here (see the files above / the code that writes it)*
  - `ci_hi` (float64; e.g. '0.1227577494311302')  - *meaning not documented here (see the files above / the code that writes it)*
  - `date_verification` (str; e.g. 'primary (text PDF read)')  - *meaning not documented here (see the files above / the code that writes it)*

### `results\secondary_eve_of_paper_pilot_pre.csv`
- size 2 KB; modified 2026-10-13; rows 15
- columns / contents:
  - `subject` (str; e.g. 'X-SCI')  - *meaning not documented here (see the files above / the code that writes it)*
  - `year` (int64; e.g. '2017'): publication year
  - `paper_date` (str; e.g. '2017-03-22')  - *meaning not documented here (see the files above / the code that writes it)*
  - `n_pairs` (int64; e.g. '12')  - *meaning not documented here (see the files above / the code that writes it)*
  - `spike_syllabus` (float64; e.g. '0.2364628875293991')  - *meaning not documented here (see the files above / the code that writes it)*
  - `spike_control` (float64; e.g. '0.0973390419717713')  - *meaning not documented here (see the files above / the code that writes it)*
  - `gap` (float64; e.g. '0.1391238455576278')  - *meaning not documented here (see the files above / the code that writes it)*
  - `ci_lo` (float64; e.g. '0.0141075489208367')  - *meaning not documented here (see the files above / the code that writes it)*
  - `ci_hi` (float64; e.g. '0.2716672703422958')  - *meaning not documented here (see the files above / the code that writes it)*
  - `date_verification` (str; e.g. 'primary (text PDF read)')  - *meaning not documented here (see the files above / the code that writes it)*

### `results\yearly_gaps_full_all.csv`
- size 26 KB; modified 2026-10-17; rows 264
- columns / contents:
  - `spec` (str; e.g. 'MAIN science+maths, control A, all acces')  - *meaning not documented here (see the files above / the code that writes it)*
  - `lang` (str; e.g. 'en')  - *meaning not documented here (see the files above / the code that writes it)*
  - `estimator` (str; e.g. 'article-level')  - *meaning not documented here (see the files above / the code that writes it)*
  - `year` (int64; e.g. '2016'): publication year
  - `role` (str; e.g. 'set aside')  - *meaning not documented here (see the files above / the code that writes it)*
  - `n_pairs` (int64; e.g. '707')  - *meaning not documented here (see the files above / the code that writes it)*
  - `uplift_syllabus` (float64; e.g. '0.2078')  - *meaning not documented here (see the files above / the code that writes it)*
  - `uplift_control` (float64; e.g. '0.0835')  - *meaning not documented here (see the files above / the code that writes it)*
  - `gap` (float64; e.g. '0.1238')  - *meaning not documented here (see the files above / the code that writes it)*
  - `ci_lo` (float64; e.g. '0.1011')  - *meaning not documented here (see the files above / the code that writes it)*
  - `ci_hi` (float64; e.g. '0.1471')  - *meaning not documented here (see the files above / the code that writes it)*
  - `median_gap` (str; e.g. '0.1071')  - *meaning not documented here (see the files above / the code that writes it)*

### `results\yearly_gaps_pilot_pre.csv`
- size 10 KB; modified 2026-10-13; rows 100
- columns / contents:
  - `spec` (str; e.g. 'MAIN science+maths, control A, all acces')  - *meaning not documented here (see the files above / the code that writes it)*
  - `lang` (str; e.g. 'en')  - *meaning not documented here (see the files above / the code that writes it)*
  - `estimator` (str; e.g. 'article-level')  - *meaning not documented here (see the files above / the code that writes it)*
  - `year` (int64; e.g. '2016'): publication year
  - `role` (str; e.g. 'set aside')  - *meaning not documented here (see the files above / the code that writes it)*
  - `n_pairs` (int64; e.g. '40')  - *meaning not documented here (see the files above / the code that writes it)*
  - `uplift_syllabus` (float64; e.g. '0.2558')  - *meaning not documented here (see the files above / the code that writes it)*
  - `uplift_control` (float64; e.g. '0.1296')  - *meaning not documented here (see the files above / the code that writes it)*
  - `gap` (float64; e.g. '0.1262')  - *meaning not documented here (see the files above / the code that writes it)*
  - `ci_lo` (float64; e.g. '0.0483')  - *meaning not documented here (see the files above / the code that writes it)*
  - `ci_hi` (float64; e.g. '0.2213')  - *meaning not documented here (see the files above / the code that writes it)*
  - `median_gap` (str; e.g. '0.0623')  - *meaning not documented here (see the files above / the code that writes it)*

### `data\cache\` (summarised)
- 6657 files, 70 MB. Raw downloads/caches as fetched on the stated dates; not individually listed. Check the code that fills it for the source URL.
