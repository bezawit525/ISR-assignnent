# HW2 Report

## Overview
HW2 replaces the Elasticsearch dependency from HW1 with a **self-designed inverted index** stored on disk. It supports both:
- **Unstemmed** indexing (with stopword removal)
- **Stemmed** indexing (with stopword removal)

It also adds a **proximity-based retrieval model**.

## Components
- **Indexers**
  - `Unstemmed_With_Stopwords_Index-1.py`
  - `Stemmed_Stopwords_Removed_Index-1.py`
- **Query processing**
  - `Query_Processing.py`, plus stemmed/proximity variants
- **Retrieval models**
  - `Retrieval_Models.py`, plus stemmed variant

## Index format (as implemented)
The index is written as text blocks with:
- Term id
- DF
- TTF
- A postings list of `(docid, tf, positions...)`

A separate **catalog** file stores offsets/lengths to enable random access into the inverted file.

## Dataset
- **Assignment dataset**: AP89 (as referenced by the original student paths).
- **Practice dataset in this repo**: Cranfield under `datasets/cran/`.

## Execution process (intended)
1. Run one of the indexers to build the inverted file and catalog.
2. Run a query processing script to materialize per-query `termVector`/`termStats` pickles.
3. Run `Retrieval_Models.py` to produce runfiles.
4. Evaluate with qrels.

## Cranfield end-to-end run (implemented in this repo)
To make HW2 runnable end-to-end on the included Cranfield dataset, an additional runner script was added:

- `HW2/cranfield_end_to_end.py`

It:
- Parses `datasets/cran/cran.all.1400` and `datasets/cran/cran.qry`
- Builds an in-memory inverted index
- Produces TREC-format runfiles under `HW2/cranfield_runs/` for:
  - Okapi TF (`cran_okapi_tf.run`)
  - BM25 (`cran_bm25.run`)
  - Unigram LM Laplace (`cran_lm_laplace.run`)

Commands used:

```bash
python HW2/cranfield_end_to_end.py
python HW5/Trec_Eval.py datasets/cran/cranqrel HW2/cranfield_runs/cran_okapi_tf.run
python HW5/Trec_Eval.py datasets/cran/cranqrel HW2/cranfield_runs/cran_bm25.run
python HW5/Trec_Eval.py datasets/cran/cranqrel HW2/cranfield_runs/cran_lm_laplace.run
```

## Cranfield evaluation results (binary relevance: grade > 0)
Evaluator: `HW5/Trec_Eval.py` treating any positive Cranfield grade as relevant.

### BM25 (`cran_bm25.run`)
- Average Precision: **0.0098**
- R-precision: **0.0072**
- Mean Precision@5: **0.0064**
- Mean Precision@10: **0.0085**
- Mean Precision@20: **0.0080**
- Mean Precision@50: **0.0066**
- Mean Recall@100: **0.0723**

### Okapi TF (`cran_okapi_tf.run`)
- Average Precision: **0.0086**
- R-precision: **0.0048**
- nDCG: **0.1697**
- Mean Precision@10: **0.0064**
- Mean Recall@100: **0.0730**

### LM Laplace (`cran_lm_laplace.run`)
- Average Precision: **0.0084**
- R-precision: **0.0048**
- nDCG: **0.1877**
- Mean Precision@10: **0.0053**
- Mean Recall@100: **0.0600**

## Known issues / fixes required to execute on this repo
- **Hard-coded AP89 + macOS paths** in indexers and query scripts.
- **Python 2 style** prints in the indexers.
- Query scripts reference `QueryUpdated.txt` which is not part of this folder by default.
- Module import names include `-1` in filenames (not importable as Python modules).

## Outputs
- `Files/Unstemmed/*.txt` and `Files/Stemmed/*.txt`
- Runfiles for Okapi TF/BM25/LM/proximity depending on which functions are enabled.

## Evaluation with Cranfield
Cranfield qrels are graded (codes 1–4), and there are occasional negative codes in the provided file. For binary metrics (MAP/P@k), you should decide a threshold (commonly treat 1–4 as relevant, ignore negatives).
