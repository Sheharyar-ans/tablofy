"""Tests for visualization methods."""

import matplotlib
import matplotlib.figure
import pandas as pd
import pytest
import seaborn as sns

matplotlib.use("Agg")

from tablofy import TablofyFrame
from tablofy.core.errors import TablofyChartError, TablofyColumnError, TablofyDataError


class TestCharts:
    @pytest.fixture
    def frame(self):
        return TablofyFrame(
            pd.DataFrame({
                "month": ["Jan", "Feb", "Mar"],
                "sales": [100, 200, 150],
                "profit": [30, 50, 40],
            }),
        )

    @pytest.fixture
    def num_frame(self):
        return TablofyFrame(
            pd.DataFrame({
                "x": [1, 2, 3, 4, 5],
                "y": [10, 20, 15, 25, 30],
                "z": [5, 4, 3, 2, 1],
            }),
        )

    # -- bar -------------------------------------------------------------------

    def test_bar_returns_figure(self, frame):
        fig = frame.bar(x="month", y="sales")
        assert isinstance(fig, matplotlib.figure.Figure)

    def test_bar_missing_column_raises(self, frame):
        with pytest.raises(TablofyColumnError):
            frame.bar(x="nonexistent", y="sales")

    # -- line ------------------------------------------------------------------

    def test_line_returns_figure(self, frame):
        fig = frame.line(x="month", y="sales")
        assert isinstance(fig, matplotlib.figure.Figure)

    def test_line_missing_column_raises(self, frame):
        with pytest.raises(TablofyColumnError):
            frame.line(x="month", y="nonexistent")

    # -- scatter ---------------------------------------------------------------

    def test_scatter_returns_figure(self, frame):
        fig = frame.scatter(x="month", y="sales")
        assert isinstance(fig, matplotlib.figure.Figure)

    def test_scatter_missing_column_raises(self, frame):
        with pytest.raises(TablofyColumnError):
            frame.scatter(x="nonexistent", y="sales")

    # -- hist ------------------------------------------------------------------

    def test_hist_returns_figure(self, frame):
        fig = frame.hist("sales")
        assert isinstance(fig, matplotlib.figure.Figure)

    def test_hist_missing_column_raises(self, frame):
        with pytest.raises(TablofyColumnError):
            frame.hist("nonexistent")

    # -- box -------------------------------------------------------------------

    def test_box_returns_figure(self, frame):
        fig = frame.box(x="month", y="sales")
        assert isinstance(fig, matplotlib.figure.Figure)

    def test_box_missing_column_raises(self, frame):
        with pytest.raises(TablofyColumnError):
            frame.box(x="month", y="nonexistent")

    # -- heatmap ---------------------------------------------------------------

    def test_heatmap_returns_figure(self, num_frame):
        fig = num_frame.heatmap()
        assert isinstance(fig, matplotlib.figure.Figure)

    def test_heatmap_too_few_numeric_raises(self):
        single_num = TablofyFrame(pd.DataFrame({
            "label": ["a", "b", "c"],
            "value": [1.0, 2.0, 3.0],
        }))
        with pytest.raises(TablofyChartError):
            single_num.heatmap()

    # -- pairplot --------------------------------------------------------------

    def test_pairplot_returns_pairgrid(self, num_frame):
        pg = num_frame.pairplot()
        assert isinstance(pg, sns.PairGrid)

    def test_pairplot_too_few_numeric_raises(self):
        single_num = TablofyFrame(pd.DataFrame({
            "label": ["a", "b", "c"],
            "value": [1.0, 2.0, 3.0],
        }))
        with pytest.raises(TablofyChartError):
            single_num.pairplot()

    # -- save ------------------------------------------------------------------

    def test_bar_save_creates_file(self, frame, tmp_path):
        path = tmp_path / "bar.png"
        frame.bar(x="month", y="sales", save=str(path))
        assert path.exists()

    def test_line_save_creates_file(self, frame, tmp_path):
        path = tmp_path / "line.png"
        frame.line(x="month", y="sales", save=str(path))
        assert path.exists()

    def test_scatter_save_creates_file(self, frame, tmp_path):
        path = tmp_path / "scatter.png"
        frame.scatter(x="month", y="sales", save=str(path))
        assert path.exists()

    def test_heatmap_save_creates_file(self, num_frame, tmp_path):
        path = tmp_path / "heatmap.png"
        num_frame.heatmap(save=str(path))
        assert path.exists()


class TestSmartChart:
    @pytest.fixture
    def frame(self):
        return TablofyFrame(
            pd.DataFrame({
                "month": ["Jan", "Feb", "Mar"],
                "sales": [100, 200, 150],
                "profit": [30, 50, 40],
                "ad_spend": [10, 25, 20],
            }),
        )

    def test_chart_sales_by_month_returns_figure(self, frame):
        fig = frame.chart("sales by month")
        assert isinstance(fig, matplotlib.figure.Figure)

    def test_chart_profit_vs_ad_spend_returns_figure(self, frame):
        fig = frame.chart("profit vs ad_spend")
        assert isinstance(fig, matplotlib.figure.Figure)

    def test_chart_unparseable_raises(self, frame):
        with pytest.raises(TablofyDataError):
            frame.chart("some random description")

    def test_chart_empty_raises(self, frame):
        with pytest.raises(TablofyDataError):
            frame.chart("")

    def test_chart_missing_column_raises(self, frame):
        with pytest.raises(TablofyDataError):
            frame.chart("nonexistent vs sales")

    def test_chart_profit_vs_ad_spend_is_scatter(self, frame):
        fig = frame.chart("profit vs ad_spend")
        assert len(fig.axes) == 1
