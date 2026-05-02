# HW4 Report

## Overview
HW4 implements link analysis algorithms:
- **PageRank** (`PageRank.py`)
- **HITS** (`HITS.py`)

These operate on a link graph (inlinks/outlinks) rather than a text qrels benchmark.

## Algorithms
- **PageRank**
  - Uses damping factor `d = 0.85`
  - Iterates until perplexity converges (4 consecutive iterations with change < 1)
  - Requires an inlinks file such as `wt2g_inlinks.txt`

- **HITS**
  - Builds a root set via an Elasticsearch query against a crawl index (`hw3_crawl`)
  - Expands to a base set using outlinks and `linkgraph.txt`
  - Iterates hub/authority updates (details continue later in file)

## Inputs
- `wt2g_inlinks.txt` (for PageRank)
- `linkgraph.txt` plus an Elasticsearch index named `hw3_crawl` (for HITS)

## Outputs
- PageRank ranks written to `wt2g_rank.txt`
- HITS typically writes top hubs/authorities (depending on the remainder of the script)

## Known issues / portability gaps
- Missing required data files in the repo root for direct execution (e.g., `wt2g_inlinks.txt`, `linkgraph.txt`).
- `HITS.py` depends on Elasticsearch and a specific crawl index.

## Notes
Cranfield is **not applicable** to HW4 directly, because it is not a link graph dataset.
