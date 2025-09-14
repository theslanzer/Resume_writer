import tomllib             # tomli for <3.11
from pathlib import Path
from typing import Any

_cfg_cache: dict[str, Any] | None = None

def load(path: str | Path = "settings.toml") -> dict[str, Any]:
    global _cfg_cache
    if _cfg_cache is None:
        with open(path, "rb") as f:
            _cfg_cache = tomllib.load(f)
    return _cfg_cache
