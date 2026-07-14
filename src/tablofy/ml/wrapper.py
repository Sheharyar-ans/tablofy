"""Lazy-loaded ML wrapper (scikit-learn)."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tablofy.core.frame import TablofyFrame


class MLWrapper:
    """Entry point for ML operations on a TablofyFrame.

    Accessed via ``data.ml``.

    Requires ``tablofy[ml]`` (scikit-learn).
    """

    def __init__(self, frame: TablofyFrame) -> None:
        self._frame = frame
        self._df = frame._df
        self._model = None

    def _check_imports(self) -> None:
        try:
            import sklearn  # noqa: F401
        except ImportError:
            raise ImportError(
                "scikit-learn is required for ML features.\n"
                "  pip install tablofy[ml]"
            ) from None
