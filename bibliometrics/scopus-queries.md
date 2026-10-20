# Scopus and Web of Science queries - paper 05 (Wikipedia exam-season traffic after ChatGPT)

Status: **not run.** There is no Scopus or Web of Science login on this machine. `scopus-drop\` was empty on 2026-10-13.
These strings mirror the three sub-literatures in `search-protocol.md`. Paste each into the *Advanced search* box.

How to use
- Scopus: Advanced document search -> paste -> Search -> Export -> **CSV** with *Citation information, Bibliographical information, Abstract & keywords, Include references*.
- Web of Science: Advanced Search (Core Collection) -> paste -> Export -> **BibTeX** or *Plain text*, Record Content = **Full Record and Cited References** (500 per file).
- Save exports into `bibliometrics\scopus-drop\` and re-run `R\bibliometrix_analysis.R`; it loads and merges whatever is there.
- Much of sub-literature A is 2023-2026 preprints (arXiv, SSRN) that neither Scopus nor WoS indexes. Expect both to return far fewer records than the free-database pull for A; they add most value for B and C.

## A. Generative AI / AI search and knowledge platforms

Scopus
```
TITLE-ABS-KEY ( ( chatgpt OR "generative AI" OR "generative artificial intelligence" OR "large language model*" OR llm OR llms OR "AI overview*" OR "AI search" OR "AI chatbot*" OR "conversational AI" )
  AND ( wikipedia OR "stack overflow" OR "stack exchange" OR "Q&A platform*" OR "Q&A communit*" OR "question-and-answer" OR "online knowledge communit*" OR "knowledge sharing platform*" OR "digital public good*"
        OR "user-generated content" OR "web traffic" OR "website traffic" OR "search traffic" OR "online communit*" OR reddit OR quora OR chegg OR "google trends" OR "search interest" OR "homework help" )
  AND ( traffic OR pageview* OR "page view*" OR engagement OR declin* OR displac* OR substitut* OR participation OR contribut* OR posting OR visits OR readership OR "crowd* out" OR "user activity" OR clicks ) )
AND NOT TITLE ( "question answering" OR "retrieval-augmented" OR benchmark OR dataset* OR "fine-tun*" OR "pre-train*" OR embedding* OR summari?ation OR "knowledge graph*" OR hallucinat* OR "code generation" )
AND PUBYEAR > 2021
```
Web of Science
```
TS=((ChatGPT OR "generative AI" OR "generative artificial intelligence" OR "large language model*" OR LLM OR LLMs OR "AI overview*" OR "AI search" OR "AI chatbot*" OR "conversational AI")
  AND (Wikipedia OR "Stack Overflow" OR "Stack Exchange" OR "Q&A platform*" OR "Q&A communit*" OR "question-and-answer" OR "online knowledge communit*" OR "knowledge sharing platform*" OR "digital public good*"
       OR "user-generated content" OR "web traffic" OR "website traffic" OR "search traffic" OR "online communit*" OR Reddit OR Quora OR Chegg OR "Google Trends" OR "search interest" OR "homework help")
  AND (traffic OR pageview* OR "page view*" OR engagement OR declin* OR displac* OR substitut* OR participation OR contribut* OR posting OR visits OR readership OR "crowd* out" OR "user activity" OR clicks))
NOT TI=("question answering" OR "retrieval-augmented" OR benchmark OR dataset* OR "fine-tun*" OR "pre-train*" OR embedding* OR summari$ation OR "knowledge graph*" OR hallucinat* OR "code generation")
AND PY=(2022-2026)
```

## B. Wikipedia page-view research / Wikipedia as a behavioural signal

Scopus
```
TITLE-ABS-KEY ( wikipedia AND ( pageview* OR "page view*" OR "page-view*" OR "traffic data" OR "wikipedia traffic" OR readership OR "wikipedia readers" OR "reading behavio*" OR "view count*" OR "usage data" OR "usage statistics"
   OR "access log*" OR clickstream OR "collective attention" OR "public attention" OR "online attention" OR "information-seeking" OR "search interest" OR nowcast* ) )
