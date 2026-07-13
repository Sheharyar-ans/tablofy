"""Cleaning report generator."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tablofy.core.frame import TablofyFrame


class CleanReport:
    """Summarises the most recent cleaning run."""

    def __init__(self, frame: TablofyFrame) -> None:
        self._frame = frame

    def summary(self) -> dict:
        """Return a dict with actions, action_count, and summary_text."""
        actions = self._frame._last_clean_actions
        count = len(actions)
        if count:
            summary_text = f"Cleaning completed: {count} action(s) performed."
        else:
            summary_text = "No cleaning operations recorded."
        return {
            "actions": actions,
            "action_count": count,
            "summary_text": summary_text,
        }
