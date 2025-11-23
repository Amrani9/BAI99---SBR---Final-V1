"""Simple TSP heuristic solvers."""
from __future__ import annotations

from typing import List, Sequence


def nearest_neighbor_tsp(distance_matrix: Sequence[Sequence[float]], start: int = 0) -> List[int]:
    """Compute a TSP path using the nearest-neighbor heuristic.

    Parameters
    ----------
    distance_matrix: matrix of pairwise distances (assumed symmetric)
    start: starting index

    Returns
    -------
    List of node indices representing the visitation order.
    """

    n = len(distance_matrix)
    if n == 0:
        return []

    start = max(0, min(start, n - 1))
    visited = [False] * n
    path: List[int] = [start]
    visited[start] = True

    current = start
    for _ in range(n - 1):
        neighbors = distance_matrix[current]
        next_idx = None
        next_distance = float("inf")
        for idx, distance in enumerate(neighbors):
            if visited[idx] or idx == current:
                continue
            if distance < next_distance:
                next_distance = distance
                next_idx = idx

        if next_idx is None:
            break

        path.append(next_idx)
        visited[next_idx] = True
        current = next_idx

    return path
