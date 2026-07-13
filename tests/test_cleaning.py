"""Tests for cleaning methods."""

import pandas as pd

from tablofy import TablofyFrame


class TestCleanReturnsSelf:
    def test_clean_returns_self(self):
        frame = TablofyFrame(pd.DataFrame({"x": [1, 2]}))
        result = frame.clean()
        assert result is frame


class TestCleanDuplicates:
    def test_removes_duplicates(self):
        frame = TablofyFrame(pd.DataFrame({"a": [1, 1, 2]}))
        frame.clean()
        assert len(frame) == 2

    def test_no_duplicates_unchanged(self):
        frame = TablofyFrame(pd.DataFrame({"a": [1, 2, 3]}))
        frame.clean()
        assert len(frame) == 3

    def test_duplicates_disabled(self):
        frame = TablofyFrame(pd.DataFrame({"a": [1, 1, 2]}))
        frame.clean(duplicates=False)
        assert len(frame) == 3


class TestCleanEmptyColumns:
    def test_removes_fully_empty_columns(self):
        frame = TablofyFrame(pd.DataFrame({
            "a": [1, 2, 3],
            "b": [None, None, None],
            "c": ["x", "y", "z"],
        }))
        frame.clean()
        assert "b" not in frame.columns()

    def test_preserves_partial_nulls(self):
        frame = TablofyFrame(pd.DataFrame({
            "a": [1, None, 3],
            "b": ["x", "y", None],
        }))
        frame.clean()
        assert "a" in frame.columns()
        assert "b" in frame.columns()


class TestCleanColumnNames:
    def test_snake_case_conversion(self):
        frame = TablofyFrame(pd.DataFrame({
            "First Name": ["Alice"],
            "AGE ": [25],
            "SALARY ": [50000],
        }))
        frame.clean()
        cols = frame.columns()
        assert "first_name" in cols
        assert "age" in cols
        assert "salary" in cols

    def test_column_names_disabled(self):
        frame = TablofyFrame(pd.DataFrame({"First Name": ["Alice"]}))
        frame.clean(columns=False)
        assert "First Name" in frame.columns()


class TestCleanTextWhitespace:
    def test_strips_whitespace(self):
        frame = TablofyFrame(pd.DataFrame({
            "name": ["  Alice  ", "  Bob  "],
        }))
        frame.clean()
        assert frame.to_pandas()["name"].iloc[0] == "Alice"
        assert frame.to_pandas()["name"].iloc[1] == "Bob"

    def test_text_disabled(self):
        frame = TablofyFrame(pd.DataFrame({
            "name": ["  Alice  "],
        }))
        frame.clean(text=False)
        assert frame.to_pandas()["name"].iloc[0] == "  Alice  "


class TestCleanMissingValues:
    def test_numeric_smart_fill(self):
        frame = TablofyFrame(pd.DataFrame({
            "age": [20, None, 30],
        }))
        frame.clean()
        assert pd.notna(frame.to_pandas()["age"].iloc[1])

    def test_text_smart_fill(self):
        frame = TablofyFrame(pd.DataFrame({
            "name": ["Alice", None, "Bob", "Bob"],
        }))
        frame.clean()
        assert pd.notna(frame.to_pandas()["name"].iloc[1])

    def test_missing_off_skips_fill(self):
        frame = TablofyFrame(pd.DataFrame({
            "age": [20, None, 30],
        }))
        frame.clean(missing="off")
        assert pd.isna(frame.to_pandas()["age"].iloc[1])

    def test_explicit_dict_fill(self):
        frame = TablofyFrame(pd.DataFrame({
            "age": [20, None, 30],
        }))
        frame.clean(missing={"age": 99})
        assert frame.to_pandas()["age"].iloc[1] == 99


class TestCleanDateParsing:
    def test_parses_date_columns(self):
        frame = TablofyFrame(pd.DataFrame({
            "date": ["2020-01-15", "2019-06-01", "2021-03-20"],
        }))
        frame.clean()
        assert "datetime64" in str(frame.to_pandas()["date"].dtype)

    def test_handles_mixed_dates_gracefully(self):
        frame = TablofyFrame(pd.DataFrame({
            "date": ["2020-01-15", "not-a-date", "2021-03-20"],
        }))
        frame.clean()
        col = frame.to_pandas()["date"]
        assert col.iloc[1] == "not-a-date"

    def test_numeric_column_untouched(self):
        frame = TablofyFrame(pd.DataFrame({
            "price": [10, 20, 30],
        }))
        frame.clean()
        assert frame.to_pandas()["price"].dtype != "datetime64[ns]"


class TestCleanReport:
    def test_clean_report_returns_dict(self):
        frame = TablofyFrame(pd.DataFrame({"x": [1, 2]}))
        frame.clean()
        report = frame.clean_report()
        assert isinstance(report, dict)

    def test_clean_report_has_action_count(self):
        frame = TablofyFrame(pd.DataFrame({"x": [1, 2]}))
        frame.clean()
        report = frame.clean_report()
        assert "action_count" in report

    def test_clean_report_records_actions(self):
        frame = TablofyFrame(pd.DataFrame({
            "  Name  ": ["  Alice  ", "  Bob  "],
            "AGE ": [25, 30],
        }))
        frame.clean()
        report = frame.clean_report()
        assert report["action_count"] > 0
        assert len(report["actions"]) > 0

    def test_clean_report_summary_text(self):
        frame = TablofyFrame(pd.DataFrame({"x": [1, 2]}))
        frame.clean()
        report = frame.clean_report()
        assert "summary_text" in report
        assert isinstance(report["summary_text"], str)

    def test_clean_report_empty_when_no_clean(self):
        frame = TablofyFrame(pd.DataFrame({"x": [1, 2]}))
        report = frame.clean_report()
        assert report["action_count"] == 0

    def test_clean_report_after_multiple_cleans(self):
        frame = TablofyFrame(pd.DataFrame({
            "  Name  ": ["  Alice  "],
            "AGE ": [25],
        }))
        frame.clean()
        first = frame.clean_report()["action_count"]
        assert first > 0
        frame.clean()
        second = frame.clean_report()["action_count"]
        assert second >= 0
