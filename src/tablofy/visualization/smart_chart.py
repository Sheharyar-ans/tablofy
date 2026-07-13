"""Smart chart dispatch — parses plain-English descriptions."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from tablofy.core.errors import TablofyDataError

if TYPE_CHECKING:
    from tablofy.core.frame import TablofyFrame


class SmartChart:
    """Parses a short description and dispatches to the right chart method."""

    def __init__(self, frame: TablofyFrame) -> None:
        self._frame = frame
        self._df = frame._df

    def parse_chart(self, description: str) -> tuple[str, dict]:
        """Return ``(chart_kind, kwargs)`` from a plain-English description.

        Supported patterns
        ------------------
        - ``"{y} by {x}"`` — bar chart (categorical x) or line chart (numeric x)
        - ``"{y} vs {x}"`` — scatter plot
        """
        desc = description.strip().lower()

        # "y vs x" → scatter
        m = re.match(r"^(.+?)\s+vs\s+(.+)$", desc)
        if m:
            y_name = self._resolve_column(m.group(1).strip())
            x_name = self._resolve_column(m.group(2).strip())
            return "scatter", {"x": x_name, "y": y_name}

        # "y by x" → bar or line
        m = re.match(r"^(.+?)\s+by\s+(.+)$", desc)
        if m:
            y_name = self._resolve_column(m.group(1).strip())
            x_name = self._resolve_column(m.group(2).strip())
            kind = self._guess_bar_or_line(x_name)
            return kind, {"x": x_name, "y": y_name}

        raise TablofyDataError(
            f"Could not parse chart description: {description!r}. "
            "Try patterns like 'sales by month' or 'profit vs ad_spend'."
        )

    def _resolve_column(self, name: str) -> str:
        """Find the actual column name (case-insensitive fuzzy match)."""
        name_lower = name.lower()
        for col in self._df.columns:
            if col.lower() == name_lower:
                return col
        # If no exact match, try partial match
        matches = [c for c in self._df.columns if name_lower in c.lower()]
        if matches:
            return matches[0]
        raise TablofyDataError(
            f"Column {name!r} not found. Available: {list(self._df.columns)}"
        )

    def _guess_bar_or_line(self, x_col: str) -> str:
        """Choose ``bar`` for categorical x, ``line`` for numeric x."""
        import pandas as pd

        series = self._df[x_col]
        if pd.api.types.is_numeric_dtype(series):
            return "line"
        return "bar"
