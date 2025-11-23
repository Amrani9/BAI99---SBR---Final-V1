"""Distance matrix helpers."""
from __future__ import annotations

import json
import math
import urllib.parse
import urllib.request
from typing import List, Optional, Sequence, Tuple

from config import get_settings

Coordinate = Tuple[float, float]


def _haversine(origin: Coordinate, destination: Coordinate) -> float:
    """Approximate distance between two coordinates in kilometers."""

    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371.0

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.asin(math.sqrt(a))
    return radius * c


def _mock_matrix(origins: Sequence[Coordinate], destinations: Sequence[Coordinate]) -> List[List[float]]:
    """Generate a symmetric mock matrix using haversine distances."""

    matrix: List[List[float]] = []
    for origin in origins:
        row = []
        for dest in destinations:
            row.append(round(_haversine(origin, dest), 3))
        matrix.append(row)
    return matrix


def distance_matrix(
    origins: Sequence[Coordinate],
    destinations: Optional[Sequence[Coordinate]] = None,
    api_key: Optional[str] = None,
    mode: str = "driving",
    units: str = "metric",
    timeout: float = 5.0,
) -> List[List[float]]:
    """Call the Google Distance Matrix API or fall back to a mock implementation."""

    if destinations is None:
        destinations = origins

    settings = get_settings()
    key = api_key or settings.google_api_key

    if not key:
        return _mock_matrix(origins, destinations)

    origin_param = "|".join(
        f"{lat},{lng}" for lat, lng in origins
    )
    destination_param = "|".join(
        f"{lat},{lng}" for lat, lng in destinations
    )
    params = urllib.parse.urlencode(
        {
            "origins": origin_param,
            "destinations": destination_param,
            "mode": mode,
            "units": units,
            "key": key,
        }
    )
    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?{params}"

    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:  # nosec: B310
            payload = resp.read()
    except Exception:
        return _mock_matrix(origins, destinations)

    body = json.loads(payload)
    rows = body.get("rows", [])
    matrix: List[List[float]] = []
    for row in rows:
        entries = []
        for element in row.get("elements", []):
            if element.get("status") == "OK":
                distance_meters = element.get("distance", {}).get("value", 0)
                entries.append(round(distance_meters / 1000.0, 3))
            else:
                entries.append(float("inf"))
        matrix.append(entries)

    if not matrix:
        return _mock_matrix(origins, destinations)

    return matrix
