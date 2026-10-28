import pandas as pd

from src.reconcile import reconcile


def test_detects_missing_and_mismatched_rows():
    left = pd.DataFrame({"id": [1, 2, 3], "amount": [100, 200, 300]})
    right = pd.DataFrame({"id": [1, 2, 4], "amount": [100, 250, 400]})

    result = reconcile(left, right, key="id")

    assert result["missing_in_right"] == [3]
    assert result["missing_in_left"] == [4]
    assert len(result["mismatched"]) == 1
    assert result["mismatched"][0]["key"] == 2
    assert result["mismatched"][0]["column"] == "amount"


def test_identical_data_has_no_issues():
    df = pd.DataFrame({"id": [1, 2], "amount": [10, 20]})

    result = reconcile(df, df.copy(), key="id")

    assert result["missing_in_right"] == []
    assert result["missing_in_left"] == []
    assert result["mismatched"] == []
