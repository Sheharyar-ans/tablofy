"""Tablofy — A beginner-friendly data analytics library."""

__version__ = "2.0.0"

from tablofy.core.errors import (
    TablofyColumnError,
    TablofyDataError,
    TablofyError,
    TablofyFileError,
)
from tablofy.core.frame import TablofyFrame
from tablofy.core.loader import load

ColumnNotFoundError = TablofyColumnError
EmptyTableError = TablofyDataError
FileFormatError = TablofyFileError

__all__ = [
    "TablofyFrame",
    "load",
    "TablofyError",
    "TablofyFileError",
    "TablofyColumnError",
    "TablofyDataError",
    "ColumnNotFoundError",
    "EmptyTableError",
    "FileFormatError",
]
