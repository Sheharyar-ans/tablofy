"""Schema inspector for column types and missing data."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pandas as pd

if TYPE_CHECKING:
    from tablofy.core.frame import TablofyFrame


class SchemaInspector:
    """Inspects column dtypes, null counts, and missing-value tables."""

    def __init__(self, frame: TablofyFrame) -> None:
        self._frame = frame
        self._df = frame._df

    def types_table(self) -> pd.DataFrame:
        """Return a DataFrame with column, dtype, non_null, nulls, null_pct."""
        rows = []
        for col in self._df.columns:
            nulls = int(self._df[col].isna().sum())
            total = len(self._df)
            rows.append({
                "column": col,
                "dtype": str(self._df[col].dtype),
                "non_null": total - nulls,
                "nulls": nulls,
                "null_pct": round(nulls / total * 100, 2) if total else 0.0,
            })
        return pd.DataFrame(rows)

    def missing_table(self) -> pd.DataFrame:
        """Return a DataFrame with column, missing count, and missing percent.

        Only includes columns that have at least one null value.
        Returns an empty DataFrame if no missing values exist.
        """
        rows = []
        for col in self._df.columns:
            nulls = int(self._df[col].isna().sum())
            if nulls > 0:
                total = len(self._df)
                rows.append({
                    "column": col,
                    "missing": nulls,
                    "percent": round(nulls / total * 100, 2) if total else 0.0,
                })
        if not rows:
            return pd.DataFrame(columns=["column", "missing", "percent"])
        return pd.DataFrame(rows)
