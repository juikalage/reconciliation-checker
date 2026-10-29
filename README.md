# Reconciliation Checker

A Python tool that compares two CSV or Excel files on a shared key column. It reports rows that are missing from either file and rows where a value differs, then writes the differences to a CSV report.

## Features

- Loads CSV and Excel (`.xlsx`, `.xls`) files
- Finds keys present in one file but not the other
- Finds value mismatches for matching keys, column by column
- Writes a report with one row per issue
- Unit tests with pytest, run automatically on GitHub Actions

## Project structure
src/
reconcile.py # load, compare, and report functions
config.py # default settings
tests/
test_reconcile.py
test_config.py
sample_data/ # example input files

## How it works

1. `load_table` reads each file into a pandas DataFrame.
2. `reconcile` compares the two tables on the key column. It finds missing keys with set differences, then merges the shared rows to compare values.
3. `write_report` saves the results to a CSV file.

## Run the tests

```bash
python -m pip install -r requirements.txt
python -m pytest
```

## Status

Core comparison logic and tests are complete. A command-line interface is planned next.
