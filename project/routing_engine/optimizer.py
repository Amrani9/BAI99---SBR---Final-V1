"""Route optimization orchestration."""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, Iterable, List, Literal, Sequence

from .clustering import Stop, cluster_students
from .tsp import nearest_neighbor_tsp

Coord = tuple[float, float]


@dataclass
class School:
    name: str
    lat: float
    lng: float


@dataclass
class RoutePlan:
    bus_id: str
    stops: List[Stop]
    distance_km: float
    duration_min: float
    fuel_liters: float
    used_seats: int
    capacity: int


@dataclass
class OptimizationResult:
    summary: Dict[str, float | str]
    routes: List[RoutePlan]


DEFAULT_SPEED_KMH = 35.0
DEFAULT_FUEL_L_PER_KM = 0.25


def _haversine(origin: Coord, destination: Coord) -> float:
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


def _pairwise_matrix(points: Sequence[Coord]) -> List[List[float]]:
    """Build a symmetric distance matrix using haversine distances."""

    matrix: List[List[float]] = []
    for origin in points:
        row = []
        for dest in points:
            row.append(round(_haversine(origin, dest), 3))
        matrix.append(row)
    return matrix


def _estimate_duration(distance_km: float, speed_kmh: float | None) -> float:
    """Convert distance into minutes given an average speed."""

    speed = speed_kmh or DEFAULT_SPEED_KMH
    if speed <= 0:
        speed = DEFAULT_SPEED_KMH
    hours = distance_km / speed
    return hours * 60.0


def _estimate_fuel(distance_km: float, fuel_per_km: float | None) -> float:
    fuel = fuel_per_km if fuel_per_km is not None else DEFAULT_FUEL_L_PER_KM
    return max(distance_km * fuel, 0.0)


def _build_route(
    school: School,
    stops: Sequence[Stop],
    capacity: int,
    speed_kmh: float | None,
    fuel_per_km: float | None,
) -> RoutePlan:
    """Construct a RoutePlan for a cluster of stops."""

    ordered = [Stop(None, school.name, school.lat, school.lng)] + list(stops)
    coords: List[Coord] = [(stop.lat, stop.lng) for stop in ordered]
    matrix = _pairwise_matrix(coords)

    order = nearest_neighbor_tsp(matrix, start=0)
    # Ensure school is both start and end
    if order and order[0] != 0:
        order.insert(0, 0)
    if order and order[-1] != 0:
        order.append(0)

    distance = 0.0
    path: List[Stop] = []
    for idx in range(len(order) - 1):
        current = order[idx]
        nxt = order[idx + 1]
        distance += matrix[current][nxt]
        path.append(ordered[current])
    # append final stop
    if order:
        path.append(ordered[order[-1]])

    duration = _estimate_duration(distance, speed_kmh)
    fuel = _estimate_fuel(distance, fuel_per_km)

    return RoutePlan(
        bus_id="",
        stops=path,
        distance_km=round(distance, 3),
        duration_min=round(duration, 2),
        fuel_liters=round(fuel, 3),
        used_seats=len(stops),
        capacity=capacity,
    )


def optimize_routes(
    school: Dict[str, float | str] | School,
    students: Iterable[Dict[str, float | str] | Stop],
    bus_count: int,
    capacity: int,
    objective: Literal["distance", "duration", "fuel"] = "distance",
    weight: float | None = None,
    max_speed: float | None = None,
    fuel_consumption: float | None = None,
) -> Dict[str, object]:
    """Optimize student pickup routes.

    Parameters
    ----------
    school: dict or School with lat/lng
    students: iterable of dict or Stop containing lat/lng
    bus_count: number of buses available
    capacity: seats per bus
    objective: which metric to prioritize in the summary
    weight: optional multiplier applied to the objective
    max_speed: optional average speed in km/h
    fuel_consumption: liters per km
    """

    school_obj = (
        school
        if isinstance(school, School)
        else School(
            name=str(school.get("name", "School")),
            lat=float(school.get("lat")),
            lng=float(school.get("lng")),
        )
    )

    stop_objs: List[Stop] = []
    for s in students:
        if isinstance(s, Stop):
            stop_objs.append(s)
            continue
        stop_objs.append(
            Stop(
                id=s.get("id"),
                name=str(s.get("name", "Stop")),
                lat=float(s.get("lat")),
                lng=float(s.get("lng")),
                address=s.get("address"),
            )
        )

    clusters = cluster_students((school_obj.lat, school_obj.lng), stop_objs, bus_count, capacity)

    routes: List[RoutePlan] = []
    total_distance = total_duration = total_fuel = 0.0

    for idx, cluster in enumerate(clusters):
        plan = _build_route(school_obj, cluster, capacity, max_speed, fuel_consumption)
        plan.bus_id = f"bus-{idx + 1}"
        total_distance += plan.distance_km
        total_duration += plan.duration_min
        total_fuel += plan.fuel_liters
        routes.append(plan)

    objective_value = {
        "distance": total_distance,
        "duration": total_duration,
        "fuel": total_fuel,
    }.get(objective, total_distance)

    if weight is not None:
        objective_value *= weight

    summary: Dict[str, float | str] = {
        "objective": objective,
        "objectiveValue": round(objective_value, 3),
        "totalDistanceKm": round(total_distance, 3),
        "totalDurationMin": round(total_duration, 2),
        "totalFuelLiters": round(total_fuel, 3),
        "busCount": len(routes),
        "capacity": capacity,
    }

    return {
        "summary": summary,
        "routes": [
            {
                "busId": r.bus_id,
                "stops": [
                    {
                        "id": stop.id,
                        "name": stop.name,
                        "lat": stop.lat,
                        "lng": stop.lng,
                        "address": stop.address,
                    }
                    for stop in r.stops
                ],
                "distanceKm": r.distance_km,
                "durationMin": r.duration_min,
                "fuelLiters": r.fuel_liters,
                "usedSeats": r.used_seats,
                "capacity": r.capacity,
            }
            for r in routes
        ],
    }
