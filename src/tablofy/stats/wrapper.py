"""Lazy-loaded advanced statistics wrapper (SciPy, Statsmodels)."""

from __future__ import annotations

from typing import TYPE_CHECKING

from tablofy.analytics.stats import Stats

if TYPE_CHECKING:
    from tablofy.core.frame import TablofyFrame


class DataFrameStats(Stats):
    """Entry point for advanced statistics on a TablofyFrame.

    Accessed via ``data.stats``.

    Provides all basic stats from the parent ``Stats`` class plus
    advanced methods that require ``tablofy[stats]`` (scipy, statsmodels).
    """

    def __init__(self, frame: TablofyFrame) -> None:
        super().__init__(frame)

    def _check_advanced_imports(self) -> None:
        try:
            import scipy  # noqa: F401
        except ImportError:
            raise ImportError(
                "SciPy is required for advanced statistics.\n"
                "  pip install tablofy[stats]"
            ) from None
