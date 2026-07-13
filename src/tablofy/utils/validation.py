"""Input validation helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from tablofy.core.errors import TablofyColumnError, TablofyDataError, TablofyFileError


class Validator:
    """Collection of static validation methods."""

    SUPPORTED_EXTENSIONS: frozenset[str] = frozenset({
        ".csv",
        ".xlsx",
        ".xls",
        ".json",
        ".parquet",
    })

    @staticmethod
    def assert_file_exists(path: Path) -> None:
        """Raise TablofyFileError if *path* does not exist."""
        if not path.exists():
            raise TablofyFileError(f"File not found: {path}")
        if not path.is_file():
            raise TablofyFileError(f"Path is not a file: {path}")

    @staticmethod
    def assert_supported_format(suffix: str) -> None:
        """Raise TablofyFileError if *suffix* is not a supported format."""
        if suffix not in Validator.SUPPORTED_EXTENSIONS:
            raise TablofyFileError(
                f"Unsupported file format '{suffix}'. "
                f"Supported: {', '.join(sorted(Validator.SUPPORTED_EXTENSIONS))}"
            )

    @staticmethod
    def assert_not_empty(df: pd.DataFrame, name: str = "dataset") -> None:
        """Raise TablofyDataError if *df* is empty."""
        if df.empty:
            raise TablofyDataError(f"{name} is empty after loading.")

    @staticmethod
    def assert_columns_exist(
        df: pd.DataFrame,
        columns: list[str],
        label: str = "DataFrame",
    ) -> None:
        """Raise TablofyColumnError if any *columns* are missing from *df*."""
        missing = [c for c in columns if c not in df.columns]
        if missing:
            raise TablofyColumnError(
                f"Columns {missing} not found in {label}. "
                f"Available: {list(df.columns)}"
            )

    @staticmethod
    def coerce_dataframe(data: Any) -> pd.DataFrame:
        """Convert common types to DataFrame or raise TablofyDataError."""
        if isinstance(data, pd.DataFrame):
            return data
        if isinstance(data, dict):
            return pd.DataFrame(data)
        if isinstance(data, list):
            return pd.DataFrame(data)
        raise TablofyDataError(f"Cannot coerce {type(data).__name__} to DataFrame.")
