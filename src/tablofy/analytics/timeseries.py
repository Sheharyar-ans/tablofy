"""Time-series helpers for TablofyFrame.

Accessed via ``data.ts``.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pandas as pd

from tablofy.core.errors import TablofyColumnError, TablofyDataError

if TYPE_CHECKING:
    from tablofy.core.frame import TablofyFrame


class TimeSeries:
    """Time-series transformation helpers on a TablofyFrame.

    Parameters
    ----------
    frame : TablofyFrame
        The parent frame whose underlying DataFrame will be operated on.
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

    def set_time_index(self, column: str) -> TablofyFrame:
        """Convert *column* to datetime and set it as the DataFrame index.

        The operation is performed in-place on the underlying DataFrame.

        Parameters
        ----------
        column : str
            Name of the column to parse and promote to the index.

        Returns
        -------
        TablofyFrame
            ``self``, so you can chain further operations.
        """
        self._check_col(column)
        try:
            self._df[column] = pd.to_datetime(self._df[column])
        except (ValueError, TypeError) as exc:
            raise TablofyDataError(
                f"Could not convert column {column!r} to datetime: {exc}"
            ) from exc
        self._df.set_index(column, inplace=True)
        self._df.index.name = column
        return self._frame

    def resample(self, rule: str, agg: str = "sum") -> TablofyFrame:
        """Resample the time-series data using *agg*.

        The DataFrame index must be a datetime-like index (use
        ``set_time_index`` first).

        Parameters
        ----------
        rule : str
            Pandas offset alias, e.g. ``"M"`` (month end), ``"W"`` (weekly),
            ``"D"`` (daily), ``"h"`` (hourly).
        agg : str
            Aggregation function — ``"sum"``, ``"mean"``, ``"median"``,
            ``"min"``, ``"max"``, etc. (default ``"sum"``).

        Returns
        -------
        TablofyFrame
            A new frame with resampled data.
        """
        if not isinstance(self._df.index, pd.DatetimeIndex):
            raise TablofyDataError(
                "The DataFrame index is not a DatetimeIndex. "
                "Use .ts.set_time_index(col) first."
            )
        resampled = self._df.resample(rule).agg(agg)
        from tablofy.core.frame import TablofyFrame

        return TablofyFrame(resampled, name=self._frame.name)

    def rolling(self, window: int, col: str, **kwargs):
        """Calculate rolling mean on the specified column.

        Returns a TablofyFrame containing the rolling window results to
        preserve library chainability.

        Parameters
        ----------
        window : int
            Window size (number of periods).
        col : str
            Numeric column to compute the rolling statistic on.

        Returns
        -------
        TablofyFrame
            A new frame containing the rolling mean column.
        """
        from tablofy.core.frame import TablofyFrame

        self._check_col(col)
        rolling_series = self._df[col].rolling(window=window, **kwargs).mean()
        rolling_df = pd.DataFrame({f"{col}_rolling_{window}": rolling_series})
        return TablofyFrame(rolling_df, name=f"{self._frame.name}_rolling")

    def detect_trend(self, column: str) -> dict:
        """Detect the overall trend direction of *column*.

        If *statsmodels* is installed, seasonal decomposition is used for a
        more robust estimate.  Otherwise a simple linear regression is
        fitted via numpy.

        Parameters
        ----------
        column : str
            Numeric column to analyse.

        Returns
        -------
        dict
            Keys: ``direction`` ("upward", "downward", "flat"),
            ``slope`` (float), ``strength`` ("strong", "moderate", "weak").
        """
        self._check_col(column)
        import numpy as np

        y = self._df[column].dropna().values
        x = np.arange(len(y))

        if len(y) < 2:
            return {"direction": "flat", "slope": 0.0, "strength": "weak"}

        try:
            import statsmodels.api as sm

            mod = sm.OLS(y, sm.add_constant(x)).fit()
            slope = float(mod.params[1])
        except ImportError:
            slope = float(np.polyfit(x, y, 1)[0])

        eps = 1e-8
        y_range = float(np.ptp(y)) if np.ptp(y) > eps else 1.0
        relative_slope = abs(slope) / y_range

        if relative_slope < 0.01:
            direction = "flat"
            strength = "weak"
        elif relative_slope < 0.05:
            direction = "upward" if slope > 0 else "downward"
            strength = "weak"
        elif relative_slope < 0.15:
            direction = "upward" if slope > 0 else "downward"
            strength = "moderate"
        else:
            direction = "upward" if slope > 0 else "downward"
            strength = "strong"

        return {
            "direction": direction,
            "slope": round(slope, 6),
            "strength": strength,
        }
