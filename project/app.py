"""Flask application entrypoint for the Smart School Bus Routing System."""
from __future__ import annotations

from flask import Flask

from config import get_settings
from core.db import Base, engine
from routes import register_blueprints

# Import models to register them with SQLAlchemy's metadata before table creation
from models import bus, daily_log, driver, route, student  # noqa: F401


settings = get_settings()

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config.update(
    SECRET_KEY=settings.secret_key,
    SQLALCHEMY_DATABASE_URI=settings.sqlalchemy_database_uri,
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

# Ensure database tables exist
Base.metadata.create_all(bind=engine)

# Register all blueprints
register_blueprints(app)


@app.cli.command("create-db")
def create_db_command():
    """CLI helper to create all database tables."""

    Base.metadata.create_all(bind=engine)
    print("Database tables created.")


if __name__ == "__main__":
    app.run(debug=settings.debug)
