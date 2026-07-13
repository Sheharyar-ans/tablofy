"""File loading and export dispatch."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from tablofy.core.errors import TablofyFileError
from tablofy.utils.validation import Validator


def load(path: str | Path, **kwargs: Any):
    """Load a file into a ``TablofyFrame``.

    Supported formats: CSV, Excel (.xlsx, .xls), JSON, Parquet.

    Parameters
    ----------
    path : str | Path
        Path to the file.
    **kwargs
        Passed to the underlying pandas reader.

    Returns
    -------
    TablofyFrame

    Raises
    ------
    TablofyFileError
        If the file is not found or format is unsupported.
    """
    from tablofy.core.frame import TablofyFrame

    p = Path(path)
    suffix = p.suffix.lower()

    Validator.assert_file_exists(p)
    Validator.assert_supported_format(suffix)

    name = p.stem

    if suffix == ".csv":
        import pandas as pd
        df = pd.read_csv(p, **kwargs)
    elif suffix in (".xlsx", ".xls"):
        import pandas as pd
        df = pd.read_excel(p, **kwargs)
    elif suffix == ".json":
        import pandas as pd
        df = pd.read_json(p, **kwargs)
    elif suffix == ".parquet":
        import pandas as pd
        df = pd.read_parquet(p, **kwargs)
    else:
        raise TablofyFileError(
            f"Unsupported file format '{suffix}'. "
            f"Supported: {', '.join(sorted(Validator.SUPPORTED_EXTENSIONS))}"
        )

    Validator.assert_not_empty(df, name=name)
    return TablofyFrame(df, name=name)
