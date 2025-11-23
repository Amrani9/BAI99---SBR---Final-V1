"""Route optimization API blueprint."""
from __future__ import annotations

from flask import Blueprint, abort, jsonify, request

from core.guards import require_json
from routing_engine.optimizer import optimize_routes

optimize_api_bp = Blueprint("optimize_api", __name__, url_prefix="/api/optimize")


@optimize_api_bp.post("")
@require_json
def optimize():
    data = request.get_json() or {}
    school = data.get("school") or {}
    students = data.get("students") or []

    try:
        bus_count = int(data.get("busCount") or data.get("bus_count") or 1)
        capacity = int(data.get("capacity") or data.get("busCapacity") or 40)
    except (TypeError, ValueError):
        abort(400, description="busCount and capacity must be numbers")

    objective = data.get("objective", "distance")
    weight = data.get("weight")
    max_speed = data.get("maxSpeed") or data.get("max_speed")
    fuel_consumption = data.get("fuelConsumption") or data.get("fuel_consumption")

    weight_val = float(weight) if weight not in (None, "") else None
    speed_val = float(max_speed) if max_speed not in (None, "") else None
    fuel_val = float(fuel_consumption) if fuel_consumption not in (None, "") else None

    result = optimize_routes(
        school=school,
        students=students,
        bus_count=bus_count,
        capacity=capacity,
        objective=objective,
        weight=weight_val,
        max_speed=speed_val,
        fuel_consumption=fuel_val,
    )

    return jsonify(result)
