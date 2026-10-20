# Search protocol - 05-wikipedia-exam-traffic

- Paper question: Did exam-season Wikipedia traffic for syllabus topics shrink after ChatGPT?
- Date of search and data pull: **2026-10-17**
- Years covered: 2005-2026; language: English (OpenAlex language field `en` or missing)
- Built by an AI agent (Claude) with the scripts in `python\` and `R\`; all numbers below are read from the run logs.

## 1. Databases

| Role | Database | Access | Note |
|---|---|---|---|
| Discovery | Crossref REST API | free, no key, `mailto` polite pool | relevance-ranked keyword search; top N per query |
| Discovery | Semantic Scholar Graph API (bulk search) | free, no key | boolean search on title/abstract; top N by citations per query |
| Discovery | ERIC API | free, no key | education topics only |
| Discovery | arXiv API | free, no key | preprints |
| Enrichment (authors, institutions, countries, topics, keywords, abstracts, references, citation counts, OA links) | **OpenAlex** single-record lookups (`/works/doi:...`, `/works/mag:...`, `/works/W...`) | free, no key | see limit 1 below |
| Forward citations for snowballing | OpenCitations Index API v2 | free, no key | DOI-to-DOI citations only |
| Cross-check | Crossref (per-DOI), Semantic Scholar (batch) | free, no key | citation counts and reference-list coverage compared in `tables\coverage_crosscheck.csv` |
| Not used | Scopus, Web of Science, Lens, Dimensions | need accounts | equivalent strings are in `scopus-queries.md` |
| Not usable | RePEc/IDEAS | its API needs a registered access code; the public search page returned no parseable result list to a script | economics working papers still enter via Crossref, Semantic Scholar and snowballing |

**Why OpenAlex was not the search engine.** Since 2026 OpenAlex charges keyless list/search calls against a small daily budget shared by everyone on the same IP address ($0.10/day). On the day of the pull that budget was already exhausted by other work on this network, and an API key needs an account (ruled out). Single-record lookups remain free and unlimited, so records were *discovered* in Crossref / Semantic Scholar / ERIC / arXiv and then *enriched* one by one from OpenAlex. Consequence: a work that is in OpenAlex but not found by any of the four discovery databases is missed, except where snowballing caught it.

## 2. Exact search strings

### A_genai_knowledge_platforms: Generative AI / AI search and knowledge platforms

| database | query | hits in database | records retrieved | status |
|---|---|---|---|---|
| crossref | ChatGPT impact Wikipedia traffic page views | 2000341.0 | 250 | ok |
| crossref | large language models Stack Overflow activity decline | 3406300.0 | 250 | ok |
| crossref | generative AI online knowledge communities participation | 2409507.0 | 250 | ok |
| crossref | AI Overviews search traffic websites publishers | 939155.0 | 250 | ok |
| crossref | ChatGPT substitution user-generated content platforms | 751579.0 | 250 | ok |
| s2 | (ChatGPT \| "generative AI" \| "large language models" \| LLM \| LLMs) + Wikipedia + (traffic \| pageviews \| "page views" \| engagement \| readership \| decline \| editing \| contributions) | 90.0 | 90 | ok |
| s2 | (ChatGPT \| "generative AI" \| "large language models" \| LLMs) + ("Stack Overflow" \| "Stack Exchange") + (decline \| activity \| questions \| traffic \| impact) | 115.0 | 115 | ok |
| s2 | (ChatGPT \| "generative AI" \| "AI Overviews" \| "AI search") + ("web traffic" \| "website traffic" \| "search traffic" \| publishers \| "knowledge platforms" \| "online communities" \| "user-generated content") | 469.0 | 469 | ok |
| s2 | ("generative AI" \| ChatGPT \| "large language models") + ("digital public goods" \| "knowledge commons" \| "online knowledge communities" \| "knowledge sharing") + (contribution \| participation \| decline) | 40.0 | 40 | ok |
| s2 | (ChatGPT \| "generative AI") + ("Google Trends" \| "search interest" \| Chegg \| "homework help") | 168.0 | 168 | ok |
| arxiv | all:Wikipedia AND all:ChatGPT AND (all:pageviews OR all:traffic OR all:engagement) | 3.0 | 3 | ok |
| arxiv | all:"Stack Overflow" AND (all:ChatGPT OR all:"large language models") AND (all:decline OR all:activity OR all:impact) | 19.0 | 19 | ok |
| arxiv | all:"generative AI" AND (all:"online communities" OR all:"knowledge platforms" OR all:"user-generated content") AND (all:traffic OR all:participation) | 5.0 | 5 | ok |
| arxiv | all:"AI Overviews" AND (all:traffic OR all:clicks) | 9.0 | 9 | ok |
| arxiv | all:Wikipedia AND (all:"large language models" OR all:"generative AI") AND (all:readership OR all:traffic OR all:decline OR all:editors) | 14.0 | 14 | ok |

### B_wikipedia_pageviews: Wikipedia page-view research / behavioural signal

| database | query | hits in database | records retrieved | status |
|---|---|---|---|---|
| crossref | Wikipedia page views analysis | 5319396.0 | 250 | ok |
| crossref | Wikipedia traffic data forecasting nowcasting | 2478633.0 | 250 | ok |
| crossref | Wikipedia readers reading behaviour study | 5667789.0 | 250 | ok |
| crossref | Wikipedia page view statistics collective attention | 873600.0 | 250 | ok |
| crossref | Wikipedia usage seasonality students academic calendar | 1416494.0 | 250 | ok |
| crossref | Wikipedia pageviews proxy public interest | 1375037.0 | 250 | ok |
| s2 | Wikipedia + (pageviews \| "page views" \| "page view" \| "page-view" \| "traffic data" \| "view counts" \| "access logs" \| clickstream) | 360.0 | 360 | ok |
| s2 | Wikipedia + (readers \| readership \| "reading behavior" \| navigation) + (study \| analysis \| characterization \| "large-scale") | 628.0 | 628 | ok |
| s2 | Wikipedia + (pageviews \| "page views" \| traffic \| views) + (forecasting \| nowcasting \| predict \| surveillance \| "stock market" \| "box office" \| election \| epidemic \| influenza \| "collective attention" \| seasonality) | 308.0 | 308 | ok |
| arxiv | all:Wikipedia AND (all:pageviews OR all:"page views" OR all:"page view") | 48.0 | 48 | ok |
| arxiv | ti:Wikipedia AND (ti:readers OR ti:reading OR ti:navigation OR ti:traffic OR ti:attention) | 22.0 | 22 | ok |

### C_student_information_seeking: Students' information-seeking and AI tools for schoolwork

| database | query | hits in database | records retrieved | status |
|---|---|---|---|---|
| crossref | students use of Wikipedia academic information seeking | 4651664.0 | 250 | ok |
| crossref | high school students information seeking behaviour internet search engines homework | 370171.0 | 250 | ok |
| crossref | ChatGPT use by secondary school students homework survey | 3458110.0 | 250 | ok |
| crossref | generative AI adoption teenagers schoolwork | 681933.0 | 250 | ok |
| s2 | (students \| undergraduates \| pupils) + Wikipedia + (use \| usage \| "information seeking" \| credibility \| academic) | 1707.0 | 800 | ok |
| s2 | (students \| adolescents \| teenagers) + ("information seeking" \| "information-seeking" \| "information behavior" \| "information behaviour") + (school \| homework \| academic \| "search engines" \| Google) | 2105.0 | 800 | ok |
| s2 | (ChatGPT \| "generative AI") + (homework \| schoolwork \| "high school" \| "secondary school" \| "K-12" \| teenagers \| adolescents) + (use \| usage \| adoption \| survey) | 1663.0 | 800 | ok |
| eric | Wikipedia AND students AND ("information seeking" OR "use studies" OR credibility) | 33.0 | 33 | ok |
| eric | "information seeking" AND ("secondary school students" OR "high school students") AND (internet OR "search engines") | 43.0 | 35 | ok |
| eric | (ChatGPT OR "generative artificial intelligence") AND (homework OR "high school students" OR "secondary school students") AND (use OR usage) | 67.0 | 67 | ok |

Per-query retrieval caps: crossref = 250, s2 = 800, eric = 300, arxiv = 150. Crossref totals are large because its search is an OR-type relevance ranking; only the top-ranked records were taken. Raw responses for every query are in `data\raw\<database>\`.

### Seed papers (known key works, each verified to exist by a Crossref title match; they bypass the keyword rules)

| seed title | result |
|---|---|
| Large language models reduce public knowledge sharing on online Q&A platforms | matched 10.1093/pnasnexus/pgae400 |
| The consequences of generative AI for online knowledge communities | matched 10.1038/s41598-024-61221-0 |
| Why We Read Wikipedia | matched 10.1145/3038912.3052716 |
| Wikipedia Usage Estimates Prevalence of Influenza-Like Illness in the United States in Near Real-Time | matched 10.1371/journal.pcbi.1003581 |
| Quantifying Wikipedia Usage Patterns Before Stock Market Moves | matched 10.1038/srep01801 |
| Early Prediction of Movie Box Office Success Based on Wikipedia Activity Big Data | matched 10.1371/journal.pone.0071226 |
| Forecasting the 2013-2014 Influenza Season Using Wikipedia | matched 10.1371/journal.pcbi.1004239 |
| Global Disease Monitoring and Forecasting with Wikipedia | matched 10.5210/ojphi.v8i1.6530 |
| Wikipedia traffic data and electoral prediction: towards theoretically informed models | matched 10.1140/epjds/s13688-016-0083-3 |
| Dynamics and biases of online attention: the case of aircraft crashes | matched 10.1098/rsos.160460 |
| The memory remains: Understanding collective memory in the digital age | matched 10.1126/sciadv.1602368 |
| How today's college students use Wikipedia for course-related research | matched 10.5210/fm.v15i3.2830 |
| Death by AI: Will large language models diminish Wikipedia? | matched 10.1002/asi.24975 |
| Wikipedia in the eyes of its beholders: A systematic review of scholarly research on Wikipedia readers and readership | matched 10.1002/asi.23162 |
| The Substantial Interdependence of Wikipedia and Google: A Case Study on the Relationship Between Peer Production Communities and Information Technologies | matched 10.1609/icwsm.v11i1.14883 |
| Measuring the Importance of User-Generated Content to Search Engines | matched 10.1609/icwsm.v13i01.3248 |
| Sudden Attention Shifts on Wikipedia During the COVID-19 Crisis | matched 10.1609/icwsm.v15i1.18054 |
| Exploring the impact of ChatGPT on Wikipedia engagement | matched 10.1177/26339137251372599 |

Seed arXiv ids (from the PDFs the substance agent saved in the paper folder): 1702.05379, 1812.00474, 2112.11848, 2307.07367, 2405.10205, 2503.00757, 2509.05879, 2602.09550, 2602.18455, 2609.36069, 2609.38563

## 3. Inclusion and exclusion rules (applied identically to search hits and snowballed records)

A record is **included** if all of the following hold:
1. It resolves to an OpenAlex work record (by DOI, MAG id, or a Crossref title match of at least 93% similarity).
2. OpenAlex type is article, review, preprint, book chapter, book, dissertation, report or other (editorials, errata, paratext, datasets, peer reviews are dropped).
3. Publication year 2005-2026; language English or unrecorded.
4. It satisfies at least one sub-literature rule below: every `include` pattern must match in title + abstract, and every `title_must` pattern must match in the title.
5. Its title does not match the exclusion pattern.

Book-series and proceedings trap: a record whose abstract is a series/proceedings blurb (detected by wording such as 'this volume constitutes the refereed proceedings', or the same abstract shared by 3+ records) is screened on its title alone; whole-volume records (titles starting 'Proceedings of', 'Front matter', etc.) are dropped.

The patterns are case-insensitive regular expressions (`\b` = word boundary, `\w*` = any word ending, `.{0,80}` = within 80 characters).

**A_genai_knowledge_platforms - Generative AI / AI search and knowledge platforms**

- include (title+abstract): `(chatgpt|generative ai|generative artificial intelligence|genai|large language models?|\bllms?\b|ai overviews?|ai[- ]generated|ai search|ai chatbots?|gpt-?[34]|conversational ai|ai summar\w+)`
- include (title+abstract): `(wikipedia|stack ?overflow|stack ?exchange|q&a (platforms?|communit\w+|sites?|forums?)|question[- ]and[- ]answer|online knowledge|knowledge (communit\w+|platforms?|commons|sharing)|digital public goods?|user[- ]generated content|web ?traffic|website traffic|search traffic|publishers?|online communit\w+|reddit|quora|chegg|google trends|search interest|homework help|open[- ]source|search engines?|web search)`
- include (title+abstract): `(traffic|page ?views?|pageviews|engagement|declin\w+|displac\w+|substitut\w+|participation|contribut\w+|posting|visits|readership|crowd\w* out|user activity|activity on|clicks?|search interest|demand|usage)`
- title_must (title): `(chatgpt|generative|genai|large language models?|\bllms?\b|\bai\b|gpt|artificial intelligence|language models?)`
- title_must (title): `(wikipedia|stack ?overflow|stack ?exchange|q&a|question|knowledge|communit\w+|traffic|platforms?|public goods?|search|chegg|google|\bweb\b|content|forums?|reddit|crowd\w*|publishers?|open[- ]source|peer production|commons|homework|tutoring)`

**B_wikipedia_pageviews - Wikipedia page-view research / behavioural signal**

- include (title+abstract): `wikipedia`
- include (title+abstract): `(page ?views?|pageviews|page[- ]view|\btraffic|readership|\breaders?\b|reading (behaviou?r|sessions?|patterns?)|view counts?|usage (data|statistics|logs?|patterns?)|access (logs?|statistics|data)|clickstream|navigat\w+|collective attention|public attention|online attention|attention (dynamics|to|shifts?)|visits|information[- ]seeking|search (behaviou?r|interest|volume))`
- title_must (title): `wikipedia`

**C_student_information_seeking - Students' information-seeking and AI tools for schoolwork**

- include (title+abstract): `(\b(students?|pupils|undergraduates?|school)\b.{0,200}wikipedia|wikipedia.{0,200}\b(students?|pupils|undergraduates?|school|homework|coursework|academic)\b|(information[- ]seeking|information behaviou?r|search (behaviou?r|habits)|use of search engines).{0,200}\b(students?|pupils|adolescents?|teenagers?)\b|\b(students?|pupils|adolescents?|teenagers?)\b.{0,200}(information[- ]seeking|information behaviou?r|search (behaviou?r|habits))|(chatgpt|generative ai|genai|ai chatbots?|ai tools?|large language models?).{0,200}(homework|schoolwork|high school|secondary school|k-?12|adolescents?|teenagers?|teens\b|exam preparation)|(homework|schoolwork|high school|secondary school|k-?12|adolescents?|teenagers?|teens\b|exam preparation).{0,200}(chatgpt|generative ai|genai|ai chatbots?|ai tools?|large language models?))`
- include (title+abstract): `(wikipedia|internet|\bweb\b|online|search engines?|google|chatgpt|generative ai|\bai\b|artificial intelligence|digital)`
- title_must (title): `(students?|pupils|adolescents?|teen\w*|school\w*|undergraduates?|homework|youth|children|young people|learners)`
- title_must (title): `(wikipedia|information|search\w*|chatgpt|generative|\bai\b|artificial intelligence|homework|google|internet|\bweb\b|online)`

**Exclusion pattern (title):** `(question answering|retrieval[- ]augmented|benchmark|\bdatasets?\b|fine-?tun|pre-?train|embedding|entity (linking|recognition|disambiguation)|summari[sz]ation|machine translation|knowledge graph|hallucinat|parsing|language model(l)?ing|text generation|named entity|wikidata|word sense|semantic (similarity|relatedness)|ontolog|vandalism|\bnursing|\bdental|pharmac|surg|radiolog|patient education|code generation|program repair|prompt engineering|text classification|infobox|link prediction|recommender|recommendation|spectroscop|\bpatients?\b|museum|journalism|\bmedical|clinical|autism|writing skills|english (writing|skills|language)|\befl\b|\besl\b|keyphrase|multilingual)`

A record matching several rules is assigned to the first one in the order listed (its other matches are kept in `sublits_all`).

## 4. Snowballing (one round)

- Central papers: the 28 corpus records ranked highest on local citations + topical relevance + log(global citations) - listed in `data\clean\snowball_central_papers.csv`.
- Backward: every OpenAlex `referenced_works` entry of those papers not already in the corpus (1064 candidates).
- Forward: citing DOIs from OpenCitations, up to 150 per central paper (1263 candidates). OpenCitations only knows DOI-to-DOI links, so citing preprints and books without DOIs are missed.
- All candidates were looked up in OpenAlex and screened with the rules in section 3: 17 backward and 33 forward records were added.

## 5. PRISMA-style counts

| stage | n |
|---|---|
| Records identified through database searching (all query hits) | 8631 |
|    of which from arxiv | 120 |
|    of which from crossref | 3750 |
|    of which from eric | 135 |
|    of which from s2 | 4578 |
|    of which from seed | 48 |
| Duplicates removed (same DOI / id / title across queries and databases) | 1033 |
| Unique records screened on title (+ abstract where the database supplied one) | 7598 |
| Removed at title pre-screen (off-topic) | 6322 |
| Records looked up in OpenAlex | 1276 |
| Duplicates removed after OpenAlex matching (same work / same title) | 27 |
| Excluded at full screen: type_excluded | 239 |
| Excluded at full screen: offtopic_fails_inclusion_rule | 219 |
| Excluded at full screen: no_openalex_record (no DOI / not indexed) | 56 |
| Excluded at full screen: year_out_of_range | 17 |
| Excluded at full screen: language_not_english | 7 |
| Excluded at full screen: paratext_or_container_record | 1 |
| Included after search screening | 710 |
| Snowball: central papers used | 28 |
| Snowball: backward-reference candidates | 1064 |
| Snowball: forward-citation candidates (OpenCitations) | 1263 |
| Snowball: duplicates of corpus records | 10 |
| Snowball excluded: offtopic_fails_inclusion_rule | 1534 |
| Snowball excluded: type_excluded | 274 |
| Snowball excluded: no_openalex_record | 157 |
| Snowball excluded: offtopic_exclusion_term_in_title | 125 |
| Snowball excluded: year_out_of_range | 122 |
| Snowball excluded: language_not_english | 44 |
| Snowball excluded: paratext_or_container_record | 11 |
| Snowball: included (backward) | 17 |
| Snowball: included (forward) | 33 |
| Corpus before hand-screening | 760 |
| Removed at hand-screening (see tables/hand_screen_removed.csv) | 129 |
| FINAL CORPUS | 631 |
|    with abstract | 582 |
|    with DOI | 576 |
|    with a reference list in OpenAlex | 480 |
| Distinct cited references / resolved to metadata | 16727 / 4268 |

Figure: `figures\py_01_prisma_flow.png`.

## 6. Hand-screening

After rule screening and snowballing, the agent read the titles (with source and year) of the whole corpus and removed 129 records as off-topic or mis-matched; every removal and its reason is in `tables\hand_screen_removed.csv`. This is a single-screener pass by an AI agent on titles, not a two-person human screen; borderline records were kept.

Removal reasons:
- health, mental-health or clinical topic, not students' schoolwork or knowledge platforms: 69
- off-topic: Wikipedia content/language/biography/tool study, not readership or use: 21
- off-topic: research-publishing / scholarly-writing / AI-ethics policy, not knowledge platforms: 18
- off-topic: LLM engineering / application unrelated to knowledge-platform use or schoolwork: 15
- off-topic: not about students' information seeking or AI use for schoolwork: 6

## 7. Coverage and cross-checks

| item | value |
|---|---|
| corpus records | 631.0 |
| records with DOI | 576.0 |
| found in Crossref (DOI lookup) | 531.0 |
| found in Semantic Scholar (batch DOI lookup) | 538.0 |
| Spearman corr. OpenAlex vs Crossref cited-by | 0.974 |
| Spearman corr. OpenAlex vs Semantic Scholar cited-by | 0.918 |
| median cited-by: OpenAlex | 6.0 |
| median cited-by: Crossref | 6.0 |
| median cited-by: Semantic Scholar | 7.5 |
| records with no reference list in OpenAlex | 151.0 |
|   of which Crossref holds a reference list | 6.0 |
| records with no institution/country data | 99.0 |
| records without abstract | 49.0 |
| open-access records (OpenAlex) | 443.0 |
| origin: search | 553.0 |
| origin: snowball_forward | 33.0 |
| origin: seed | 30.0 |
| origin: snowball_backward | 15.0 |
| retrieved by: s2 | 559.0 |
| retrieved by: openalex_snowball | 48.0 |
| retrieved by: eric | 38.0 |
| retrieved by: arxiv | 36.0 |
| retrieved by: seed | 31.0 |


- 56 title-screened candidates could not be matched to any OpenAlex record (no DOI or MAG id, or not indexed) and are **not** in the corpus. They are listed in `data\clean\unresolved_candidates.csv` (s2: 47, eric: 10). ERIC reports and theses and Indian or legal journal articles without DOIs dominate this list.

- Cited references: 16727 distinct works are cited by the corpus (21882 links); 4268 of the 5000 outside the corpus were resolved to metadata for the co-citation and RPYS analyses.


### Named prior work (seed list / the substance agent's saved papers) - is it in the corpus?

| id | kind | in_corpus | title |
|---|---|---|---|
| 10.1016/j.jebo.2020.12.004 | doi | 1 |  |
| 10.1038/s41598-024-61221-0 | doi | 1 |  |
| 10.1093/pnasnexus/pgae400 | doi | 1 |  |
| 10.1145/3038912.3052716 | doi | 1 |  |
| 10.1145/3386527.3405913 | doi | 1 |  |
| 10.1177/26339137251372599 | doi | 1 |  |
| 10.1371/journal.pbio.3000146 | doi | 1 |  |
| 10.2139/ssrn.6164926 | doi | 0 |  |
| 10.2196/34464 | doi | 1 |  |
| arXiv:1702.05379 | arxiv | 1 | Why We Read Wikipedia |
| arXiv:1812.00474 | arxiv | 1 | Why the World Reads Wikipedia: Beyond English Speakers |
| arXiv:2112.11848 | arxiv | 1 | A Large-Scale Characterization of How Readers Browse Wikipedia |
| arXiv:2307.07367 | arxiv | 1 | Large language models reduce public knowledge sharing on online Q&A platforms |
| arXiv:2405.10205 | arxiv | 1 | Exploring the impact of ChatGPT on Wikipedia engagement |
| arXiv:2503.00757 | arxiv | 1 | Wikipedia Contributions in the Wake of ChatGPT |
| arXiv:2509.05879 | arxiv | 1 | Stack Overflow is not dead yet: Crowd answers still matter |
| arXiv:2602.09550 | arxiv | 1 | From Search to GenAI Queries: Global Trends in Physics Information-Seeking Across Topics and Regions |
| arXiv:2602.18455 | arxiv | 1 | Impact of AI Search Summaries on Website Traffic: Evidence from Google AI Overviews and Wikipedia |
| arXiv:2609.36069 | arxiv | 1 | The Uneven Decline of Collective Knowledge Production: Evidence from Stack Overflow After Generative AI |
| arXiv:2609.38563 | arxiv | 1 | Navigating the Changing Landscape of Online Knowledge Consumption and Production in the Age of Generative AI: Evidence from Stack Overflow |

## 8. API failures during the run

- api.openalex.org: failed after retries: {"error":"Rate limit exceeded","message":"Rate l (x617)


## 9. Scopus / Web of Science exports
- `scopus-drop\`: EMPTY - no Scopus/WoS export to merge; corpus is OpenAlex-only.
- Ready-to-paste strings: `scopus-queries.md`.
