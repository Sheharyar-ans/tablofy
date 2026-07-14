"""Tablofy — A beginner-friendly data analytics library."""

__version__ = "2.1.0"

from tablofy.core.errors import (
    TablofyColumnError,
    TablofyDataError,
    TablofyError,
    TablofyFileError,
)
from tablofy.core.frame import TablofyFrame
from tablofy.core.loader import load
from tablofy.visualization.styles import set_theme

ColumnNotFoundError = TablofyColumnError
EmptyTableError = TablofyDataError
FileFormatError = TablofyFileError

__all__ = [
    "TablofyFrame",
    "load",
    "set_theme",
    "TablofyError",
    "TablofyFileError",
    "TablofyColumnError",
    "TablofyDataError",
    "ColumnNotFoundError",
    "EmptyTableError",
    "FileFormatError",
]
