"""Standard chart types with optional Plotly interactive support."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import matplotlib

matplotlib.use("Agg")

import matplotlib.figure  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import seaborn  # noqa: E402

from tablofy.core.errors import TablofyChartError, TablofyColumnError
from tablofy.visualization.styles import get_plotly_template

if TYPE_CHECKING:
    from tablofy.core.frame import TablofyFrame


def _check_plotly() -> None:
    try:
        import plotly.express  # noqa: F401
    except ImportError:
        raise ImportError(
            "Plotly is required for interactive charts.\n"
            "  pip install tablofy[viz]\n"
            "  pip install tablofy[all]"
        ) from None


class Charts:
    """Generates matplotlib/seaborn or Plotly charts from a TablofyFrame."""

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

    @staticmethod
    def _apply_plotly_template(fig: Any) -> None:
        template = get_plotly_template()
        if template:
            fig.update_layout(template=template)

    # ------------------------------------------------------------------
    #  Bar
    # ------------------------------------------------------------------

    def bar(
        self,
        x: str,
        y: str,
        interactive: bool = False,
        save: str | None = None,
        **kwargs: Any,
    ) -> matplotlib.figure.Figure | Any:
        self._check_cols(x, y)

        if interactive:
            _check_plotly()
            import plotly.express as px

            fig = px.bar(self._df, x=x, y=y, title=f"{y} by {x}", **kwargs)
            self._apply_plotly_template(fig)
            if save:
                fig.write_html(save)
            return fig

        fig, ax = plt.subplots()
        seaborn.barplot(data=self._df, x=x, y=y, ax=ax, **kwargs)
        ax.set_title(f"{y} by {x}")
        fig.tight_layout()
        self._maybe_save(fig, save)
        plt.close(fig)
        return fig

    # ------------------------------------------------------------------
    #  Line
    # ------------------------------------------------------------------

    def line(
        self,
        x: str,
        y: str,
        interactive: bool = False,
        save: str | None = None,
        **kwargs: Any,
    ) -> matplotlib.figure.Figure | Any:
        self._check_cols(x, y)

        if interactive:
            _check_plotly()
            import plotly.express as px

            fig = px.line(self._df, x=x, y=y, title=f"{y} over {x}", **kwargs)
            self._apply_plotly_template(fig)
            if save:
                fig.write_html(save)
            return fig

        fig, ax = plt.subplots()
        seaborn.lineplot(data=self._df, x=x, y=y, ax=ax, **kwargs)
        ax.set_title(f"{y} over {x}")
        fig.tight_layout()
        self._maybe_save(fig, save)
        plt.close(fig)
        return fig

    # ------------------------------------------------------------------
    #  Scatter
    # ------------------------------------------------------------------

    def scatter(
        self,
        x: str,
        y: str,
        interactive: bool = False,
        save: str | None = None,
        **kwargs: Any,
    ) -> matplotlib.figure.Figure | Any:
        self._check_cols(x, y)

        if interactive:
            _check_plotly()
            import plotly.express as px

            fig = px.scatter(self._df, x=x, y=y, title=f"{y} vs {x}", **kwargs)
            self._apply_plotly_template(fig)
            if save:
                fig.write_html(save)
            return fig

        fig, ax = plt.subplots()
        seaborn.scatterplot(data=self._df, x=x, y=y, ax=ax, **kwargs)
        ax.set_title(f"{y} vs {x}")
        fig.tight_layout()
        self._maybe_save(fig, save)
        plt.close(fig)
        return fig

    # ------------------------------------------------------------------
    #  Histogram
    # ------------------------------------------------------------------

    def hist(
        self,
        column: str,
        interactive: bool = False,
        save: str | None = None,
        **kwargs: Any,
    ) -> matplotlib.figure.Figure | Any:
        self._check_cols(column)

        if interactive:
            _check_plotly()
            import plotly.express as px

            fig = px.histogram(self._df, x=column, title=f"Distribution of {column}", **kwargs)
            self._apply_plotly_template(fig)
            if save:
                fig.write_html(save)
            return fig

        fig, ax = plt.subplots()
        seaborn.histplot(data=self._df, x=column, ax=ax, **kwargs)
        ax.set_title(f"Distribution of {column}")
        fig.tight_layout()
        self._maybe_save(fig, save)
        plt.close(fig)
        return fig

    # ------------------------------------------------------------------
    #  Box
    # ------------------------------------------------------------------

    def box(
        self,
        x: str,
        y: str,
        interactive: bool = False,
        save: str | None = None,
        **kwargs: Any,
    ) -> matplotlib.figure.Figure | Any:
        self._check_cols(x, y)

        if interactive:
            _check_plotly()
            import plotly.express as px

            fig = px.box(self._df, x=x, y=y, title=f"{y} by {x}", **kwargs)
            self._apply_plotly_template(fig)
            if save:
                fig.write_html(save)
            return fig

        fig, ax = plt.subplots()
        seaborn.boxplot(data=self._df, x=x, y=y, ax=ax, **kwargs)
        ax.set_title(f"{y} by {x}")
        fig.tight_layout()
        self._maybe_save(fig, save)
        plt.close(fig)
        return fig

    # ------------------------------------------------------------------
    #  Heatmap
    # ------------------------------------------------------------------

    def heatmap(
        self,
        interactive: bool = False,
        save: str | None = None,
        **kwargs: Any,
    ) -> matplotlib.figure.Figure | Any:
        numeric = self._df.select_dtypes(include="number")
        if numeric.shape[1] < 2:
            raise TablofyChartError(
                "Heatmap requires at least 2 numeric columns."
            )

        if interactive:
            _check_plotly()
            import plotly.express as px

            fig = px.imshow(
                numeric.corr(),
                text_auto=".2f",
                color_continuous_scale="RdBu_r",
                title="Correlation Heatmap",
                **kwargs,
            )
            self._apply_plotly_template(fig)
            if save:
                fig.write_html(save)
            return fig

        fig, ax = plt.subplots()
        seaborn.heatmap(
            numeric.corr(),
            annot=True,
            fmt=".2f",
            cmap="coolwarm",
            ax=ax,
            **kwargs,
        )
        ax.set_title("Correlation Heatmap")
        fig.tight_layout()
        self._maybe_save(fig, save)
        plt.close(fig)
        return fig

    # ------------------------------------------------------------------
    #  Pairplot
    # ------------------------------------------------------------------

    def pairplot(
        self,
        interactive: bool = False,
        save: str | None = None,
        **kwargs: Any,
    ) -> seaborn.PairGrid | Any:
        numeric = self._df.select_dtypes(include="number")
        if numeric.shape[1] < 2:
            raise TablofyChartError(
                "Pairplot requires at least 2 numeric columns."
            )

        if interactive:
            _check_plotly()
            import plotly.figure_factory as ff

            fig = ff.create_scatterplotmatrix(
                numeric, diag="histogram", **kwargs
            )
            fig.update_layout(title="Pairwise Relationships")
            self._apply_plotly_template(fig)
            if save:
                fig.write_html(save)
            return fig

        pg = seaborn.pairplot(numeric, **kwargs)
        pg.fig.suptitle("Pairwise Relationships", y=1.02)
        self._maybe_save(pg.fig, save)
        return pg

    # ------------------------------------------------------------------
    #  Area
    # ------------------------------------------------------------------

    def area(
        self,
        x: str,
        y: str,
        interactive: bool = False,
        save: str | None = None,
        **kwargs: Any,
    ) -> matplotlib.figure.Figure | Any:
        self._check_cols(x, y)

        if interactive:
            _check_plotly()
            import plotly.express as px

            fig = px.area(self._df, x=x, y=y, title=f"{y} over {x}", **kwargs)
            self._apply_plotly_template(fig)
            if save:
                fig.write_html(save)
            return fig

        fig, ax = plt.subplots()
        seaborn.lineplot(data=self._df, x=x, y=y, ax=ax, **kwargs)
        ax.fill_between(
            self._df[x].astype(str) if not self._df[x].dtype.kind in "iuf" else self._df[x],
            self._df[y],
            alpha=0.3,
        )
        ax.set_title(f"{y} over {x}")
        fig.tight_layout()
        self._maybe_save(fig, save)
        plt.close(fig)
        return fig

    # ------------------------------------------------------------------
    #  Pie
    # ------------------------------------------------------------------

    def pie(
        self,
        labels: str,
        values: str,
        interactive: bool = False,
        save: str | None = None,
        **kwargs: Any,
    ) -> matplotlib.figure.Figure | Any:
        self._check_cols(labels, values)

        if interactive:
            _check_plotly()
            import plotly.express as px

            fig = px.pie(self._df, names=labels, values=values, title=f"{values} by {labels}", **kwargs)
            self._apply_plotly_template(fig)
            if save:
                fig.write_html(save)
            return fig

        fig, ax = plt.subplots()
        data = self._df.groupby(labels)[values].sum().sort_index()
        ax.pie(data.values, labels=data.index, autopct="%1.1f%%", **kwargs)
        ax.set_title(f"{values} by {labels}")
        fig.tight_layout()
        self._maybe_save(fig, save)
        plt.close(fig)
        return fig

    # ------------------------------------------------------------------
    #  Violin
    # ------------------------------------------------------------------

    def violin(
        self,
        x: str,
        y: str,
        interactive: bool = False,
        save: str | None = None,
        **kwargs: Any,
    ) -> matplotlib.figure.Figure | Any:
        self._check_cols(x, y)

        if interactive:
            _check_plotly()
            import plotly.express as px

            fig = px.violin(self._df, x=x, y=y, title=f"{y} by {x}", **kwargs)
            self._apply_plotly_template(fig)
            if save:
                fig.write_html(save)
            return fig

        fig, ax = plt.subplots()
        seaborn.violinplot(data=self._df, x=x, y=y, ax=ax, **kwargs)
        ax.set_title(f"{y} by {x}")
        fig.tight_layout()
        self._maybe_save(fig, save)
        plt.close(fig)
        return fig
