"""Security helpers and route guards."""
from __future__ import annotations

from functools import wraps
from typing import Callable, Optional

from flask import request, abort

from config import get_settings

settings = get_settings()


def require_api_key(header_name: str = "X-API-KEY") -> Callable:
    """Simple decorator to enforce a static API key check on a route."""

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            configured_key: Optional[str] = settings.google_api_key
            incoming_key = request.headers.get(header_name)
            if configured_key and incoming_key != configured_key:
                abort(401, description="Unauthorized: invalid API key")
            return func(*args, **kwargs)

        return wrapper

    return decorator


def require_json(func: Callable) -> Callable:
    """Ensure the request has a JSON body."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not request.is_json:
            abort(400, description="Expected JSON payload")
        return func(*args, **kwargs)

    return wrapper
