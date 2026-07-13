"""Descriptive and categorical summary generators."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pandas as pd

if TYPE_CHECKING:
    from tablofy.core.frame import TablofyFrame


class Summarizer:
    """Generates summary statistics for a TablofyFrame."""

    def __init__(self, frame: TablofyFrame) -> None:
        self._frame = frame
        self._df = frame._df

    def descriptive_summary(self) -> pd.DataFrame:
        """Return descriptive statistics for all numeric columns.

        Includes count, mean, std, min, 25%, 50%, 75%, max.
        """
        return self._df.describe(include="all")

    def categorical_summary(self) -> dict[str, Any]:
        """Return value counts for each categorical column."""
        summary = {}
        for col in self._df.select_dtypes(include=["category", "bool"]).columns:
            summary[col] = self._df[col].value_counts().to_dict()
        return summary
