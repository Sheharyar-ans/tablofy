"""Tests for exploration methods."""

import pandas as pd
import pytest

from tablofy import TablofyFrame


@pytest.fixture
def frame():
    return TablofyFrame(
        pd.DataFrame({
            "name": ["Alice", "Bob", "Charlie"],
            "age": [25, 30, None],
            "salary": [50000.0, 60000.0, 70000.0],
            "department": ["Sales", "Eng", "Sales"],
            "start_date": pd.to_datetime(["2020-01-15", "2019-06-01", "2021-03-20"]),
            "active": [True, False, True],
        }),
        name="employees",
    )


class TestPreview:
    def test_preview_default(self, frame):
        result = frame.preview()
        assert len(result) == 3

    def test_preview_with_n(self, frame):
        result = frame.preview(1)
        assert len(result) == 1

    def test_head_alias(self, frame):
        result = frame.head(2)
        assert len(result) == 2


class TestShape:
    def test_shape_counts(self, frame):
        s = frame.shape()
        assert s["rows"] == 3
        assert s["columns"] == 6


class TestColumns:
    def test_columns_list(self, frame):
        cols = frame.columns()
        assert isinstance(cols, list)
        assert "name" in cols
        assert len(cols) == 6


class TestTypes:
    def test_types_columns(self, frame):
        t = frame.types()
        assert list(t.columns) == ["column", "dtype", "non_null", "nulls", "null_pct"]

    def test_types_content(self, frame):
        t = frame.types()
        row = t[t["column"] == "age"].iloc[0]
        assert row["dtype"] == "float64"
        assert row["nulls"] == 1
        assert row["non_null"] == 2
        assert row["null_pct"] == pytest.approx(33.33, rel=0.01)

    def test_types_mixed_dtypes(self, frame):
        t = frame.types()
        dtypes = dict(zip(t["column"], t["dtype"]))
        assert dtypes["name"] == "object"
        assert dtypes["salary"] == "float64"
        assert dtypes["active"] == "bool"
        assert "datetime64" in dtypes["start_date"]


class TestMissing:
    def test_missing_columns(self, frame):
        m = frame.missing()
        assert list(m.columns) == ["column", "missing", "percent"]

    def test_missing_only_nonzero(self, frame):
        m = frame.missing()
        assert len(m) == 1
        assert m.iloc[0]["column"] == "age"
        assert m.iloc[0]["missing"] == 1

    def test_missing_empty_when_no_nulls(self):
        clean = TablofyFrame(pd.DataFrame({"x": [1, 2], "y": [3, 4]}))
        m = clean.missing()
        assert len(m) == 0


class TestDuplicates:
    def test_no_duplicates(self, frame):
        d = frame.duplicates()
        assert d["count"] == 0
        assert d["percent"] == 0.0

    def test_with_duplicates(self):
        df = TablofyFrame(pd.DataFrame({"a": [1, 1, 2]}))
        d = df.duplicates()
        assert d["count"] == 1
        assert d["percent"] == pytest.approx(33.33, rel=0.01)


class TestSummary:
    def test_summary_returns_dataframe(self, frame):
        s = frame.summary()
        assert isinstance(s, pd.DataFrame)

    def test_summary_includes_numeric(self, frame):
        s = frame.summary()
        assert "age" in s.columns
        assert "salary" in s.columns

    def test_summary_columns(self, frame):
        s = frame.summary()
        assert "mean" in s.index
        assert "std" in s.index


class TestProfile:
    def test_profile_keys(self, frame):
        p = frame.profile()
        assert p["rows"] == 3
        assert p["columns"] == 6
        assert p["total_cells"] == 18
        assert p["missing_cells"] == 1
        assert p["missing_percent"] == pytest.approx(5.56, rel=0.01)
        assert p["duplicate_rows"] == 0
        assert isinstance(p["memory_usage"], int)

    def test_profile_column_lists(self, frame):
        p = frame.profile()
        assert "age" in p["numeric_columns"]
        assert "salary" in p["numeric_columns"]
        assert "name" in p["text_columns"]
        assert "start_date" in p["date_columns"]
        assert "active" in p["categorical_columns"]
        assert "department" in p["text_columns"]
