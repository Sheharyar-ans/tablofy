"""Tests for transform methods."""

import pandas as pd
import pytest

from tablofy import TablofyFrame
from tablofy.core.errors import TablofyColumnError, TablofyDataError, TablofyFileError


class TestSelect:
    @pytest.fixture
    def frame(self):
        return TablofyFrame(pd.DataFrame({
            "name": ["Alice", "Bob", "Charlie"],
            "age": [25, 30, 35],
            "salary": [50000, 60000, 70000],
            "region": ["North", "South", "North"],
        }))

    def test_select_returns_requested_columns(self, frame):
        result = frame.select("name", "age")
        assert result.columns() == ["name", "age"]

    def test_select_does_not_modify_original(self, frame):
        frame.select("name")
        assert frame.columns() == ["name", "age", "salary", "region"]

    def test_select_single_column(self, frame):
        result = frame.select("name")
        assert result.columns() == ["name"]
        assert len(result) == 3

    def test_select_missing_column_raises(self, frame):
        with pytest.raises(TablofyColumnError):
            frame.select("nonexistent")

    def test_select_empty_raises(self, frame):
        with pytest.raises(TablofyColumnError):
            frame.select()


class TestDrop:
    @pytest.fixture
    def frame(self):
        return TablofyFrame(pd.DataFrame({
            "name": ["Alice", "Bob"],
            "age": [25, 30],
            "salary": [50000, 60000],
        }))

    def test_drop_removes_column(self, frame):
        result = frame.drop("age")
        assert "age" not in result.columns()

    def test_drop_preserves_other_columns(self, frame):
        result = frame.drop("age")
        assert result.columns() == ["name", "salary"]

    def test_drop_does_not_modify_original(self, frame):
        frame.drop("age")
        assert "age" in frame.columns()

    def test_drop_missing_column_raises(self, frame):
        with pytest.raises(TablofyColumnError):
            frame.drop("nonexistent")


class TestRename:
    @pytest.fixture
    def frame(self):
        return TablofyFrame(pd.DataFrame({
            "name": ["Alice", "Bob"],
            "age": [25, 30],
        }))

    def test_rename_renames_column(self, frame):
        result = frame.rename({"name": "full_name"})
        assert "full_name" in result.columns()

    def test_rename_removes_old_name(self, frame):
        result = frame.rename({"name": "full_name"})
        assert "name" not in result.columns()

    def test_rename_does_not_modify_original(self, frame):
        frame.rename({"name": "full_name"})
        assert "name" in frame.columns()

    def test_rename_missing_column_raises(self, frame):
        with pytest.raises(TablofyColumnError):
            frame.rename({"nonexistent": "x"})

    def test_rename_empty_mapping_raises(self, frame):
        with pytest.raises(TablofyColumnError):
            frame.rename({})


class TestSort:
    @pytest.fixture
    def frame(self):
        return TablofyFrame(pd.DataFrame({
            "name": ["Charlie", "Alice", "Bob"],
            "age": [35, 25, 30],
            "salary": [70000, 50000, 60000],
        }))

    def test_sort_ascending(self, frame):
        result = frame.sort("age")
        assert result.to_pandas()["age"].iloc[0] == 25
        assert result.to_pandas()["age"].iloc[1] == 30
        assert result.to_pandas()["age"].iloc[2] == 35

    def test_sort_descending(self, frame):
        result = frame.sort("salary", descending=True)
        assert result.to_pandas()["salary"].iloc[0] == 70000
        assert result.to_pandas()["salary"].iloc[1] == 60000

    def test_sort_does_not_modify_original(self, frame):
        frame.sort("age")
        assert frame.to_pandas()["age"].iloc[0] == 35

    def test_sort_missing_column_raises(self, frame):
        with pytest.raises(TablofyColumnError):
            frame.sort("nonexistent")


class TestFilter:
    @pytest.fixture
    def frame(self):
        return TablofyFrame(pd.DataFrame({
            "name": ["Alice", "Bob", "Charlie"],
            "age": [25, 30, 35],
            "salary": [50000, 60000, 70000],
            "region": ["North", "South", "North"],
        }))

    def test_filter_valid_expression(self, frame):
        result = frame.filter("age > 25")
        assert len(result) == 2

    def test_filter_equal(self, frame):
        result = frame.filter("region == 'North'")
        assert len(result) == 2

    def test_filter_and_condition(self, frame):
        result = frame.filter("age > 25 and region == 'North'")
        assert len(result) == 1

    def test_filter_returns_new_frame(self, frame):
        result = frame.filter("age > 25")
        assert result is not frame

    def test_filter_invalid_column_raises(self, frame):
        with pytest.raises(TablofyColumnError):
            frame.filter("nonexistent > 25")

    def test_filter_empty_expression_raises(self, frame):
        with pytest.raises(TablofyDataError):
            frame.filter("")

    def test_filter_whitespace_expression_raises(self, frame):
        with pytest.raises(TablofyDataError):
            frame.filter("   ")


