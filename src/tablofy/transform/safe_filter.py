"""Safe row filtering using pandas query with column validation."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from tablofy.core.errors import TablofyColumnError, TablofyDataError

if TYPE_CHECKING:
    from tablofy.core.frame import TablofyFrame


class SafeFilter:
    """Filters rows using a user-supplied expression."""

    _PYTHON_KEYWORDS = frozenset({
        "and", "or", "not", "in", "is", "True", "False", "None",
        "if", "else", "for", "while", "try", "except", "finally",
        "def", "class", "return", "import", "from", "as", "pass",
        "break", "continue", "lambda", "with", "yield", "raise",
    })

    def __init__(self, frame: TablofyFrame) -> None:
        self._frame = frame
        self._df = frame._df

    def filter(self, expression: str) -> TablofyFrame:
        """Return rows matching *expression* using ``pd.DataFrame.query``.

        Parameters
        ----------
        expression : str
            A pandas query expression (e.g. ``"age > 25"``).

        Returns
        -------
        TablofyFrame
            A new frame containing only the matching rows.

        Raises
        ------
        TablofyColumnError
            If a referenced column does not exist.
        TablofyDataError
            If the expression is invalid or empty.
        """
        if not expression or not expression.strip():
            raise TablofyDataError("Filter expression cannot be empty.")

        _sq = r"'[^']*'"
        _dq = r'"[^"]*"'
        no_strings = re.sub(f"{_sq}|{_dq}", "", expression)
        candidates = set(re.findall(r"\b[a-zA-Z_]\w*\b", no_strings))
        unknown = [
            c for c in candidates
            if c not in self._df.columns
            and c.lower() not in self._PYTHON_KEYWORDS
            and not c.startswith("@")
        ]
        if unknown:
            raise TablofyColumnError(
                f"Column(s) not found in dataset: {unknown}. "
                f"Available columns: {list(self._df.columns)}"
            )

        try:
            result = self._df.query(expression)
        except Exception as exc:
            raise TablofyDataError(
                f"Invalid filter expression: {expression!r}. "
                f"Error: {exc}"
            ) from exc

        from tablofy.core.frame import TablofyFrame
        return TablofyFrame(result.copy(), name=self._frame.name)
