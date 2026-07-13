"""HTML report generation via Jinja2."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

from jinja2 import Environment, FileSystemLoader

if TYPE_CHECKING:
    from tablofy.core.frame import TablofyFrame


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
        profile["duplicate_pct"] = round(
            profile["duplicate_rows"] / rows * 100, 2
        ) if rows else 0.0

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

        # Render template
        env = Environment(loader=FileSystemLoader(
            Path(__file__).parent / "templates"
        ))
        template = env.get_template("report.html")
        html = template.render(
            title=f"Report: {frame.name}",
            profile=profile,
            missing_table=missing_table,
            summary_table=summary_table,
            insight_list=insight_list,
            clean_actions=clean_actions,
            clean_summary=clean_summary,
            charts=charts or [],
        )

        path.write_text(html, encoding="utf-8")
        return str(path.resolve())
