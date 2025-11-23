"""Student CRUD API blueprint."""
from __future__ import annotations

from flask import Blueprint, abort, jsonify, request

from core.session import db_session
from core.guards import require_json
from models import Student

student_api_bp = Blueprint("students_api", __name__, url_prefix="/api/students")

ALLOWED_FIELDS = {"full_name", "email", "phone_number", "address", "route_id"}


def _get_student_or_404(session, student_id: int) -> Student:
    student = session.get(Student, student_id)
    if not student:
        abort(404, description="Student not found")
    return student


@student_api_bp.get("")
def list_students():
    with db_session() as session:
        students = session.query(Student).all()
        return jsonify([student.to_dict() for student in students])


@student_api_bp.post("")
@require_json
def create_student():
    data = request.get_json() or {}
    if not data.get("full_name"):
        abort(400, description="full_name is required")

    payload = {key: data.get(key) for key in ALLOWED_FIELDS}
    with db_session() as session:
        student = Student(**payload)
        session.add(student)
        session.flush()
        return jsonify(student.to_dict()), 201


@student_api_bp.get("/<int:student_id>")
def get_student(student_id: int):
    with db_session() as session:
        student = _get_student_or_404(session, student_id)
        return jsonify(student.to_dict())


@student_api_bp.put("/<int:student_id>")
@require_json
def update_student(student_id: int):
    data = request.get_json() or {}
    with db_session() as session:
        student = _get_student_or_404(session, student_id)
        for key in ALLOWED_FIELDS:
            if key in data:
                setattr(student, key, data.get(key))
        session.add(student)
        session.flush()
        return jsonify(student.to_dict())


@student_api_bp.delete("/<int:student_id>")
def delete_student(student_id: int):
    with db_session() as session:
        student = _get_student_or_404(session, student_id)
        session.delete(student)
        session.flush()
        return jsonify({"status": "deleted", "id": student_id})
