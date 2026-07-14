"""Interactive Jupyter Notebook widget explorer for TablofyFrame.

Usage in a notebook
-------------------
>>> data.explore_interactive()
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pandas as pd

if TYPE_CHECKING:
    from tablofy.core.frame import TablofyFrame


def _in_notebook() -> bool:
    """Return True if running inside an IPython / Jupyter kernel."""
    try:
        from IPython import get_ipython

        shell = get_ipython()
        if shell is not None and "IPython" in type(shell).__name__:
            return True
    except ImportError:
        pass
    return False


def _check_imports() -> None:
    """Check that ipywidgets and IPython are available, or raise."""
    try:
        import ipywidgets  # noqa: F401
        import IPython.display  # noqa: F401
        import matplotlib  # noqa: F401
    except ImportError as exc:
        name = exc.name
        msg = (
            f"'{name}' is required for interactive exploration.\n"
            f"  pip install tablofy[widgets]\n"
            f"  pip install tablofy[all]"
        )
        raise ImportError(msg) from exc


def explore_interactive(frame: TablofyFrame) -> None:
    """Launch an interactive widget dashboard for the current TablofyFrame.

    Displays a column picker, real-time filters, a dynamic table preview,
    and an auto-updating chart.  Only works inside a Jupyter notebook;
    prints a friendly message otherwise.
    """
    if not _in_notebook():
        print(
            "explore_interactive() is designed for Jupyter Notebook / "
            "JupyterLab.\nRun this code in a notebook cell to see the "
            "interactive dashboard."
        )
        return

    _check_imports()

    import ipywidgets as wg
    from IPython.display import display

    import matplotlib.pyplot as plt
    import seaborn as sns

    df: pd.DataFrame = frame._df

    # -- Column selector -------------------------------------------------------
    col_picker = wg.Dropdown(
        options=list(df.columns),
        description="Column:",
        style={"description_width": "initial"},
    )

    # -- Chart type toggle -----------------------------------------------------
    chart_type = wg.ToggleButtons(
        options=["Auto", "Bar", "Histogram", "Box"],
        value="Auto",
        description="Chart:",
    )

    # -- Filter widgets (built dynamically) ------------------------------------
    filter_box = wg.VBox([])
    current_filters: dict[str, wg.Widget] = {}

    def _numeric_range_widget(col: str) -> wg.FloatRangeSlider:
        lo, hi = float(df[col].min()), float(df[col].max())
        pad = max((hi - lo) * 0.05, 0.01)
        return wg.FloatRangeSlider(
            value=[lo, hi],
            min=lo - pad,
            max=hi + pad,
            step=(hi - lo) / 100 if hi > lo else 0.01,
            description=col,
            continuous_update=False,
            readout=True,
        )

    def _categorical_select_widget(col: str) -> wg.SelectMultiple:
        options = sorted(df[col].dropna().unique().tolist())
        return wg.SelectMultiple(
            options=options,
            value=tuple(options),
            description=col,
            rows=min(6, len(options)),
        )

    def _rebuild_filters(*args) -> None:
        col = col_picker.value
        children = []
        for c in df.columns:
            if c == col:
                continue
            if pd.api.types.is_numeric_dtype(df[c]):
                w = _numeric_range_widget(c)
            else:
                w = _categorical_select_widget(c)
            w.observe(_on_filter_change, "value")
            current_filters[c] = w
            children.append(w)
        filter_box.children = children

    # -- Output areas ----------------------------------------------------------
    table_out = wg.Output()
    chart_out = wg.Output()

    def _apply_filters() -> pd.DataFrame:
        filtered = df.copy()
        for col, w in current_filters.items():
            if isinstance(w, wg.FloatRangeSlider):
                lo, hi = w.value
                filtered = filtered[(filtered[col] >= lo) & (filtered[col] <= hi)]
            elif isinstance(w, wg.SelectMultiple):
                vals = set(w.value)
                if vals:
                    filtered = filtered[filtered[col].isin(vals)]
        return filtered

    def _on_filter_change(*args) -> None:
        _refresh()

    def _on_column_change(*args) -> None:
        _rebuild_filters()
        _refresh()

    def _refresh() -> None:
        filtered = _apply_filters()

        # Table
        table_out.clear_output(wait=True)
        with table_out:
            display(
                wg.HTML(
                    f"<b>Rows:</b> {len(filtered)} / {len(df)}  &nbsp;|&nbsp; "
                    f"<b>Columns:</b> {len(filtered.columns)}"
                )
            )
            display(wg.HTML(filtered.head(50).to_html(index=False)))

        # Chart
        col = col_picker.value
        kind = chart_type.value
        chart_out.clear_output(wait=True)
        with chart_out:
            fig, ax = plt.subplots(figsize=(8, 4))
            try:
                if kind == "Bar" or (kind == "Auto" and not pd.api.types.is_numeric_dtype(filtered[col])):
                    filtered[col].value_counts().sort_index().plot(kind="bar", ax=ax)
                    ax.set_title(f"Bar chart — {col}")
                    ax.set_xlabel(col)
                    ax.set_ylabel("count")
                elif kind == "Histogram" or (kind == "Auto" and pd.api.types.is_numeric_dtype(filtered[col])):
                    sns.histplot(data=filtered, x=col, ax=ax)
                    ax.set_title(f"Histogram — {col}")
                elif kind == "Box":
                    if pd.api.types.is_numeric_dtype(filtered[col]):
                        sns.boxplot(data=filtered, y=col, ax=ax)
                        ax.set_title(f"Box plot — {col}")
                    else:
                        ax.text(0.5, 0.5, "Box plot requires a numeric column",
                                ha="center", va="center", transform=ax.transAxes)
                else:
                    ax.text(0.5, 0.5, "Select a column to begin",
                            ha="center", va="center", transform=ax.transAxes)
            except Exception:
                ax.text(0.5, 0.5, "Could not render chart",
                        ha="center", va="center", transform=ax.transAxes)
            fig.tight_layout()
            display(fig)
            plt.close(fig)

    # -- Wire observers --------------------------------------------------------
    col_picker.observe(_on_column_change, "value")
    chart_type.observe(_on_filter_change, "value")

    # -- Layout ----------------------------------------------------------------
    header = wg.HTML(
        f"<h2>Tablofy Explorer — {frame.name}</h2>"
        f"<p>Select a column, apply filters, and explore your data interactively.</p>"
    )
    controls = wg.HBox([col_picker, chart_type])
    left_panel = wg.VBox([controls, filter_box])
    right_panel = wg.VBox([table_out, chart_out])
    dashboard = wg.VBox([header, wg.HBox([left_panel, right_panel])])

    # -- Initial render --------------------------------------------------------
    _rebuild_filters()
    _refresh()

    display(dashboard)
