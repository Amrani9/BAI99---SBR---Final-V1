import os
import sys
import importlib
from pathlib import Path
from typing import Any, Dict

import pytest

# Ensure the application uses an isolated test database before importing the app
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

os.environ.setdefault("DATABASE_URL", "sqlite:///./test_api.db")

from app import app  # noqa: E402
from core.db import Base, engine  # noqa: E402

optimize_module = importlib.import_module("routes.optimize_api_bp")  # noqa: E402


@pytest.fixture(autouse=True)
def clean_database():
    """Reset database schema for each test."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client():
    with app.test_client() as client:
        yield client


def test_health_endpoint(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}


def test_optimize_endpoint(monkeypatch, client):
    payload: Dict[str, Any] = {
        "school": {"lat": 0, "lng": 0, "name": "School"},
        "students": [
            {"full_name": "Alice", "lat": 1.0, "lng": 1.0},
            {"full_name": "Bob", "lat": 2.0, "lng": 2.0},
        ],
        "busCount": 1,
        "capacity": 40,
        "objective": "distance",
    }

    fake_response = {
        "summary": {"totalDistanceKm": 10, "objective": "distance"},
        "routes": [
            {
                "busId": 1,
                "stops": [payload["school"], *payload["students"]],
                "distanceKm": 10,
                "durationMin": 20,
                "fuelLiters": 5,
                "usedSeats": 2,
                "capacity": 40,
            }
        ],
    }

    def fake_optimize(**kwargs):
        return fake_response

    monkeypatch.setattr(optimize_module, "optimize_routes", fake_optimize)

    resp = client.post("/api/optimize", json=payload)
    assert resp.status_code == 200
    assert resp.get_json() == fake_response


def test_student_crud_endpoints(client):
    # Create
    new_student = {"full_name": "Charlie", "email": "charlie@example.com"}
    create_resp = client.post("/api/students", json=new_student)
    assert create_resp.status_code == 201
    created = create_resp.get_json()
    assert created["full_name"] == "Charlie"

    # List
    list_resp = client.get("/api/students")
    assert list_resp.status_code == 200
    students = list_resp.get_json()
    assert any(s["full_name"] == "Charlie" for s in students)

    # Retrieve
    student_id = created["id"]
    get_resp = client.get(f"/api/students/{student_id}")
    assert get_resp.status_code == 200
    assert get_resp.get_json()["full_name"] == "Charlie"
