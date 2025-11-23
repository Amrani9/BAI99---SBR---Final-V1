"""Lightweight Google Maps API wrappers with optional offline mode."""

from .geocode import geocode_address
from .matrix import distance_matrix
from .resolver import normalize_address, resolve_student_addresses

__all__ = [
    "geocode_address",
    "distance_matrix",
    "normalize_address",
    "resolve_student_addresses",
]
