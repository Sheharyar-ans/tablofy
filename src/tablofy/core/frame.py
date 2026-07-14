"""Core TablofyFrame class wrapping a pandas DataFrame."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pandas as pd

from tablofy.core.errors import TablofyDataError

if TYPE_CHECKING:
    from tablofy.transform.group import GroupedFrame


class TablofyFrame:
    """Primary data container representing a tabular dataset.

    Wraps a ``pd.DataFrame`` and provides a high-level API for loading,
    cleaning, exploring, visualising, and reporting on data.

    Parameters
    ----------
    df : pd.DataFrame
        The underlying data. Must not be empty.
    name : str
        A human-friendly label derived from the source filename.
    """

    def __init__(self, df: pd.DataFrame, name: str = "") -> None:
        if df.empty:
            raise TablofyDataError(
                "Cannot create a TablofyFrame from an empty dataset."
            )
        self._df = df
        self.name = name or "Data"
        self._last_clean_actions: list[dict] = []
        self._ml: Any | None = None
        self._stats: Any | None = None
        self._scrape: Any | None = None
        self._ts: Any | None = None

    # -- Properties -----------------------------------------------------------

    @property
    def dtypes(self) -> dict[str, str]:
        """Return a mapping of column name -> dtype string."""
        return {col: str(dtype) for col, dtype in self._df.dtypes.items()}

    @property
    def size(self) -> int:
        """Return the total number of cells (rows * columns)."""
        return int(self._df.size)

    @property
    def stats(self):
        """Access basic and advanced statistical methods.

        Basic stats (mean, median, std, etc.) work out of the box.
        Advanced stats (SciPy / Statsmodels) require ``tablofy[stats]``.
        """
        if self._stats is None:
            try:
                from tablofy.stats.wrapper import DataFrameStats
                self._stats = DataFrameStats(self)
            except ImportError:
                from tablofy.analytics.stats import Stats
                self._stats = Stats(self)
        return self._stats

    @property
    def ml(self):
        """Access ML operations (scikit-learn).

        Requires ``tablofy[ml]``.
        """
        if self._ml is None:
            try:
                import sklearn  # noqa: F401
            except ImportError as exc:
                raise ImportError(
                    "scikit-learn is required for ML features.\n"
                    "  pip install tablofy[ml]"
                ) from exc
            from tablofy.ml.wrapper import MLWrapper
            self._ml = MLWrapper(self)
        return self._ml

    @property
    def scrape(self):
        """Access web-scraping operations (BeautifulSoup, Requests).

        Requires ``tablofy[scraping]``.
        """
        if self._scrape is None:
            try:
                import bs4  # noqa: F401
                import requests  # noqa: F401
            except ImportError as exc:
                raise ImportError(
                    "beautifulsoup4 and requests are required for scraping.\n"
                    "  pip install tablofy[scraping]"
                ) from exc
            from tablofy.scrape.wrapper import ScrapeWrapper
            self._scrape = ScrapeWrapper(self)
        return self._scrape

    # -- Exploration ----------------------------------------------------------

    def preview(self, n: int = 5) -> pd.DataFrame:
        """Return the first *n* rows of the dataset.

        Parameters
        ----------
        n : int
            Number of rows (default 5).

        Returns
        -------
        pd.DataFrame
        """
        return self._df.head(n)

    def head(self, n: int = 5) -> pd.DataFrame:
        """Return the first *n* rows.

        Alias for :meth:`preview`.

        Parameters
        ----------
        n : int
            Number of rows (default 5).

        Returns
        -------
        pd.DataFrame
        """
        return self._df.head(n)

    def shape(self) -> dict[str, int]:
        """Return a dict with ``rows`` and ``columns`` counts.

        Returns
        -------
        dict[str, int]
        """
        return {"rows": self._df.shape[0], "columns": self._df.shape[1]}

    def columns(self) -> list[str]:
        """Return column names as a list.

        Returns
        -------
        list[str]
        """
        return list(self._df.columns)

    def types(self) -> pd.DataFrame:
        """Return column names, dtypes, and null counts.

        Returns
        -------
        pd.DataFrame
            Columns: ``column``, ``dtype``, ``non_null``, ``nulls``, ``null_pct``.
        """
        from tablofy.exploration.schema import SchemaInspector

        return SchemaInspector(self).types_table()

    def missing(self) -> pd.DataFrame:
        """Return missing-value count and percent per column.

        Only includes columns that have at least one null value.

        Returns
        -------
        pd.DataFrame
            Columns: ``column``, ``missing``, ``percent``.
        """
        from tablofy.exploration.schema import SchemaInspector

        return SchemaInspector(self).missing_table()

    def duplicates(self) -> dict[str, int | float]:
        """Return duplicate row count and percentage.

        Returns
        -------
        dict[str, int | float]
            Keys: ``count``, ``percent``.
        """
        count = int(self._df.duplicated().sum())
        return {
            "count": count,
            "percent": round(count / len(self._df) * 100, 2) if len(self._df) else 0.0,
        }

    def summary(self) -> pd.DataFrame:
        """Return descriptive statistics for all columns.

        Numeric columns: count, mean, std, min, 25%, 50%, 75%, max.
        Categorical/text columns: count, unique, top, freq.

        Returns
        -------
        pd.DataFrame
        """
        from tablofy.exploration.summary import Summarizer

        return Summarizer(self).descriptive_summary()

    def profile(self) -> dict:
        """Return a beginner-friendly dataset profile.

        Includes row/column counts, missing values, duplicates, column
        type breakdown (numeric, text, date, categorical), and memory usage.

        Returns
        -------
        dict
        """
        from tablofy.exploration.profile import Profiler

        return Profiler(self).run()

    # -- Cleaning -------------------------------------------------------------

    def clean(
        self,
        duplicates: bool = True,
        missing: str | dict = "smart",
        columns: str | bool = "snake_case",
        dates: bool = True,
        text: bool = True,
    ) -> TablofyFrame:
        """Clean the dataset in-place and return ``self`` for chaining.

        Parameters
        ----------
        duplicates : bool
            Remove duplicate rows (default True).
        missing : str or dict
            ``"smart"`` — fill numeric with median, text with mode.
            ``"off"`` or ``False`` — skip.
            ``dict`` — explicit column -> value mapping for ``fillna``.
        columns : str or bool
            ``"snake_case"`` — normalise column names (default).
            ``False`` — leave names unchanged.
        dates : bool
            Attempt to parse date-like object columns (default True).
        text : bool
            Strip whitespace from text columns and drop fully-null columns
            (default True).

        Returns
        -------
        TablofyFrame
            ``self``, so you can chain: ``data.clean().summary()``.
        """
        from tablofy.cleaning.cleaner import Cleaner

        cleaner = Cleaner(self)
        result = cleaner.run(
            duplicates=duplicates,
            missing=missing,
            columns=columns,
            dates=dates,
            text=text,
        )
        self._last_clean_actions = cleaner.actions
        return result

    def clean_report(self) -> dict:
        """Return a report of the last cleaning run.

        Returns
        -------
        dict
            Keys: ``actions`` (list of action dicts), ``action_count``,
            ``summary_text`` (human-readable overview).
        """
        from tablofy.cleaning.report import CleanReport

        return CleanReport(self).summary()

    # -- Transform ------------------------------------------------------------

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
        from tablofy.transform.operations import Operations
        return Operations(self).select(*columns)

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
        from tablofy.transform.operations import Operations
        return Operations(self).drop(column)

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
        from tablofy.transform.operations import Operations
        return Operations(self).rename(mapping)

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
        from tablofy.transform.operations import Operations
        return Operations(self).sort(by, descending=descending)

    def filter(self, expression: str) -> TablofyFrame:
        """Filter rows using a safe pandas expression.

        Parameters
        ----------
        expression : str
            A pandas query expression (e.g. ``"age > 25"``).

        Returns
        -------
        TablofyFrame
        """
        from tablofy.transform.safe_filter import SafeFilter
        return SafeFilter(self).filter(expression)

    def group(self, by: str) -> GroupedFrame:
        """Return a ``GroupedFrame`` for aggregation.

        Parameters
        ----------
        by : str
            Column to group by.

        Returns
        -------
        GroupedFrame
        """
        from tablofy.transform.group import GroupedFrame
        return GroupedFrame(self, by)

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
            Aggregation function (default ``"mean"``).

        Returns
        -------
        TablofyFrame
        """
        from tablofy.transform.operations import Operations
        return Operations(self).pivot(index, columns, values, aggfunc=aggfunc)

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
        from tablofy.transform.operations import Operations
        return Operations(self).join(other, on=on, how=how)

    def export(self, path: str, **kwargs) -> None:
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
        from tablofy.transform.operations import Operations
        Operations(self).export(path, **kwargs)

    # -- Visualization --------------------------------------------------------

    def bar(
        self,
        x: str,
        y: str,
        interactive: bool = False,
        save: str | None = None,
        **kwargs,
    ):
        """Bar chart of *x* vs *y*.

        Parameters
        ----------
        x : str
            Column for the x-axis (categories).
        y : str
            Column for the y-axis (values).
        interactive : bool
            If True, render an interactive Plotly chart (requires ``tablofy[viz]``).
        save : str or None
            File path to save the figure (PNG for static, HTML for interactive).

        Returns
        -------
        matplotlib.figure.Figure or plotly.graph_objects.Figure
        """
        from tablofy.visualization.charts import Charts
        return Charts(self).bar(x, y, interactive=interactive, save=save, **kwargs)

    def line(
        self,
        x: str,
        y: str,
        interactive: bool = False,
        save: str | None = None,
        **kwargs,
    ):
        """Line chart of *x* vs *y*.

        Parameters
        ----------
        x : str
            Column for the x-axis.
        y : str
            Column for the y-axis.
        interactive : bool
            If True, render an interactive Plotly chart.
        save : str or None
            File path to save the figure.

        Returns
        -------
        matplotlib.figure.Figure or plotly.graph_objects.Figure
        """
        from tablofy.visualization.charts import Charts
        return Charts(self).line(x, y, interactive=interactive, save=save, **kwargs)

    def scatter(
        self,
        x: str,
        y: str,
        interactive: bool = False,
        save: str | None = None,
        **kwargs,
    ):
        """Scatter plot of *x* vs *y*.

        Parameters
        ----------
        x : str
            Column for the x-axis.
        y : str
            Column for the y-axis.
        interactive : bool
            If True, render an interactive Plotly chart.
        save : str or None
            File path to save the figure.

        Returns
        -------
        matplotlib.figure.Figure or plotly.graph_objects.Figure
        """
        from tablofy.visualization.charts import Charts
        return Charts(self).scatter(x, y, interactive=interactive, save=save, **kwargs)

    def hist(
        self,
        column: str,
        interactive: bool = False,
        save: str | None = None,
        **kwargs,
    ):
        """Histogram of *column*.

        Parameters
        ----------
        column : str
            Column to plot.
        interactive : bool
            If True, render an interactive Plotly chart.
        save : str or None
            File path to save the figure.

        Returns
        -------
        matplotlib.figure.Figure or plotly.graph_objects.Figure
        """
        from tablofy.visualization.charts import Charts
        return Charts(self).hist(column, interactive=interactive, save=save, **kwargs)

    def box(
        self,
        x: str,
        y: str,
        interactive: bool = False,
        save: str | None = None,
        **kwargs,
    ):
        """Box plot of *y* grouped by *x*.

        Parameters
        ----------
        x : str
            Column for grouping (categories).
        y : str
            Column for the values.
        interactive : bool
            If True, render an interactive Plotly chart.
        save : str or None
            File path to save the figure.

        Returns
        -------
        matplotlib.figure.Figure or plotly.graph_objects.Figure
        """
        from tablofy.visualization.charts import Charts
        return Charts(self).box(x, y, interactive=interactive, save=save, **kwargs)

    def heatmap(
        self,
        interactive: bool = False,
        save: str | None = None,
        **kwargs,
    ):
        """Correlation heatmap of all numeric columns.

        Parameters
        ----------
        interactive : bool
            If True, render an interactive Plotly chart.
        save : str or None
            File path to save the figure.

        Returns
        -------
        matplotlib.figure.Figure or plotly.graph_objects.Figure
        """
        from tablofy.visualization.charts import Charts
        return Charts(self).heatmap(interactive=interactive, save=save, **kwargs)

    def pairplot(
        self,
        interactive: bool = False,
        save: str | None = None,
        **kwargs,
    ):
        """Pairwise scatter matrix of all numeric columns.

        Parameters
        ----------
        interactive : bool
            If True, render an interactive Plotly chart.
        save : str or None
            File path to save the figure.

        Returns
        -------
        seaborn.PairGrid or plotly.graph_objects.Figure
        """
        from tablofy.visualization.charts import Charts
        return Charts(self).pairplot(interactive=interactive, save=save, **kwargs)

    def area(
        self,
        x: str,
        y: str,
        interactive: bool = False,
        save: str | None = None,
        **kwargs,
    ):
        """Area chart of *x* vs *y*.

        Parameters
        ----------
        x : str
            Column for the x-axis.
        y : str
            Column for the y-axis.
        interactive : bool
            If True, render an interactive Plotly chart.
        save : str or None
            File path to save the figure.

        Returns
        -------
        matplotlib.figure.Figure or plotly.graph_objects.Figure
        """
        from tablofy.visualization.charts import Charts
        return Charts(self).area(x, y, interactive=interactive, save=save, **kwargs)

    def pie(
        self,
        labels: str,
        values: str,
        interactive: bool = False,
        save: str | None = None,
        **kwargs,
    ):
        """Pie chart of *values* grouped by *labels*.

        Parameters
        ----------
        labels : str
            Column for slice labels.
        values : str
            Column for slice sizes.
        interactive : bool
            If True, render an interactive Plotly chart.
        save : str or None
            File path to save the figure.

        Returns
        -------
        matplotlib.figure.Figure or plotly.graph_objects.Figure
        """
        from tablofy.visualization.charts import Charts
        return Charts(self).pie(labels, values, interactive=interactive, save=save, **kwargs)

    def violin(
        self,
        x: str,
        y: str,
        interactive: bool = False,
        save: str | None = None,
        **kwargs,
    ):
        """Violin plot of *y* grouped by *x*.

        Parameters
        ----------
        x : str
            Column for grouping (categories).
        y : str
            Column for the values.
        interactive : bool
            If True, render an interactive Plotly chart.
        save : str or None
            File path to save the figure.

        Returns
        -------
        matplotlib.figure.Figure or plotly.graph_objects.Figure
        """
        from tablofy.visualization.charts import Charts
        return Charts(self).violin(x, y, interactive=interactive, save=save, **kwargs)

    def chart(self, description: str, **kwargs):
        """Generate a chart from a plain-English description.

        Supported patterns:
        - ``"sales by month"`` → bar or line chart
        - ``"profit vs ad_spend"`` → scatter plot

        Parameters
        ----------
        description : str
            Short description of the desired chart.

        Returns
        -------
        matplotlib.figure.Figure or seaborn.PairGrid
        """
        from tablofy.visualization.smart_chart import SmartChart
        kind, chart_kwargs = SmartChart(self).parse_chart(description)
        chart_kwargs.update(kwargs)
        method = getattr(self, kind)
        return method(**chart_kwargs)

    # -- Analytics ------------------------------------------------------------

    def insights(self) -> list[str]:
        """Return a list of deterministic, rule-based observations.

        Analyses the dataset for:
        - Missing values
        - Duplicate rows
        - Strong correlations
        - High / low cardinality columns
        - Min/max values
        - Outlier hints

        Returns
        -------
        list[str]
            Human-readable insight strings.
        """
        from tablofy.analytics.insights import Insights
        return Insights(self).generate()

    @property
    def ts(self):
        """Access time-series transformation helpers.

        Provides ``set_time_index``, ``resample``, ``rolling``, and
        ``detect_trend`` methods.
        """
        if self._ts is None:
            from tablofy.analytics.timeseries import TimeSeries
            self._ts = TimeSeries(self)
        return self._ts

    # -- SQL ------------------------------------------------------------------

    def sql(self, query: str) -> TablofyFrame:
        """Execute a read-only SQL query against the frame using DuckDB.

        The underlying DataFrame is registered as the table ``data`` inside
        an isolated in-memory DuckDB session.

        Parameters
        ----------
        query : str
            A read-only SQL query (SELECT, WITH, DESCRIBE, EXPLAIN).

        Returns
        -------
        TablofyFrame

        Raises
        ------
        TablofyDataError
            If the query is non-read-only, empty, or syntactically invalid.
        """
        from tablofy.sql.duckdb_query import DuckDBQuery
        return DuckDBQuery(self).execute(query)

    # -- Reporting ------------------------------------------------------------

    def report(
        self,
        path: str,
        charts: list[tuple[str, str]] | None = None,
        **kwargs,
    ) -> str:
        """Generate an HTML or Excel report.

        Parameters
        ----------
        path : str
            Destination file path (``.html`` or ``.xlsx``).
        charts : list[tuple[str, str]] or None
            Optional list of ``(title, file_path)`` pairs for chart images.

        Returns
        -------
        str
            Absolute path to the generated report.

        Raises
        ------
        TablofyFileError
            If the extension is not ``.html`` or ``.xlsx``.
        """
        ext = path.rsplit(".", 1)[-1].lower() if "." in path else ""
        if ext == "html":
            from tablofy.reports.html import HTMLReport
            return HTMLReport(self).generate(path, charts=charts, **kwargs)
        elif ext == "xlsx":
            from tablofy.reports.excel import ExcelReport
            return ExcelReport(self).generate(path, **kwargs)
        else:
            from tablofy.core.errors import TablofyFileError
            raise TablofyFileError(
                f"Unsupported report format: .{ext}. "
                f"Supported: .html, .xlsx"
            )

    def explore_interactive(self) -> None:
        """Launch an interactive widget dashboard inside a Jupyter notebook.

        Displays a column picker, real-time filters, a dynamic table preview,
        and an auto-updating chart.

        Requires ``ipywidgets``:
            pip install tablofy[widgets]

        Falls back gracefully with a printed message outside of notebooks.
        """
        from tablofy.core.widgets import explore_interactive as _explore

        _explore(self)

    # -- Escape hatch ---------------------------------------------------------

    def to_pandas(self) -> pd.DataFrame:
        """Return the underlying pandas DataFrame."""
        return self._df

    def __getitem__(self, key):
        """Allows square-bracket access to columns from the underlying DataFrame.

        If *key* is a string, returns the pandas Series directly.
        If *key* is a list, returns a new TablofyFrame with those columns.
        """
        result = self._df[key]
        if isinstance(result, pd.DataFrame):
            return TablofyFrame(result, name=self.name)
        return result

    def __repr__(self) -> str:
        return f"<TablofyFrame '{self.name}' shape=({self._df.shape[0]}, {self._df.shape[1]})>"

    def __len__(self) -> int:
        return self._df.shape[0]

    def _repr_html_(self) -> str:
        """Render an HTML table for Jupyter Notebook display."""
        return self._df._repr_html_()

    def __getattr__(self, name: str):
        """Delegate unknown attribute access to the underlying DataFrame.

        If the attribute is a callable (method) and its return value is a
        ``pd.DataFrame``, it is automatically wrapped in a ``TablofyFrame``
        so that chaining continues to work.
        """
        attr = getattr(self._df, name)
        if callable(attr):
            def wrapper(*args, **kwargs):
                result = attr(*args, **kwargs)
                if isinstance(result, pd.DataFrame):
                    return TablofyFrame(result, name=self.name)
                return result
            return wrapper
        return attr
