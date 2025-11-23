"""Driver CRUD API blueprint."""
from __future__ import annotations

from flask import Blueprint, abort, jsonify, request

from core.guards import require_json
from core.session import db_session
from models import Driver


driver_api_bp = Blueprint("drivers_api", __name__, url_prefix="/api/drivers")

ALLOWED_FIELDS = {"full_name", "email", "phone_number", "license_number"}


def _get_driver_or_404(session, driver_id: int) -> Driver:
    driver = session.get(Driver, driver_id)
    if not driver:
        abort(404, description="Driver not found")
    return driver


@driver_api_bp.get("")
def list_drivers():
    with db_session() as session:
        drivers = session.query(Driver).all()
        return jsonify([driver.to_dict() for driver in drivers])


@driver_api_bp.post("")
@require_json
def create_driver():
    data = request.get_json() or {}
    if not data.get("full_name"):
        abort(400, description="full_name is required")

    payload = {key: data.get(key) for key in ALLOWED_FIELDS}
    with db_session() as session:
        driver = Driver(**payload)
        session.add(driver)
        session.flush()
        return jsonify(driver.to_dict()), 201


@driver_api_bp.get("/<int:driver_id>")
def get_driver(driver_id: int):
    with db_session() as session:
        driver = _get_driver_or_404(session, driver_id)
        return jsonify(driver.to_dict())


@driver_api_bp.put("/<int:driver_id>")
@require_json
def update_driver(driver_id: int):
    data = request.get_json() or {}
    with db_session() as session:
        driver = _get_driver_or_404(session, driver_id)
        for key in ALLOWED_FIELDS:
            if key in data:
                setattr(driver, key, data.get(key))
        session.add(driver)
        session.flush()
        return jsonify(driver.to_dict())


@driver_api_bp.delete("/<int:driver_id>")
def delete_driver(driver_id: int):
    with db_session() as session:
        driver = _get_driver_or_404(session, driver_id)
        session.delete(driver)
        session.flush()
        return jsonify({"status": "deleted", "id": driver_id})
