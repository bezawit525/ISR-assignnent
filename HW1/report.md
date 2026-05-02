# HW1 Report

## Overview
HW1 implements and compares multiple classical Information Retrieval (IR) retrieval models (vector space and language modeling) over a TREC-style news corpus (originally AP89), with indexing and statistics obtained from Elasticsearch.

## Implemented models
- **ES built-in** (baseline `match` query)
- **Okapi TF**
- **TF-IDF**
- **Okapi BM25**
- **Unigram LM (Laplace smoothing)**
- **Unigram LM (Jelinek–Mercer smoothing)**

## Dataset
- **Primary (per assignment)**: AP89 collection (TREC format documents with `<DOC>`, `<DOCNO>`, `<TEXT>`)
- **Practice dataset in this repo**: Cranfield
  - `datasets/cran/cran.all.1400` (documents)
  - `datasets/cran/cran.qry` (queries)
  - `datasets/cran/cranqrel` (qrels; 3 columns with graded relevance codes)

## Execution process (intended)
1. **Index documents into Elasticsearch**.
2. **Process queries** from the query file.
3. **Compute ranking scores** using the retrieval model implementations.
4. **Write run files** in TREC format:
   - `<query-id> Q0 <docno> <rank> <score> Exp`
5. **Evaluate** with `trec_eval` or with the project’s evaluation script(s).

## Notes from manual reports
A detailed narrative report exists at:
- `manual reports/HW1/README.md.txt`

That manual report describes:
- Architecture overview
- Model descriptions
- TREC output format
- Evaluation with `trec_eval`

## Known issues / portability gaps in current code
- **Hard-coded absolute dataset paths** appear in several scripts across HWs (e.g., `/Users/Zion/...`).
- HW1 in this repo expects **Elasticsearch running locally** and correct index mappings.
- Some scripts reference helper files like `QueryUpdated.txt` which may not exist in every folder.

## Outputs
Expected outputs are model-specific runfiles (e.g., BM25 results file) suitable for evaluation.

## Evaluation
- Standard tools: `trec_eval` on qrels + runfile.
- Metrics typically reported: **MAP**, **P@k**, **R-Precision**, **nDCG**.

## Reproducibility checklist
- Elasticsearch installed and running
- Python dependencies installed (`elasticsearch`, `elasticsearch-dsl`, `bs4`, etc.)
- Corpus and query files placed where the scripts expect them (or script paths updated)
