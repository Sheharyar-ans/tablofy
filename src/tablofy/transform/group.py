"""Grouped aggregation support."""

from __future__ import annotations

from typing import TYPE_CHECKING

from tablofy.core.errors import TablofyColumnError

if TYPE_CHECKING:
    from tablofy.core.frame import TablofyFrame


class GroupedFrame:
    """Result of ``frame.group(by)``. Supports ``.sum()`` and ``.mean()``."""

    def __init__(self, frame: TablofyFrame, by: str) -> None:
        if by not in frame._df.columns:
            raise TablofyColumnError(
                f"Column {by!r} not found. Available: {list(frame._df.columns)}"
            )
        self._frame = frame
        self._df = frame._df
        self._by = by

    def sum(self, column: str | None = None) -> TablofyFrame:
        """Sum *column* per group.

        Parameters
        ----------
        column : str or None
            Column to sum. If None, sums all numeric columns.

        Returns
        -------
        TablofyFrame
        """
        if column is not None and column not in self._df.columns:
            raise TablofyColumnError(
                f"Column {column!r} not found. Available: {list(self._df.columns)}"
            )

        grouped = self._df.groupby(self._by)
        result = grouped[[column]].sum() if column else grouped.sum(numeric_only=True)
        result = result.reset_index()

        from tablofy.core.frame import TablofyFrame
        return TablofyFrame(result, name=self._frame.name)

    def mean(self, column: str | None = None) -> TablofyFrame:
        """Mean of *column* per group.

        Parameters
        ----------
        column : str or None
            Column to average. If None, averages all numeric columns.

        Returns
        -------
        TablofyFrame
        """
        if column is not None and column not in self._df.columns:
            raise TablofyColumnError(
                f"Column {column!r} not found. Available: {list(self._df.columns)}"
            )

        grouped = self._df.groupby(self._by)
        result = grouped[[column]].mean() if column else grouped.mean(numeric_only=True)
        result = result.reset_index()

        from tablofy.core.frame import TablofyFrame
        return TablofyFrame(result, name=self._frame.name)
