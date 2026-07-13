"""Tests for report generation."""

import pandas as pd
import pytest

from tablofy import TablofyFrame
from tablofy.core.errors import TablofyFileError


class TestReports:
    @pytest.fixture
    def frame(self):
        return TablofyFrame(
            pd.DataFrame({
                "month": ["Jan", "Feb"],
                "sales": [100, 200],
            }),
        )

    def test_html_report(self, frame, tmp_path):
        path = tmp_path / "report.html"
        result = frame.report(str(path))
        assert path.exists()
        assert result == str(path.resolve())

    def test_excel_report(self, frame, tmp_path):
        path = tmp_path / "report.xlsx"
        frame.report(str(path))
        assert path.exists()

    def test_unsupported_extension_raises(self, frame, tmp_path):
        with pytest.raises(TablofyFileError):
            frame.report(str(tmp_path / "report.pdf"))
