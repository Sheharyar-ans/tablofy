"""Package-level configuration constants."""

SUPPORTED_EXTENSIONS: frozenset[str] = frozenset({
    ".csv",
    ".xlsx",
    ".xls",
    ".json",
    ".parquet",
})

REPORT_EXTENSIONS: frozenset[str] = frozenset({".html", ".xlsx"})
