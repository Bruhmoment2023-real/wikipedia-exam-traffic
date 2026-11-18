#!/bin/bash
# Downloads the 12 English clickstream monthly files named in PLAN-exploratory (sequential, resumable).
OUT=/d/Research-Publishing/05-wikipedia-exam-traffic/rework-v3/clickstream
for m in 2018-10 2019-02 2019-10 2020-02 2022-10 2023-02 2023-10 2024-02 2024-10 2025-02 2025-10 2026-02; do
  f=clickstream-enwiki-$m.tsv.gz
  curl -s -C - -A "WikiExamTraffic/0.2 (academic research on exam-season pageviews)" -o $OUT/$f https://dumps.wikimedia.org/other/clickstream/$m/$f
  echo "$m done $(stat -c %s $OUT/$f)"
  sleep 3
done
