"""Standard chart types: bar, line, scatter, hist, box, heatmap, pairplot."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import matplotlib

matplotlib.use("Agg")

import matplotlib.figure  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import seaborn  # noqa: E402

from tablofy.core.errors import TablofyChartError, TablofyColumnError

if TYPE_CHECKING:
    from tablofy.core.frame import TablofyFrame


class Charts:
    """Generates matplotlib/seaborn charts from a TablofyFrame."""

    def __init__(self, frame: TablofyFrame) -> None:
        self._frame = frame
        self._df = frame._df

    def _check_cols(self, *cols: str) -> None:
        missing = [c for c in cols if c not in self._df.columns]
        if missing:
            raise TablofyColumnError(
                f"Column(s) not found: {missing}. "
                f"Available: {list(self._df.columns)}"
            )

    def _maybe_save(self, fig: Any, save: str | None) -> None:
        if save:
            fig.savefig(save, bbox_inches="tight")

    def bar(
        self, x: str, y: str, save: str | None = None, **kwargs: Any
    ) -> "matplotlib.figure.Figure":
        self._check_cols(x, y)
        fig, ax = plt.subplots()
        seaborn.barplot(data=self._df, x=x, y=y, ax=ax, **kwargs)
        ax.set_title(f"{y} by {x}")
        fig.tight_layout()
        self._maybe_save(fig, save)
        plt.close(fig)
        return fig

    def line(
        self, x: str, y: str, save: str | None = None, **kwargs: Any
    ) -> "matplotlib.figure.Figure":
        self._check_cols(x, y)
        fig, ax = plt.subplots()
        seaborn.lineplot(data=self._df, x=x, y=y, ax=ax, **kwargs)
        ax.set_title(f"{y} over {x}")
        fig.tight_layout()
        self._maybe_save(fig, save)
        plt.close(fig)
        return fig

    def scatter(
        self, x: str, y: str, save: str | None = None, **kwargs: Any
    ) -> "matplotlib.figure.Figure":
        self._check_cols(x, y)
        fig, ax = plt.subplots()
        seaborn.scatterplot(data=self._df, x=x, y=y, ax=ax, **kwargs)
        ax.set_title(f"{y} vs {x}")
        fig.tight_layout()
        self._maybe_save(fig, save)
        plt.close(fig)
        return fig

    def hist(
        self, column: str, save: str | None = None, **kwargs: Any
    ) -> "matplotlib.figure.Figure":
        self._check_cols(column)
        fig, ax = plt.subplots()
        seaborn.histplot(data=self._df, x=column, ax=ax, **kwargs)
        ax.set_title(f"Distribution of {column}")
        fig.tight_layout()
        self._maybe_save(fig, save)
        plt.close(fig)
        return fig

    def box(
        self, x: str, y: str, save: str | None = None, **kwargs: Any
    ) -> "matplotlib.figure.Figure":
        self._check_cols(x, y)
        fig, ax = plt.subplots()
        seaborn.boxplot(data=self._df, x=x, y=y, ax=ax, **kwargs)
        ax.set_title(f"{y} by {x}")
        fig.tight_layout()
        self._maybe_save(fig, save)
        plt.close(fig)
        return fig

    def heatmap(
        self, save: str | None = None, **kwargs: Any
    ) -> "matplotlib.figure.Figure":
        numeric = self._df.select_dtypes(include="number")
        if numeric.shape[1] < 2:
            raise TablofyChartError(
                "Heatmap requires at least 2 numeric columns."
            )
        fig, ax = plt.subplots()
        seaborn.heatmap(
            numeric.corr(), annot=True, fmt=".2f", cmap="coolwarm",
            ax=ax, **kwargs,
        )
        ax.set_title("Correlation Heatmap")
        fig.tight_layout()
        self._maybe_save(fig, save)
        plt.close(fig)
        return fig

    def pairplot(
        self, save: str | None = None, **kwargs: Any
    ) -> "seaborn.PairGrid":
        numeric = self._df.select_dtypes(include="number")
        if numeric.shape[1] < 2:
            raise TablofyChartError(
                "Pairplot requires at least 2 numeric columns."
            )
        pg = seaborn.pairplot(numeric, **kwargs)
        pg.fig.suptitle("Pairwise Relationships", y=1.02)
        self._maybe_save(pg.fig, save)
        return pg
