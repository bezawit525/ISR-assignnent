# HW6 Report

## Overview
HW6 builds a **feature matrix** for learning-to-rank / ML experiments using retrieval model scores as features.

## Key files
- `Feature_Matrix.py`: builds features and labels from qrels + retrieval runfiles
- `ML_Learning Algorithms.py`: a starter ML script (lightweight)
- `iris.py`: unrelated/simple ML example
- `trec_eval.pl`: evaluation tool copy
- `totalTF.p`: serialized collection statistics

## Inputs
- Elasticsearch index (`index1`) for term vector statistics.
- Qrels file and multiple runfiles to extract scores.

## Outputs
- A feature matrix (typically written to CSV via `csv` module further in the script)

## Known issues / portability gaps
- Hard-coded stoplist path `/Users/Zion/Downloads/AP_DATA/stoplist.txt` inside `Feature_Matrix.py`.
- Strong coupling to Elasticsearch schemas and precomputed pickles.

## Cranfield usage
Cranfield can be used if you:
- Index Cranfield documents into Elasticsearch with compatible field names.
- Provide a qrels parser consistent with Cranfield’s 3-column format.
