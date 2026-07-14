"""Tablofy — A beginner-friendly data analytics library."""

import logging

from tablofy.core.errors import (
    TablofyColumnError,
    TablofyDataError,
    TablofyError,
    TablofyFileError,
)
from tablofy.core.frame import TablofyFrame
from tablofy.core.loader import load, load_web
from tablofy.visualization.styles import set_theme

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

__version__ = "2.1.3"

try:
    import pandas as pd
except ImportError:
    pd = None

try:
    import numpy as np
except ImportError:
    np = None


def show(*args, **kwargs):
    """Displays all active matplotlib/seaborn figures without importing plt."""
    try:
        import matplotlib.pyplot as plt
        plt.show(*args, **kwargs)
    except ImportError:
        raise ImportError("Matplotlib is required to use tf.show(). Please install it.")


ColumnNotFoundError = TablofyColumnError
EmptyTableError = TablofyDataError
FileFormatError = TablofyFileError

__all__ = ["TablofyFrame", "load", "load_web", "show", "pd", "np"]
