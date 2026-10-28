"""Compare two datasets on a key column and report mismatches."""

import pandas as pd


def load_table(path: str) -> pd.DataFrame:
    """Load a CSV or Excel file into a DataFrame."""
    if path.lower().endswith(".csv"):
        return pd.read_csv(path)
    if path.lower().endswith((".xlsx", ".xls")):
        return pd.read_excel(path)
    raise ValueError(f"Unsupported file type: {path}")


def reconcile(left: pd.DataFrame, right: pd.DataFrame, key: str) -> dict:
    """Compare two DataFrames on a key column.

    Returns a dict with:
      - missing_in_right: keys present in left only
      - missing_in_left: keys present in right only
      - mismatched: rows where a shared key has different values
    """
    left_keys = set(left[key])
    right_keys = set(right[key])

    missing_in_right = sorted(left_keys - right_keys)
    missing_in_left = sorted(right_keys - left_keys)

    shared = left.merge(right, on=key, suffixes=("_left", "_right"))
    value_cols = [c for c in left.columns if c != key and c in right.columns]

    mismatched_rows = []
    for _, row in shared.iterrows():
        for col in value_cols:
            lv, rv = row[f"{col}_left"], row[f"{col}_right"]
            if pd.isna(lv) and pd.isna(rv):
                continue
            if lv != rv:
                mismatched_rows.append(
                    {"key": row[key], "column": col, "left": lv, "right": rv}
                )

    return {
        "missing_in_right": missing_in_right,
        "missing_in_left": missing_in_left,
        "mismatched": mismatched_rows,
    }


def write_report(result: dict, path: str) -> None:
    """Write the reconciliation result to a CSV report."""
    rows = []
    for k in result["missing_in_right"]:
        rows.append({"key": k, "issue": "missing in right", "column": "", "left": "", "right": ""})
    for k in result["missing_in_left"]:
        rows.append({"key": k, "issue": "missing in left", "column": "", "left": "", "right": ""})
    for m in result["mismatched"]:
        rows.append({"key": m["key"], "issue": "value mismatch", "column": m["column"],
                     "left": m["left"], "right": m["right"]})
    pd.DataFrame(rows, columns=["key", "issue", "column", "left", "right"]).to_csv(path, index=False)
