"""Custom exception classes for Tablofy."""


class TablofyError(Exception):
    """Base exception for all Tablofy errors."""


class TablofyFileError(TablofyError):
    """Raised when a file operation fails (not found, unsupported format)."""


class TablofyColumnError(TablofyError):
    """Raised when a requested column does not exist."""


class TablofyDataError(TablofyError):
    """Raised on invalid data (empty dataset, coercion failure)."""


class TablofyChartError(TablofyError):
    """Raised when a chart operation is invalid."""


class TablofyParseError(TablofyError):
    """Raised when parsing a user string (e.g. chart description) fails."""
