"""HTML page routes."""
from __future__ import annotations

from flask import Blueprint, render_template

pages_bp = Blueprint("pages", __name__)


@pages_bp.get("/")
def index():
    return render_template("index.html")


@pages_bp.get("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@pages_bp.get("/students")
def students():
    return render_template("students.html")


@pages_bp.get("/drivers")
def drivers():
    return render_template("drivers.html")


@pages_bp.get("/calculator")
def calculator():
    return render_template("calculator.html")
