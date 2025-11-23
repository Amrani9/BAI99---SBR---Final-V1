"""Blueprint registration for the application."""
from __future__ import annotations

from flask import Flask

from .bus_api_bp import bus_api_bp
from .driver_api_bp import driver_api_bp
from .health_bp import health_bp
from .optimize_api_bp import optimize_api_bp
from .pages_bp import pages_bp
from .resolver_api_bp import resolver_api_bp
from .student_api_bp import student_api_bp


__all__ = [
    "bus_api_bp",
    "driver_api_bp",
    "health_bp",
    "optimize_api_bp",
    "pages_bp",
    "resolver_api_bp",
    "student_api_bp",
    "register_blueprints",
]


def register_blueprints(app: Flask) -> None:
    """Attach all blueprints to the Flask application."""

    app.register_blueprint(pages_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(student_api_bp)
    app.register_blueprint(driver_api_bp)
    app.register_blueprint(bus_api_bp)
    app.register_blueprint(resolver_api_bp)
    app.register_blueprint(optimize_api_bp)
