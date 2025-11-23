"""Bus CRUD API blueprint."""
from __future__ import annotations

from flask import Blueprint, abort, jsonify, request

from core.guards import require_json
from core.session import db_session
from models import Bus

bus_api_bp = Blueprint("buses_api", __name__, url_prefix="/api/buses")

ALLOWED_FIELDS = {"label", "license_plate", "capacity", "driver_id"}


def _get_bus_or_404(session, bus_id: int) -> Bus:
    bus = session.get(Bus, bus_id)
    if not bus:
        abort(404, description="Bus not found")
    return bus


@bus_api_bp.get("")
def list_buses():
    with db_session() as session:
        buses = session.query(Bus).all()
        return jsonify([bus.to_dict() for bus in buses])


@bus_api_bp.post("")
@require_json
def create_bus():
    data = request.get_json() or {}
    if not data.get("label") or not data.get("license_plate"):
        abort(400, description="label and license_plate are required")

    payload = {key: data.get(key) for key in ALLOWED_FIELDS}
    with db_session() as session:
        bus = Bus(**payload)
        session.add(bus)
        session.flush()
        return jsonify(bus.to_dict()), 201


@bus_api_bp.get("/<int:bus_id>")
def get_bus(bus_id: int):
    with db_session() as session:
        bus = _get_bus_or_404(session, bus_id)
        return jsonify(bus.to_dict())


@bus_api_bp.put("/<int:bus_id>")
@require_json
def update_bus(bus_id: int):
    data = request.get_json() or {}
    with db_session() as session:
        bus = _get_bus_or_404(session, bus_id)
        for key in ALLOWED_FIELDS:
            if key in data:
                setattr(bus, key, data.get(key))
        session.add(bus)
        session.flush()
        return jsonify(bus.to_dict())


@bus_api_bp.delete("/<int:bus_id>")
def delete_bus(bus_id: int):
    with db_session() as session:
        bus = _get_bus_or_404(session, bus_id)
        session.delete(bus)
        session.flush()
        return jsonify({"status": "deleted", "id": bus_id})
