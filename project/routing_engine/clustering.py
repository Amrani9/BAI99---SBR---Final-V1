"""Clustering heuristics for student stops and bus capacity."""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable, List, Sequence


@dataclass
class Stop:
    """Simple representation of a pickup/drop-off location."""

    id: str | int | None
    name: str
    lat: float
    lng: float
    address: str | None = None


Coord = tuple[float, float]


def _bearing(origin: Coord, dest: Coord) -> float:
    """Compute the bearing from origin to destination in radians."""

    oy, ox = origin
    dy, dx = dest
    return math.atan2(dy - oy, dx - ox)


def cluster_students(
    school: Coord,
    students: Iterable[Stop],
    bus_count: int,
    capacity: int,
) -> List[List[Stop]]:
    """Group students into clusters using a radial sweep heuristic.

    Students are sorted by their bearing relative to the school to keep
    geographically close stops together. They are then assigned to the least
    loaded cluster that still has room, approximating a capacity-aware sweep.
    """

    students_list: List[Stop] = list(students)
    if bus_count <= 0:
        bus_count = max(1, math.ceil(len(students_list) / max(1, capacity)))

    clusters: List[List[Stop]] = [[] for _ in range(bus_count)]
    if not students_list:
        return clusters

    sorted_students = sorted(
        students_list, key=lambda s: _bearing(school, (s.lat, s.lng))
    )

    for student in sorted_students:
        # Prefer clusters under capacity; otherwise fall back to the least loaded one.
        target_idx = min(
            range(bus_count),
            key=lambda idx: (
                len(clusters[idx]) >= capacity,  # avoid full clusters when possible
                len(clusters[idx]),
            ),
        )
        clusters[target_idx].append(student)

    return clusters


def flatten_clusters(clusters: Sequence[Sequence[Stop]]) -> List[Stop]:
    """Flatten a nested cluster list into a single list of stops."""

    return [stop for cluster in clusters for stop in cluster]
