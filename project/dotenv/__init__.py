"""Lightweight fallback implementation of ``python-dotenv``'s ``load_dotenv``.

This is provided so the application can boot in environments where the third-party
package is unavailable (e.g., offline CI). It supports a minimal subset: reading
key=value pairs from a file and setting them in ``os.environ`` when not already
set.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Union


def load_dotenv(path: Union[str, Path] | None = None, encoding: str = "utf-8") -> bool:
    env_path = Path(path) if path is not None else Path(".env")
    if not env_path.exists():
        return False

    content = env_path.read_text(encoding=encoding)
    for raw_line in content.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())
    return True


__all__ = ["load_dotenv"]