class TestGroup:
    @pytest.fixture
    def frame(self):
        return TablofyFrame(pd.DataFrame({
            "name": ["Alice", "Bob", "Charlie"],
            "age": [25, 30, 35],
            "salary": [50000, 60000, 70000],
            "region": ["North", "South", "North"],
        }))

    def test_group_sum(self, frame):
        result = frame.group("region").sum("salary")
        assert "region" in result.columns()
        assert "salary" in result.columns()

    def test_group_mean(self, frame):
        result = frame.group("region").mean("age")
        assert "region" in result.columns()
        assert "age" in result.columns()

    def test_group_sum_numeric_values(self, frame):
        result = frame.group("region").sum("salary")
        north = result.to_pandas().loc[result.to_pandas()["region"] == "North", "salary"]
        assert north.iloc[0] == 120000  # 50000 + 70000

    def test_group_mean_numeric_values(self, frame):
        result = frame.group("region").mean("age")
        north = result.to_pandas().loc[result.to_pandas()["region"] == "North", "age"]
        assert north.iloc[0] == 30.0  # (25 + 35) / 2

    def test_group_missing_column_raises(self, frame):
        with pytest.raises(TablofyColumnError):
            frame.group("nonexistent")


class TestPivot:
    @pytest.fixture
    def frame(self):
        return TablofyFrame(pd.DataFrame({
            "region": ["North", "North", "South", "South"],
            "year": [2020, 2021, 2020, 2021],
            "sales": [100, 200, 150, 250],
        }))

    def test_pivot_returns_frame(self, frame):
        result = frame.pivot(index="region", columns="year", values="sales")
        assert isinstance(result, TablofyFrame)

    def test_pivot_has_index_column(self, frame):
        result = frame.pivot(index="region", columns="year", values="sales")
        assert "region" in result.columns()

    def test_pivot_missing_index_raises(self, frame):
        with pytest.raises(TablofyColumnError):
            frame.pivot(index="nonexistent", columns="year", values="sales")

    def test_pivot_missing_columns_raises(self, frame):
        with pytest.raises(TablofyColumnError):
            frame.pivot(index="region", columns="nonexistent", values="sales")

    def test_pivot_missing_values_raises(self, frame):
        with pytest.raises(TablofyColumnError):
            frame.pivot(index="region", columns="year", values="nonexistent")


class TestJoin:
    @pytest.fixture
    def left(self):
        return TablofyFrame(pd.DataFrame({
            "id": [1, 2, 3],
            "name": ["Alice", "Bob", "Charlie"],
        }))

    @pytest.fixture
    def right(self):
        return TablofyFrame(pd.DataFrame({
            "id": [1, 2, 4],
            "salary": [50000, 60000, 80000],
        }))

    def test_join_inner(self, left, right):
        result = left.join(right, on="id", how="inner")
        assert "name" in result.columns()
        assert "salary" in result.columns()
        assert len(result) == 2  # only ids 1 and 2 match

    def test_join_left(self, left, right):
        result = left.join(right, on="id", how="left")
        assert len(result) == 3  # all left rows

    def test_join_right(self, left, right):
        result = left.join(right, on="id", how="right")
        assert len(result) == 3  # all right rows (1, 2, 4)

    def test_join_outer(self, left, right):
        result = left.join(right, on="id", how="outer")
        assert len(result) == 4  # union of both

    def test_join_missing_on_in_left_raises(self, left, right):
        with pytest.raises(TablofyColumnError):
            left.join(right, on="nonexistent")

    def test_join_missing_on_in_right_raises(self, left, right):
        bad_right = TablofyFrame(pd.DataFrame({"x": [1]}))
        with pytest.raises(TablofyColumnError):
            left.join(bad_right, on="id")


class TestExport:
    @pytest.fixture
    def frame(self):
        return TablofyFrame(pd.DataFrame({
            "name": ["Alice", "Bob"],
            "age": [25, 30],
        }))

    def test_export_csv(self, frame, tmp_path):
        path = tmp_path / "test.csv"
        frame.export(str(path))
        assert path.exists()
        content = path.read_text(encoding="utf-8")
        assert "name" in content
        assert "Alice" in content

    def test_export_xlsx(self, frame, tmp_path):
        path = tmp_path / "test.xlsx"
        frame.export(str(path))
        assert path.exists()

    def test_export_json(self, frame, tmp_path):
        path = tmp_path / "test.json"
        frame.export(str(path))
        assert path.exists()
        content = path.read_text(encoding="utf-8")
        assert "Alice" in content

    def test_export_parquet(self, frame, tmp_path):
        path = tmp_path / "test.parquet"
        frame.export(str(path))
        assert path.exists()

    def test_export_unsupported_format_raises(self, frame, tmp_path):
        path = tmp_path / "test.txt"
        with pytest.raises(TablofyFileError):
            frame.export(str(path))
