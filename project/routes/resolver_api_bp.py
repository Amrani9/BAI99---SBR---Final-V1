"""Address resolver API blueprint."""
from __future__ import annotations

from flask import Blueprint, jsonify, request

from core.guards import require_json
from google_api.geocode import geocode_address
from google_api.resolver import normalize_address, resolve_student_addresses

resolver_api_bp = Blueprint("resolver_api", __name__, url_prefix="/api/resolver")


@resolver_api_bp.post("/resolve")
@require_json
def resolve_addresses():
    data = request.get_json() or {}
    addresses = data.get("addresses")
    students = data.get("students")

    if students is not None:
        resolved = resolve_student_addresses(students)
        payload = [
            {
                "student": getattr(item["student"], "to_dict", lambda: item["student"])(),
                "location": item["location"],
            }
            for item in resolved
        ]
        return jsonify(payload)

    if addresses is None:
        address = data.get("address", "")
        normalized = normalize_address(address)
        return jsonify({"query": normalized, "location": geocode_address(normalized)})

    results = []
    for addr in addresses:
        normalized = normalize_address(addr)
        results.append({"query": normalized, "location": geocode_address(normalized)})
    return jsonify(results)
