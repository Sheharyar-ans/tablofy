"""Data cleaning operations."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pandas as pd

from tablofy.utils.formatting import Formatter

if TYPE_CHECKING:
    from tablofy.core.frame import TablofyFrame


class Cleaner:
    """Performs cleaning operations on a TablofyFrame in-place."""

    def __init__(self, frame: TablofyFrame) -> None:
        self._frame = frame
        self.actions: list[dict[str, Any]] = []

    def run(
        self,
        duplicates: bool = True,
        missing: str | dict = "smart",
        columns: str | bool = "snake_case",
        dates: bool = True,
        text: bool = True,
    ) -> TablofyFrame:
        """Execute the cleaning pipeline and return the frame."""
        self.actions = []
        df = self._frame._df

        # 1. Remove duplicate rows
        if duplicates:
            before = len(df)
            df.drop_duplicates(inplace=True)
            removed = before - len(df)
            if removed:
                self.actions.append({
                    "action": "duplicates",
                    "message": f"Removed {removed} duplicate row(s).",
                })

        # 2. Remove fully empty columns
        empty_cols = [col for col in df.columns if df[col].isna().all()]
        if empty_cols:
            df.drop(columns=empty_cols, inplace=True)
            self.actions.append({
                "action": "empty_columns",
                "message": f"Removed {len(empty_cols)} fully empty column(s): {empty_cols}.",
            })

        # 3. Clean column names to snake_case
        if columns == "snake_case":
            renamed = {}
            for col in df.columns:
                clean = Formatter.to_snake_case(col)
                if clean != col:
                    renamed[col] = clean
            if renamed:
                df.rename(columns=renamed, inplace=True)
                self.actions.append({
                    "action": "column_names",
                    "message": f"Renamed {len(renamed)} column(s) to snake_case.",
                })

        # 4. Strip whitespace from text columns
        if text:
            stripped_cols = []
            text_cols = df.select_dtypes(include=["object"]).columns
            for col in text_cols:
                before_strip = df[col].astype(str).str.strip()
                df[col] = df[col].astype(str).str.strip()
                df[col] = df[col].replace(["nan", "None", ""], None)
                if not df[col].equals(before_strip):
                    stripped_cols.append(col)
            if stripped_cols:
                self.actions.append({
                    "action": "whitespace",
                    "message": f"Stripped whitespace from {len(stripped_cols)} text column(s).",
                })

        # 5. Smart fill missing values
        if missing == "smart":
            filled_cols = []
            for col in df.columns:
                if df[col].isna().any():
                    if pd.api.types.is_numeric_dtype(df[col]):
                        median_val = df[col].median()
                        if pd.notna(median_val):
                            df[col] = df[col].fillna(median_val)
                            filled_cols.append(col)
                    else:
                        mode_vals = df[col].mode()
                        if len(mode_vals):
                            fill_val = mode_vals[0] if pd.notna(mode_vals[0]) else ""
                            df[col] = df[col].fillna(fill_val)
                            filled_cols.append(col)
            if filled_cols:
                self.actions.append({
                    "action": "missing_values",
                    "message": f"Smart-filled {len(filled_cols)} column(s): {filled_cols}.",
                })
        elif isinstance(missing, dict):
            df.fillna(missing, inplace=True)
            self.actions.append({
                "action": "missing_values",
                "message": f"Filled missing values using explicit mapping: {missing}.",
            })

        # 6. Date parsing
        if dates:
            parsed_cols = []
            for col in df.select_dtypes(include=["object"]).columns:
                sample = df[col].dropna().head(20)
                if len(sample) < 2:
                    continue
                try:
                    pd.to_datetime(sample, errors="raise")
                    df[col] = pd.to_datetime(df[col], errors="coerce")
                    parsed_cols.append(col)
                except (ValueError, TypeError):
                    pass
            if parsed_cols:
                self.actions.append({
                    "action": "date_parsing",
                    "message": f"Parsed {len(parsed_cols)} date column(s): {parsed_cols}.",
                })

        self._frame._df = df
        return self._frame
