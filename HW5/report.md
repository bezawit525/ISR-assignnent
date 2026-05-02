# HW5 Report

## Overview
HW5 contains scripts for evaluation and preparation of TREC-style runfiles, plus spreadsheet artifacts used for plots.

## Files
- `Trec_Prep.py`: prepares runfiles / intermediate formatting (repository-specific).
- `Trec_Eval.py`: a custom evaluator computing:
  - **Average Precision (AP / MAP)**
  - **R-Precision**
  - **nDCG**
  - **Precision@k / Recall@k / F1@k** for `k = 5,10,20,50,100`
- `Graphs.xlsx`, `Precision-Recall.xlsx`: output/plot artifacts.

## Inputs
- A runfile in TREC format:
  - `<qid> Q0 <docid> <rank> <score> Exp`
- A qrels file.

## Important note about qrels parsing
`Trec_Eval.py` was updated to support both:

- 4-column TREC qrels (common): `<qid> 0 <docid> <rel>`
- 3-column Cranfield qrels: `<qid> <docid> <grade>`

For Cranfield, the evaluator treats **any positive grade** as relevant (and ignores 0/negative).

`Trec_Eval.py` was also updated to accept direct CLI invocation:

```bash
python HW5/Trec_Eval.py <qrels> <runfile>
python HW5/Trec_Eval.py -q <qrels> <runfile>
```

This enables Cranfield end-to-end evaluation with `datasets/cran/cranqrel`.

## Cranfield evaluation (runs produced by HW2)

Runfiles:
- `HW2/cranfield_runs/cran_okapi_tf.run`
- `HW2/cranfield_runs/cran_bm25.run`
- `HW2/cranfield_runs/cran_lm_laplace.run`

Results (binary relevance: grade > 0):

- **BM25**: AP **0.0098**, R-Prec **0.0072**
- **Okapi TF**: AP **0.0086**, R-Prec **0.0048**, nDCG **0.1697**
- **LM Laplace**: AP **0.0084**, R-Prec **0.0048**, nDCG **0.1877**

## Outputs
- Summary metrics printed to stdout.
- Per-document details written to `details.txt`.
