"""Tablofy — A beginner-friendly data analytics library."""

__version__ = "1.0.0-alpha"

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
