"""Statistical helpers for TablofyFrame."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pandas as pd

from tablofy.core.errors import TablofyColumnError

if TYPE_CHECKING:
    from tablofy.core.frame import TablofyFrame


class Stats:
    """Statistical operations on a TablofyFrame.

    Accessed via ``data.stats``.
    """

    def __init__(self, frame: TablofyFrame) -> None:
        self._frame = frame
        self._df = frame._df

    def _check_col(self, column: str) -> None:
        if column not in self._df.columns:
            raise TablofyColumnError(
                f"Column {column!r} not found. "
                f"Available: {list(self._df.columns)}"
            )

    def _check_numeric(self, column: str) -> None:
        self._check_col(column)
        if not pd.api.types.is_numeric_dtype(self._df[column]):
            raise TablofyColumnError(
                f"Column {column!r} is not numeric."
            )

    def describe(self, **kwargs: Any) -> pd.DataFrame:
        """Return descriptive statistics for all columns."""
        return self._df.describe(include="all", **kwargs)

    def correlation(self, **kwargs: Any) -> pd.DataFrame:
        """Return the correlation matrix of numeric columns."""
        return self._df.select_dtypes(include="number").corr(**kwargs)

    def covariance(self, **kwargs: Any) -> pd.DataFrame:
        """Return the covariance matrix of numeric columns."""
        return self._df.select_dtypes(include="number").cov(**kwargs)

    def outliers(
        self,
        column: str,
        multiplier: float = 1.5,
        return_indices: bool = False,
    ) -> pd.DataFrame | dict:
        """Detect outliers in *column* using the IQR method.

        Parameters
        ----------
        column : str
            Numeric column to check.
        multiplier : float
            IQR multiplier for the fence (default 1.5).
        return_indices : bool
            If True, return a dict with ``count`` and ``indices``.

        Returns
        -------
        pd.DataFrame or dict
        """
        from tablofy.analytics.outliers import OutlierDetector

        result = OutlierDetector(self._frame).iqr_outliers(column, multiplier)
        if return_indices:
            return {
                "count": len(result),
                "indices": list(result.index),
            }
        return result

    def mean(self, column: str) -> float:
        """Return the mean of *column*."""
        self._check_numeric(column)
        return float(self._df[column].mean())

    def median(self, column: str) -> float:
        """Return the median of *column*."""
        self._check_numeric(column)
        return float(self._df[column].median())

    def std(self, column: str) -> float:
        """Return the standard deviation of *column*."""
        self._check_numeric(column)
        return float(self._df[column].std())

    def min(self, column: str) -> float:
        """Return the minimum of *column*."""
        self._check_numeric(column)
        return float(self._df[column].min())

    def max(self, column: str) -> float:
        """Return the maximum of *column*."""
        self._check_numeric(column)
        return float(self._df[column].max())

    def quantile(self, column: str, q: float) -> float:
        """Return the *q*-th quantile of *column*."""
        self._check_numeric(column)
        return float(self._df[column].quantile(q))

    def value_counts(self, column: str) -> pd.Series:
        """Return frequency counts for *column*."""
        self._check_col(column)
        return self._df[column].value_counts()
