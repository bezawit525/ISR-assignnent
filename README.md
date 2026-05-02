# Information Retrieval Assignments (HW1–HW8)

This repository contains a set of Information Retrieval homework implementations organized by folder. Each homework is a separate mini-project (not a single deployable application).

## Group members (Section 1)
- Bezawit Hayalu  UGR/5778/17
- Eyael Gebrewahd UGR/1353/17
- Daniel Hirpa    UGR/3745/17
- Eden Brhane     UGR/6797/17 
- Abigia Getu     UGR/7827/17

## Repository structure

- `HW1/`: Retrieval models implemented using Elasticsearch statistics.
- `HW2/`: Disk-based inverted index (stemmed/unstemmed) + proximity retrieval.
- `HW4/`: Link analysis (PageRank, HITS).
- `HW5/`: Evaluation utilities (custom TREC-style evaluator).
- `HW6/`: Feature matrix + ML scripts (learning-to-rank style experiments).
- `HW7/`: Spam filtering / email processing pipeline.
- `HW8/`: Clustering / topic modeling scripts.

Each homework folder contains a `report.md` summarizing:
- Models/algorithms used
- Datasets
- Execution expectations
- Known issues and portability notes

## Reports

- `HW1/report.md`
- `HW2/report.md`
- `HW4/report.md`
- `HW5/report.md`
- `HW6/report.md`
- `HW7/report.md`
- `HW8/report.md`

There are also legacy/manual documents under `manual reports/` (mostly HW1 and HW2) that provide narrative writeups and “improved” script variants.

## Practice dataset included: Cranfield

For practicing indexing/querying/evaluation without downloading AP89, this repo includes the Cranfield collection:

- `datasets/cran/cran.all.1400` (documents)
- `datasets/cran/cran.qry` (queries)
- `datasets/cran/cranqrel` (relevance judgements)
- `datasets/cran/cranqrel.readme` (explains Cleverdon relevance codes)

The Cranfield qrels file uses three columns:

```text
<query_id> <doc_id> <relevance_code>
```

The relevance codes are defined by Cleverdon (see `cranqrel.readme`).

## Fixes applied in this repo

- `HW7/EmailFilter.py`
  - Removed hard-coded absolute dataset paths.
  - Added environment-driven configuration (`TREC07P_DATA_DIR`, `TREC07P_INDEX_FILE`).
  - Added an `if __name__ == "__main__":` guard to prevent execution on import.

## Notes about running the HWs

- Some HWs require **external datasets** not included here (e.g., AP89 for HW1/HW2/HW8, a link graph for HW4, TREC spam for HW7).
- Some HWs require **Elasticsearch** and specific indices/mappings (notably HW1, HW4 HITS, HW6).
- Several scripts in the HW folders still contain hard-coded paths from the original author environment; consult each `HWx/report.md` for what needs to be parameterized.

---

# HW1 assignment reference (original description)

Implement and compare various retrieval systems using vector space models and language models.

This assignment introduces Elasticsearch. It involves writing:

1. A program to parse the corpus and index it with Elasticsearch.
2. A query processor to run queries using a selected retrieval model.

## Getting Started

- Download and install Elasticsearch and Kibana.
- Download AP89 data: http://dragon.ischool.drexel.edu/example/ap89_collection.zip

## Evaluation

Use `trec_eval`:

```bash
trec_eval [-q] qrel_file results_file
```
