"""Outlier detection using IQR and z-score methods."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pandas as pd

from tablofy.core.errors import TablofyColumnError

if TYPE_CHECKING:
    from tablofy.core.frame import TablofyFrame


class OutlierDetector:
    """Detects outliers in numeric columns."""

    def __init__(self, frame: TablofyFrame) -> None:
        self._frame = frame
        self._df = frame._df

    def iqr_outliers(
        self, column: str, multiplier: float = 1.5
    ) -> pd.DataFrame:
        """Return rows where *column* values are IQR outliers.

        Parameters
        ----------
        column : str
            Numeric column to check.
        multiplier : float
            IQR multiplier for the fence (default 1.5).

        Returns
        -------
        pd.DataFrame
            Rows where the column value is outside the IQR fences.
            Includes a ``_outlier_distance`` column.
        """
        if column not in self._df.columns:
            raise TablofyColumnError(
                f"Column {column!r} not found. "
                f"Available: {list(self._df.columns)}"
            )
        if not pd.api.types.is_numeric_dtype(self._df[column]):
            raise TablofyColumnError(
                f"Column {column!r} is not numeric."
            )

        q1 = self._df[column].quantile(0.25)
        q3 = self._df[column].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - multiplier * iqr
        upper = q3 + multiplier * iqr
        mask = (self._df[column] < lower) | (self._df[column] > upper)
        result = self._df[mask].copy()
        result["_outlier_distance"] = (self._df.loc[mask, column] - q3).abs()
        return result

    def zscore_outliers(
        self, column: str, threshold: float = 3.0
    ) -> pd.DataFrame:
        """Return rows where *column* has a z-score beyond *threshold*."""
        if column not in self._df.columns:
            raise TablofyColumnError(
                f"Column {column!r} not found. "
                f"Available: {list(self._df.columns)}"
            )
        if not pd.api.types.is_numeric_dtype(self._df[column]):
            raise TablofyColumnError(
                f"Column {column!r} is not numeric."
            )

        mean = self._df[column].mean()
        std = self._df[column].std()
        if std == 0:
            return self._df.iloc[:0].copy()
        zscores = (self._df[column] - mean).abs() / std
        result = self._df[zscores > threshold].copy()
        result["_zscore"] = zscores[zscores > threshold]
        return result
