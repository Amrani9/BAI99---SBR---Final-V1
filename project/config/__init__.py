"""Configuration package for Smart School Bus Routing System."""

from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from a local .env file if present
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"
load_dotenv(ENV_PATH)

from .settings import Settings, get_settings  # noqa: E402,F401

__all__ = ["Settings", "get_settings", "BASE_DIR", "ENV_PATH"]
