"""Column selection, dropping, renaming, sorting, pivoting, joining, and export."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from tablofy.core.errors import TablofyColumnError, TablofyFileError

if TYPE_CHECKING:
    from tablofy.core.frame import TablofyFrame


class Operations:
    """Stateless transform operations that return a new TablofyFrame."""

    def __init__(self, frame: TablofyFrame) -> None:
        self._frame = frame
        self._df = frame._df

    def _check_columns(self, *columns: str) -> None:
        """Raise TablofyColumnError if any column is missing."""
        missing = [c for c in columns if c not in self._df.columns]
        if missing:
            raise TablofyColumnError(
                f"Column(s) not found: {missing}. "
                f"Available: {list(self._df.columns)}"
            )

    def select(self, *columns: str) -> TablofyFrame:
        """Return a new frame with only the given columns.

        Parameters
        ----------
        *columns : str
            Column names to keep.

        Returns
        -------
        TablofyFrame
        """
        if not columns:
            raise TablofyColumnError("At least one column must be specified for select.")
        self._check_columns(*columns)

        from tablofy.core.frame import TablofyFrame
        return TablofyFrame(self._df[list(columns)].copy(), name=self._frame.name)

    def drop(self, column: str) -> TablofyFrame:
        """Return a new frame without *column*.

        Parameters
        ----------
        column : str
            Column name to remove.

        Returns
        -------
        TablofyFrame
        """
        self._check_columns(column)

        from tablofy.core.frame import TablofyFrame
        return TablofyFrame(self._df.drop(columns=[column]).copy(), name=self._frame.name)

    def rename(self, mapping: dict[str, str]) -> TablofyFrame:
        """Rename columns using *mapping* (old -> new).

        Parameters
        ----------
        mapping : dict[str, str]
            Old name -> new name pairs.

        Returns
        -------
        TablofyFrame
        """
        if not mapping:
            raise TablofyColumnError("Rename mapping cannot be empty.")
        self._check_columns(*mapping.keys())

        from tablofy.core.frame import TablofyFrame
        return TablofyFrame(self._df.rename(columns=mapping).copy(), name=self._frame.name)

    def sort(self, by: str, descending: bool = False) -> TablofyFrame:
        """Sort the frame by column *by*.

        Parameters
        ----------
        by : str
            Column to sort by.
        descending : bool
            Sort descending if True (default False).

        Returns
        -------
        TablofyFrame
        """
        self._check_columns(by)
        ascending = not descending

        from tablofy.core.frame import TablofyFrame
        return TablofyFrame(
            self._df.sort_values(by=by, ascending=ascending).copy(),
            name=self._frame.name,
        )

    def pivot(
        self,
        index: str,
        columns: str,
        values: str,
        aggfunc: str = "mean",
    ) -> TablofyFrame:
        """Create a pivot table.

        Parameters
        ----------
        index : str
            Column to use as rows.
        columns : str
            Column to use as new column headers.
        values : str
            Column to aggregate.
        aggfunc : str
            Aggregation function (default "mean").

        Returns
        -------
        TablofyFrame
        """
        self._check_columns(index, columns, values)

        import pandas as pd

        result = pd.pivot_table(
            self._df,
            index=index,
            columns=columns,
            values=values,
            aggfunc=aggfunc,
        ).reset_index()

        from tablofy.core.frame import TablofyFrame
        return TablofyFrame(result, name=self._frame.name)

    def join(
        self,
        other: TablofyFrame,
        on: str,
        how: str = "inner",
    ) -> TablofyFrame:
        """Join with another frame on a shared key column.

        Parameters
        ----------
        other : TablofyFrame
            The right-side frame.
        on : str
            Shared key column.
        how : str
            Type of join: ``"inner"``, ``"left"``, ``"right"``, or ``"outer"``
            (default ``"inner"``).

        Returns
        -------
        TablofyFrame
        """
        self._check_columns(on)
        if on not in other._df.columns:
            raise TablofyColumnError(
                f"Column {on!r} not found in the other frame. "
                f"Available: {list(other._df.columns)}"
            )

        allowed = {"inner", "left", "right", "outer", "cross"}
        if how not in allowed:
            raise TablofyColumnError(
                f"Invalid join type {how!r}. Must be one of {allowed}."
            )

        result = self._df.merge(other._df, on=on, how=how)

        from tablofy.core.frame import TablofyFrame
        return TablofyFrame(result, name=self._frame.name)

    def export(self, path: str, **kwargs: Any) -> None:
        """Export the frame to a file.

        Format is inferred from the file extension.

        Supported formats: ``.csv``, ``.xlsx``, ``.json``, ``.parquet``.

        Parameters
        ----------
        path : str
            Destination file path.
        **kwargs
            Passed through to the underlying pandas writer.
        """
        ext = path.rsplit(".", 1)[-1].lower() if "." in path else ""
        writers = {
            "csv": self._df.to_csv,
            "xlsx": self._df.to_excel,
            "json": self._df.to_json,
            "parquet": self._df.to_parquet,
        }
        writer = writers.get(ext)
        if writer is None:
            raise TablofyFileError(
                f"Unsupported export format: .{ext}. "
                f"Supported: {', '.join(writers)}"
            )
        writer(path, **kwargs)
