"""Dataset profiler."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tablofy.core.frame import TablofyFrame


class Profiler:
    """Builds a high-level profile of a dataset."""

    def __init__(self, frame: TablofyFrame) -> None:
        self._frame = frame
        self._df = frame._df

    def run(self) -> dict:
        """Return a comprehensive profile dict.

        Keys: rows, columns, total_cells, missing_cells, missing_percent,
        duplicate_rows, numeric_columns, text_columns, date_columns,
        categorical_columns, memory_usage.
        """
        df = self._df
        rows, cols = df.shape
        total_cells = rows * cols

        missing_mask = df.isna()
        missing_cells = int(missing_mask.sum().sum())
        missing_percent = round(missing_cells / total_cells * 100, 2) if total_cells else 0.0

        duplicate_rows = int(df.duplicated().sum())

        numeric_columns = list(df.select_dtypes(include=["number"]).columns)
        date_columns = list(df.select_dtypes(include=["datetime", "timedelta"]).columns)
        categorical_columns = list(df.select_dtypes(include=["category", "bool"]).columns)

        text_dtypes = ["object", "string"]
        text_columns = [
            col for col in df.columns
            if str(df[col].dtype) in text_dtypes
        ]

        memory_usage = int(df.memory_usage(deep=True).sum())

        return {
            "rows": rows,
            "columns": cols,
            "total_cells": total_cells,
            "missing_cells": missing_cells,
            "missing_percent": missing_percent,
            "duplicate_rows": duplicate_rows,
            "numeric_columns": numeric_columns,
            "text_columns": text_columns,
            "date_columns": date_columns,
            "categorical_columns": categorical_columns,
            "memory_usage": memory_usage,
        }
