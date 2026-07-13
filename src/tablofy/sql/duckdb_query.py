"""SQL query execution via DuckDB."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

import duckdb

from tablofy.core.errors import TablofyDataError

if TYPE_CHECKING:
    from tablofy.core.frame import TablofyFrame


class DuckDBQuery:
    """Runs SQL queries against a TablofyFrame using DuckDB.

    Every query is executed in an isolated in-memory DuckDB session.
    Only read-only statements (SELECT, WITH, DESCRIBE, EXPLAIN) are
    permitted.
    """

    _READ_ONLY_KEYWORDS = frozenset({
        "select", "with", "describe", "explain", "show", "pragma",
    })

    def __init__(self, frame: TablofyFrame) -> None:
        self._frame = frame

    @staticmethod
    def _is_read_only(sql: str) -> bool:
        """Check that the SQL statement is read-only."""
        stripped = sql.strip()
        if not stripped:
            return False
        first_token = re.match(r"\s*(with|select|describe|explain|show|pragma)\b", sql, re.I)
        return first_token is not None

    def execute(self, sql: str) -> TablofyFrame:
        """Execute *sql* and return a new ``TablofyFrame``.

        Parameters
        ----------
        sql : str
            A read-only SQL query. The dataframe is registered as ``data``.

        Returns
        -------
        TablofyFrame

        Raises
        ------
        TablofyDataError
            If the query is non-read-only, empty, or syntactically invalid.
        """
        if not sql or not sql.strip():
            raise TablofyDataError("SQL query cannot be empty.")

        if not self._is_read_only(sql):
            raise TablofyDataError(
                "Only read-only queries (SELECT, WITH, DESCRIBE, EXPLAIN, "
                "SHOW, PRAGMA) are allowed."
            )

        try:
            con = duckdb.connect(":memory:")
            con.register("data", self._frame._df)
            result = con.execute(sql).fetchdf()
            con.close()
        except Exception as exc:
            raise TablofyDataError(
                f"SQL query failed: {exc}"
            ) from exc

        from tablofy.core.frame import TablofyFrame
        return TablofyFrame(result, name=self._frame.name)
