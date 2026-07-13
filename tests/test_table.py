"""Tests for TablofyFrame construction and properties."""

import pandas as pd
import pytest

from tablofy import TablofyFrame
from tablofy.core.errors import TablofyDataError


class TestConstruction:
    def test_from_dataframe(self):
        df = pd.DataFrame({"a": [1]})
        frame = TablofyFrame(df, name="test")
        assert frame.name == "test"

    def test_empty_dataframe_raises(self):
        with pytest.raises(TablofyDataError):
            TablofyFrame(pd.DataFrame())

    def test_default_name(self):
        frame = TablofyFrame(pd.DataFrame({"x": [1]}))
        assert frame.name == "Data"

    def test_to_pandas_returns_dataframe(self):
        df = pd.DataFrame({"a": [1, 2]})
        frame = TablofyFrame(df)
        result = frame.to_pandas()
        assert isinstance(result, pd.DataFrame)
        assert list(result.columns) == ["a"]

    def test_dtypes_property(self):
        frame = TablofyFrame(pd.DataFrame({"a": [1], "b": ["x"]}))
        d = frame.dtypes
        assert isinstance(d, dict)
        assert d["a"] == "int64"
        assert d["b"] == "object"

    def test_size_property(self):
        frame = TablofyFrame(pd.DataFrame({"a": [1, 2, 3]}))
        assert frame.size == 3

    def test_size_with_multiple_columns(self):
        frame = TablofyFrame(pd.DataFrame({"a": [1, 2], "b": [3, 4]}))
        assert frame.size == 4

    def test_stats_property(self):
        frame = TablofyFrame(pd.DataFrame({"x": [1.0, 2.0, 3.0]}))
        s = frame.stats
        from tablofy.analytics.stats import Stats
        assert isinstance(s, Stats)

    def test_repr(self):
        frame = TablofyFrame(pd.DataFrame({"a": [1]}), name="test")
        assert repr(frame) == "<TablofyFrame 'test' shape=(1, 1)>"

    def test_len(self):
        frame = TablofyFrame(pd.DataFrame({"a": [1, 2, 3]}))
        assert len(frame) == 3

    def test_last_clean_actions_default(self):
        frame = TablofyFrame(pd.DataFrame({"x": [1]}))
        assert frame._last_clean_actions == []
