"""Output formatting and string transformation utilities."""

from __future__ import annotations

import re


class Formatter:
    """Helpers for formatting numbers, tables, and text."""

    @staticmethod
    def pretty_number(value: float, decimals: int = 2) -> str:
        """Format a float with *decimals* and thousand separators."""
        return f"{value:,.{decimals}f}"

    @staticmethod
    def pct(value: float, decimals: int = 1) -> str:
        """Format a ratio as a percentage string."""
        return f"{value * 100:.{decimals}f}%"

    @staticmethod
    def truncate(text: str, max_len: int = 80) -> str:
        """Truncate *text* with an ellipsis if longer than *max_len*."""
        return text if len(text) <= max_len else text[: max_len - 3] + "..."

    @staticmethod
    def to_snake_case(name: str) -> str:
        """Convert a column name to snake_case.

        Handles CamelCase, spaces, hyphens, and special characters.

        Parameters
        ----------
        name : str
            Original column name.

        Returns
        -------
        str
            Cleaned snake_case name.
        """
        s = name.strip()
        s = re.sub(r"([A-Z])([A-Z][a-z])", r"\1_\2", s)
        s = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s)
        s = re.sub(r"[\s\-\.]+", "_", s)
        s = re.sub(r"[^\w]", "", s)
        s = s.lower()
        s = re.sub(r"_+", "_", s)
        s = s.strip("_")
        return s or "column"
