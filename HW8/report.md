# HW8 Report

## Overview
HW8 contains clustering/partitioning scripts. `clustering.py` in particular runs topic modeling (LDA) over sets of documents.

## Key files
- `clustering.py`: builds topic models (LDA) using scikit-learn.
- `partition.py`: additional clustering/partition logic (not reviewed in depth here).

## Inputs (as currently coded)
- Results file: `OkapiBM25_Results_File.txt`
- Qrels file: `qrels.adhoc.51-100.AP89.txt`
- AP89 corpus under `AP_DATA/ap89_collection/`
- Stoplist file at `AP_DATA/stoplist.txt`

## Outputs
- Topic descriptions written under:
  - `partA_topics/query<qid>.txt`
  - `partA_docs/query<qid>.txt`

## Known issues / portability gaps
- Hard-coded AP89 paths (`AP_DATA/...`) and interactive `input()` calls in `getDocText`.
- Logic bug: `elif 'QREL':` in `buildTopDocs` is always truthy; it should check `model == 'QREL'`.

## Cranfield usage
Cranfield could be used if you adapt `getDocText` to read from `datasets/cran/cran.all.1400` and adjust qrels parsing.
