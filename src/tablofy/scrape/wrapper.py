"""Lazy-loaded web-scraping wrapper (BeautifulSoup, Requests, Scrapy)."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tablofy.core.frame import TablofyFrame


class ScrapeWrapper:
    """Entry point for web-scraping operations on a TablofyFrame.

    Accessed via ``data.scrape``.

    Requires ``tablofy[scraping]`` (beautifulsoup4, requests, scrapy).
    """

    def __init__(self, frame: TablofyFrame) -> None:
        self._frame = frame
        self._df = frame._df

    def _check_imports(self) -> None:
        try:
            import bs4  # noqa: F401
            import requests  # noqa: F401
        except ImportError:
            raise ImportError(
                "beautifulsoup4 and requests are required for scraping features.\n"
                "  pip install tablofy[scraping]"
            ) from None
