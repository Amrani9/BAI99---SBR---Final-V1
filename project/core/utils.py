"""Shared utility helpers."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict


def utcnow() -> datetime:
    """Return a timezone-aware UTC datetime."""

    return datetime.now(timezone.utc)


def to_dict(obj: Any, fields: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """Convert an object with attributes to a dictionary representation."""

    if fields is None:
        fields = {}

    data: Dict[str, Any] = {}
    for attr in dir(obj):
        if attr.startswith("_") or callable(getattr(obj, attr)):
            continue
        if fields and attr not in fields:
            continue
        try:
            data[attr] = getattr(obj, attr)
        except Exception:
            # Best-effort serialization; skip attributes that raise
            continue
    return data
