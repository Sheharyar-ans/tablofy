"""Lazy import helpers to defer heavy module loads."""

from __future__ import annotations

import importlib
from types import ModuleType
from typing import Any


class LazyImporter:
    """Proxy that imports a module on first attribute access."""

    def __init__(self, module_name: str) -> None:
        self._module_name = module_name
        self._module: ModuleType | None = None

    def _load(self) -> ModuleType:
        if self._module is None:
            self._module = importlib.import_module(self._module_name)
        return self._module

    def __getattr__(self, name: str) -> Any:
        return getattr(self._load(), name)
