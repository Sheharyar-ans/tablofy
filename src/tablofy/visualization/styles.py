"""Global theme/style manager for Tablofy charts.

Usage
-----
>>> import tablofy as tf
>>> tf.set_theme("dark")
>>> tf.set_theme("pastel", palette=["#ff9999", "#66b3ff", "#99ff99"])
"""

from __future__ import annotations

from typing import Any

_active_config: dict[str, Any] = {
    "theme": "default",
}

# ---------------------------------------------------------------------------
#  Built-in theme definitions
# ---------------------------------------------------------------------------

_THEMES: dict[str, dict[str, Any]] = {
    "default": {
        "rcparams": {},
        "seaborn_palette": "muted",
        "plotly_template": None,
    },
    "modern": {
        "rcparams": {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "DejaVu Sans", "Helvetica"],
            "axes.edgecolor": "#333333",
            "axes.grid": True,
            "grid.color": "#d0d0d0",
            "grid.alpha": 0.6,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
        },
        "seaborn_palette": "muted",
        "plotly_template": "plotly_white",
    },
    "dark": {
        "rcparams": {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "DejaVu Sans", "Helvetica"],
            "text.color": "#e0e0e0",
            "axes.edgecolor": "#555555",
            "axes.labelcolor": "#e0e0e0",
            "xtick.color": "#e0e0e0",
            "ytick.color": "#e0e0e0",
            "axes.grid": True,
            "grid.color": "#444444",
            "grid.alpha": 0.5,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "figure.facecolor": "#1e1e1e",
            "axes.facecolor": "#2d2d2d",
        },
        "seaborn_palette": "viridis",
        "plotly_template": "plotly_dark",
    },
    "classic": {
        "rcparams": {
            "font.family": "serif",
            "font.serif": ["Times New Roman", "DejaVu Serif"],
            "axes.grid": False,
            "axes.spines.top": True,
            "axes.spines.right": True,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
        },
        "seaborn_palette": "deep",
        "plotly_template": "ggplot2",
    },
    "pastel": {
        "rcparams": {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "DejaVu Sans", "Helvetica"],
            "axes.grid": True,
            "grid.color": "#e0e0e0",
            "grid.alpha": 0.7,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "figure.facecolor": "white",
            "axes.facecolor": "#fafafa",
        },
        "seaborn_palette": "pastel",
        "plotly_template": "plotly_white",
    },
}


def _apply_mpl_theme(theme: dict[str, Any]) -> None:
    """Apply matplotlib rcParams and seaborn palette from a theme dict."""
    import matplotlib as mpl

    mpl.rcParams.update(theme["rcparams"])

    import seaborn as sns

    sns.set_palette(theme["seaborn_palette"])


def set_theme(theme_name: str, palette: list[str] | None = None) -> None:
    """Set the global chart theme for all Tablofy visualisations.

    Parameters
    ----------
    theme_name : str
        One of ``"modern"``, ``"dark"``, ``"classic"``, ``"pastel"``,
        or ``"default"``.
    palette : list of str, optional
        Custom colour palette (list of hex codes). Overrides the theme's
        default palette when provided.

    Raises
    ------
    ValueError
        If *theme_name* is not recognised.
    """
    theme = _THEMES.get(theme_name)
    if theme is None:
        raise ValueError(
            f"Unknown theme {theme_name!r}. "
            f"Available: {', '.join(_THEMES)}"
        )

    # If the user provided a custom palette, override the theme's default
    if palette is not None:
        theme = {**theme, "seaborn_palette": palette}

    _apply_mpl_theme(theme)
    _active_config["theme"] = theme_name


def get_plotly_template() -> str | None:
    """Return the Plotly template name for the currently active theme."""
    theme_name = _active_config["theme"]
    theme = _THEMES.get(theme_name)
    if theme is None:
        return None
    return theme["plotly_template"]
