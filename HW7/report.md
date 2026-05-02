# HW7 Report

## Overview
HW7 is focused on **email spam filtering / classification** using the TREC 2007 spam corpus (trec07p). It includes scripts to:
- Parse raw emails
- Extract text content
- Build an index / feature representation
- Train or evaluate ML models

## Key files
- `EmailFilter.py`: converts raw emails into simplified `<TEXT>` files with labels.
- `Indexer.py`, `FeatureMatrix.py`, `MachineLeaning.py`, `ML-GIVEN.py`, `Tagger.py`, `doc-term.py`: additional steps in the pipeline.

## Fix applied in this repo
- `HW7/EmailFilter.py`
  - Removed hard-coded absolute paths.
  - Added environment-variable based configuration for dataset locations.
  - Added `__main__` guard so importing the module does not immediately run.

## Inputs
- TREC 2007 spam dataset directory (emails) and its label index file.

## Outputs
- `HW7/Files/<email_id>.txt` containing:
  - `<EMAILID>`
  - `<TEXT>`
  - `<LABEL>`

## Cranfield usage
Cranfield is **not directly applicable** to HW7; the HW is based on a labeled email dataset.
