"""Excel report generation with multiple sheets."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

import pandas as pd

if TYPE_CHECKING:
    from tablofy.core.frame import TablofyFrame


class ExcelReport:
    """Generates a multi-sheet Excel report (Data, Summary, Missing, Insights, Cleaning)."""

    def __init__(self, frame: TablofyFrame) -> None:
        self._frame = frame
        self._df = frame._df

    def generate(
        self,
        path: str | Path,
        **kwargs: Any,
    ) -> str:
        """Write the report to *path* and return the absolute path."""
        frame = self._frame
        df = self._df
        path = Path(path)

        with pd.ExcelWriter(path, engine="openpyxl") as writer:
            # Data
            df.to_excel(writer, sheet_name="Data", index=False)

            # Summary
            summary = df.describe(include="all")
            summary.to_excel(writer, sheet_name="Summary")

            # Missing Values
            missing = frame.missing()
            if len(missing):
                missing.to_excel(writer, sheet_name="Missing Values", index=False)
            else:
                pd.DataFrame({"message": ["No missing values found."]}).to_excel(
                    writer, sheet_name="Missing Values", index=False
                )

            # Insights
            insights = frame.insights()
            pd.DataFrame({"insight": insights}).to_excel(
                writer, sheet_name="Insights", index=False
            )

            # Cleaning Report
            clean = frame.clean_report()
            if clean["actions"]:
                pd.DataFrame(clean["actions"]).to_excel(
                    writer, sheet_name="Cleaning Report", index=False
                )
            else:
                pd.DataFrame({"message": [clean["summary_text"]]}).to_excel(
                    writer, sheet_name="Cleaning Report", index=False
                )

        return str(path.resolve())
