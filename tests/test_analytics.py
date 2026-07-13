"""Tests for analytics: insights and statistics."""

import pandas as pd
import pytest

from tablofy import TablofyFrame
from tablofy.core.errors import TablofyColumnError


class TestInsights:
    @pytest.fixture
    def frame(self):
        return TablofyFrame(
            pd.DataFrame({
                "sales": [100, 200, 150, 300, 9999],
                "profit": [30, 50, 40, 80, 120],
            }),
        )

    def test_insights_returns_list(self, frame):
        result = frame.insights()
        assert isinstance(result, list)

    def test_insights_not_empty(self, frame):
        result = frame.insights()
        assert len(result) > 0

    def test_insights_all_strings(self, frame):
        result = frame.insights()
        assert all(isinstance(s, str) for s in result)

    def test_insights_mentions_rows_and_columns(self, frame):
        result = frame.insights()
        assert any("rows" in s and "columns" in s for s in result)

    def test_insights_mentions_no_missing(self, frame):
        result = frame.insights()
        assert any("No missing" in s for s in result)

    def test_insights_mentions_no_duplicates(self, frame):
        result = frame.insights()
        assert any("duplicate" in s for s in result)

    def test_insights_with_missing_values(self):
        frame = TablofyFrame(pd.DataFrame({
            "a": [1, None, 3],
            "b": ["x", None, None],
        }))
        result = frame.insights()
        assert any("missing" in s.lower() for s in result)

    def test_insights_with_duplicates(self):
        frame = TablofyFrame(pd.DataFrame({
            "a": [1, 1, 2],
            "b": [10, 10, 20],
        }))
        result = frame.insights()
        assert any("duplicate" in s.lower() for s in result)


class TestStatsDescribe:
    @pytest.fixture
    def frame(self):
        return TablofyFrame(pd.DataFrame({
            "sales": [100, 200, 150, 300, 9999],
            "profit": [30, 50, 40, 80, 120],
        }))

    def test_describe_returns_dataframe(self, frame):
        result = frame.stats.describe()
        assert isinstance(result, pd.DataFrame)

    def test_describe_has_count(self, frame):
        result = frame.stats.describe()
        assert "count" in result.index


class TestStatsCorrelation:
    @pytest.fixture
    def frame(self):
        return TablofyFrame(pd.DataFrame({
            "sales": [100, 200, 150, 300, 9999],
            "profit": [30, 50, 40, 80, 120],
        }))

    def test_correlation_returns_dataframe(self, frame):
        result = frame.stats.correlation()
        assert isinstance(result, pd.DataFrame)

    def test_correlation_square(self, frame):
        result = frame.stats.correlation()
        assert result.shape[0] == result.shape[1]


class TestStatsCovariance:
    @pytest.fixture
    def frame(self):
        return TablofyFrame(pd.DataFrame({
            "sales": [100, 200, 150, 300, 9999],
            "profit": [30, 50, 40, 80, 120],
        }))

    def test_covariance_returns_dataframe(self, frame):
        result = frame.stats.covariance()
        assert isinstance(result, pd.DataFrame)

    def test_covariance_square(self, frame):
        result = frame.stats.covariance()
        assert result.shape[0] == result.shape[1]


class TestStatsOutliers:
    @pytest.fixture
    def frame(self):
        return TablofyFrame(pd.DataFrame({
            "sales": [100, 200, 150, 300, 9999],
            "profit": [30, 50, 40, 80, 120],
        }))

    def test_outliers_dataframe(self, frame):
        result = frame.stats.outliers("sales")
        assert isinstance(result, pd.DataFrame)

    def test_outliers_indices(self, frame):
        result = frame.stats.outliers("sales", return_indices=True)
        assert "count" in result
        assert "indices" in result
        assert isinstance(result["indices"], list)

    def test_outliers_detects_9999(self, frame):
        result = frame.stats.outliers("sales")
        assert len(result) >= 1  # 9999 is an outlier

    def test_outliers_missing_column_raises(self, frame):
        with pytest.raises(TablofyColumnError):
            frame.stats.outliers("nonexistent")


class TestStatsUnivariate:
    @pytest.fixture
    def frame(self):
        return TablofyFrame(pd.DataFrame({
            "sales": [100, 200, 150, 300, 9999],
            "profit": [30, 50, 40, 80, 120],
        }))

    def test_mean(self, frame):
        assert isinstance(frame.stats.mean("sales"), float)

    def test_median(self, frame):
        assert isinstance(frame.stats.median("sales"), float)

    def test_std(self, frame):
        assert isinstance(frame.stats.std("sales"), float)

    def test_min(self, frame):
        assert isinstance(frame.stats.min("sales"), float)

    def test_max(self, frame):
        assert isinstance(frame.stats.max("sales"), float)

    def test_quantile(self, frame):
        assert isinstance(frame.stats.quantile("sales", 0.5), float)

    def test_value_counts(self, frame):
        result = frame.stats.value_counts("sales")
        assert isinstance(result, pd.Series)

    def test_mean_correct_value(self, frame):
        assert frame.stats.mean("sales") == pytest.approx(2149.8)

    def test_min_correct_value(self, frame):
        assert frame.stats.min("sales") == 100.0

    def test_max_correct_value(self, frame):
        assert frame.stats.max("sales") == 9999.0

    def test_median_correct_value(self, frame):
        assert frame.stats.median("sales") == 200.0

    def test_value_counts_sorted(self, frame):
        result = frame.stats.value_counts("sales")
        assert result.iloc[0] == 1  # all values appear once

    def test_mean_missing_column_raises(self, frame):
        with pytest.raises(TablofyColumnError):
            frame.stats.mean("nonexistent")

    def test_median_missing_column_raises(self, frame):
        with pytest.raises(TablofyColumnError):
            frame.stats.median("nonexistent")

    def test_std_missing_column_raises(self, frame):
        with pytest.raises(TablofyColumnError):
            frame.stats.std("nonexistent")

    def test_value_counts_missing_column_raises(self, frame):
        with pytest.raises(TablofyColumnError):
            frame.stats.value_counts("nonexistent")
