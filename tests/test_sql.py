"""Tests for SQL query support."""

import pandas as pd
import pytest

from tablofy import TablofyFrame
from tablofy.core.errors import TablofyDataError


class TestSQL:
    @pytest.fixture
    def frame(self):
        return TablofyFrame(
            pd.DataFrame({
                "name": ["Alice", "Bob", "Charlie"],
                "sales": [100, 200, 150],
                "region": ["North", "South", "North"],
            }),
        )

    def test_select_all(self, frame):
        result = frame.sql("SELECT * FROM data")
        assert len(result) == 3

    def test_select_where(self, frame):
        result = frame.sql("SELECT * FROM data WHERE sales > 150")
        assert len(result) == 1

    def test_select_columns(self, frame):
        result = frame.sql("SELECT name FROM data")
        assert result.columns() == ["name"]

    def test_returns_tablofyframe(self, frame):
        result = frame.sql("SELECT * FROM data")
        assert isinstance(result, TablofyFrame)

    def test_group_by(self, frame):
        result = frame.sql(
            "SELECT region, SUM(sales) AS total_sales "
            "FROM data GROUP BY region ORDER BY region"
        )
        assert "region" in result.columns()
        assert "total_sales" in result.columns()
        assert len(result) == 2

    def test_order_by(self, frame):
        result = frame.sql("SELECT name FROM data ORDER BY sales DESC")
        assert result.to_pandas()["name"].iloc[0] == "Bob"
        assert result.to_pandas()["name"].iloc[2] == "Alice"

    def test_unsupported_statement_raises(self, frame):
        with pytest.raises(TablofyDataError):
            frame.sql("DROP TABLE data")

    def test_insert_raises(self, frame):
        with pytest.raises(TablofyDataError):
            frame.sql("INSERT INTO data VALUES ('Dan', 300)")

    def test_update_raises(self, frame):
        with pytest.raises(TablofyDataError):
            frame.sql("UPDATE data SET sales = 0 WHERE name = 'Alice'")

    def test_empty_query_raises(self, frame):
        with pytest.raises(TablofyDataError):
            frame.sql("")

    def test_invalid_syntax_raises(self, frame):
        with pytest.raises(TablofyDataError):
            frame.sql("SELECT FROM WHERE")

    def test_select_nonexistent_column_raises(self, frame):
        with pytest.raises(TablofyDataError):
            frame.sql("SELECT nonexistent FROM data")
