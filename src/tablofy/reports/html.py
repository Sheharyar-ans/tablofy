"""HTML report generation via Jinja2."""

from __future__ import annotations

import math
from importlib import resources as importlib_resources
from pathlib import Path
from typing import TYPE_CHECKING, Any

import numpy as np
from jinja2 import Environment

if TYPE_CHECKING:
    from tablofy.core.frame import TablofyFrame


def _sanitize_for_jinja(obj: Any) -> Any:
    """Recursively sanitize an object for safe Jinja2 rendering.

    - Replaces NaN / NaT / Inf with an empty string.
    - Converts NumPy types to native Python types.
    """
    if isinstance(obj, dict):
        return {k: _sanitize_for_jinja(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_sanitize_for_jinja(v) for v in obj]
    if isinstance(obj, tuple):
        return tuple(_sanitize_for_jinja(v) for v in obj)
    if isinstance(obj, float):
        return "" if (math.isnan(obj) or math.isinf(obj)) else obj
    if isinstance(obj, np.floating):
        val = float(obj)
        return "" if math.isnan(val) else val
    if isinstance(obj, np.integer):
        return int(obj)
    if isinstance(obj, np.bool_):
        return bool(obj)
    if isinstance(obj, np.ndarray):
        return _sanitize_for_jinja(obj.tolist())
    return obj


class HTMLReport:
    """Generates a self-contained HTML report with optional chart images."""

    def __init__(self, frame: TablofyFrame) -> None:
        self._frame = frame

    def generate(
        self,
        path: str | Path,
        charts: list[tuple[str, str]] | None = None,
        **kwargs: Any,
    ) -> str:
        """Write the report to *path* and return the absolute path."""
        frame = self._frame
        path = Path(path)

        # Profile
        profile = frame.profile()
        rows = profile["rows"]
        profile["missing_pct"] = profile["missing_percent"]
        profile["duplicate_pct"] = (
            round(profile["duplicate_rows"] / rows * 100, 2) if rows else 0.0
        )

        # Missing values table as HTML
        missing_df = frame.missing()
        missing_table = missing_df.to_html(index=False) if len(missing_df) else None

        # Summary statistics as HTML
        summary_df = frame.summary()
        summary_table = summary_df.to_html() if len(summary_df) else None

        # Insights
        insight_list = frame.insights()

        # Cleaning report
        clean = frame.clean_report()
        clean_actions = clean["actions"]
        clean_summary = clean["summary_text"]

        # Load the Jinja2 template via importlib.resources
        try:
            template_source = (
                importlib_resources.files("tablofy.reports.templates")
                .joinpath("report.html")
                .read_text(encoding="utf-8")
            )
        except Exception as exc:
            raise RuntimeError(
                f"Failed to load the HTML report template from the installed "
                f"tablofy package: {exc}"
            ) from exc

        template = Environment().from_string(template_source)

        # Render template with sanitised data
        try:
            html = template.render(
                title=f"Report: {frame.name}",
                profile=_sanitize_for_jinja(profile),
                missing_table=missing_table,
                summary_table=summary_table,
                insight_list=insight_list,
                clean_actions=clean_actions,
                clean_summary=clean_summary,
                charts=charts or [],
            )
        except Exception as exc:
            raise RuntimeError(
                f"Failed to render the HTML report for '{path.name}'. "
                f"This may be caused by non-serialisable data (e.g. NaN, "
                f"NumPy types) in the report content: {exc}"
            ) from exc

        # Write to file
        try:
            path.write_text(html, encoding="utf-8")
        except OSError as exc:
            raise RuntimeError(
                f"Could not write the HTML report to '{path}'. "
                f"Please check that the directory exists and is writable: {exc}"
            ) from exc

        return str(path.resolve())
