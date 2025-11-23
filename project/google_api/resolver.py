"""Higher-level helpers that combine geocoding and distance matrix operations."""
from __future__ import annotations

from typing import Dict, Iterable, List, Optional

from .geocode import geocode_address


EMPTY_COORD = {"lat": None, "lng": None, "source": "unresolved"}


def normalize_address(address: Optional[str]) -> str:
    """Normalize an address string to improve deduplication and lookup."""

    if not address:
        return ""
    return " ".join(address.strip().split()).title()


def resolve_student_addresses(students: Iterable[object]) -> List[Dict[str, object]]:
    """Resolve a collection of students to coordinates.

    The objects in ``students`` should expose an ``address`` attribute.
    Returns a list of dictionaries with ``student`` and ``location`` keys.
    """

    resolved: List[Dict[str, object]] = []
    for student in students:
        address = normalize_address(getattr(student, "address", ""))
        location = geocode_address(address) if address else EMPTY_COORD
        resolved.append({"student": student, "location": location or EMPTY_COORD})
    return resolved