AND NOT TITLE ( "question answering" OR benchmark OR dataset* OR embedding* OR "entity linking" OR "named entity" OR "machine translation" OR "knowledge graph*" OR wikidata OR vandalism OR ontolog* OR "link prediction" OR recommend* )
AND PUBYEAR > 2004
```
Web of Science
```
TS=(Wikipedia AND (pageview* OR "page view*" OR "page-view*" OR "traffic data" OR "Wikipedia traffic" OR readership OR "Wikipedia readers" OR "reading behavio*" OR "view count*" OR "usage data" OR "usage statistics"
   OR "access log*" OR clickstream OR "collective attention" OR "public attention" OR "online attention" OR "information-seeking" OR "search interest" OR nowcast*))
NOT TI=("question answering" OR benchmark OR dataset* OR embedding* OR "entity linking" OR "named entity" OR "machine translation" OR "knowledge graph*" OR Wikidata OR vandalism OR ontolog* OR "link prediction" OR recommend*)
AND PY=(2005-2026)
```

## C. Students' information-seeking and use of AI tools for schoolwork

Scopus
```
TITLE-ABS-KEY ( ( ( student* OR pupil* OR undergraduate* OR school* ) W/15 wikipedia )
  OR ( ( "information-seeking" OR "information seeking" OR "information behavio*" OR "search behavio*" ) W/15 ( student* OR pupil* OR adolescen* OR teenager* ) )
  OR ( ( chatgpt OR "generative AI" OR "AI chatbot*" OR "AI tool*" ) W/15 ( homework OR schoolwork OR "high school" OR "secondary school" OR "K-12" OR adolescen* OR teenager* OR "exam preparation" ) ) )
AND NOT TITLE ( nursing OR dental OR pharmac* OR surg* OR radiolog* OR "patient education" )
AND PUBYEAR > 2004 AND ( LIMIT-TO ( LANGUAGE , "English" ) )
```
Web of Science
```
TS=(((student* OR pupil* OR undergraduate* OR school*) NEAR/15 Wikipedia)
  OR (("information-seeking" OR "information seeking" OR "information behavio*" OR "search behavio*") NEAR/15 (student* OR pupil* OR adolescen* OR teenager*))
  OR ((ChatGPT OR "generative AI" OR "AI chatbot*" OR "AI tool*") NEAR/15 (homework OR schoolwork OR "high school" OR "secondary school" OR "K-12" OR adolescen* OR teenager* OR "exam preparation")))
NOT TI=(nursing OR dental OR pharmac* OR surg* OR radiolog* OR "patient education")
AND PY=(2005-2026) AND LA=(English)
```

## Narrow "direct analogue" query (run this first; expect a handful)

Scopus
```
TITLE-ABS-KEY ( wikipedia AND ( chatgpt OR "generative AI" OR "large language model*" OR "AI overview*" ) AND ( pageview* OR "page view*" OR traffic OR readership OR visits OR engagement ) )
OR TITLE-ABS-KEY ( wikipedia AND ( pageview* OR "page view*" OR traffic ) AND ( exam* OR "academic calendar" OR "school year" OR semester OR seasonal* OR curriculum OR syllabus OR student* ) )
```
Web of Science
```
TS=(Wikipedia AND (ChatGPT OR "generative AI" OR "large language model*" OR "AI overview*") AND (pageview* OR "page view*" OR traffic OR readership OR visits OR engagement))
OR TS=(Wikipedia AND (pageview* OR "page view*" OR traffic) AND (exam* OR "academic calendar" OR "school year" OR semester OR seasonal* OR curriculum OR syllabus OR student*))
```

Notes
- Conference papers matter here (WWW/TheWebConf, ICWSM, CSCW, CHI, WSDM, OpenSym). In Scopus keep document types Article **and** Conference Paper; in WoS add the Conference Proceedings Citation Index if the institution's subscription includes it.
- For the newest work, re-run the arXiv strings in `search-protocol.md`; database indexing lags preprints by 6-18 months.
