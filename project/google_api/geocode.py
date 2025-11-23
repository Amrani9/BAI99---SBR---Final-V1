"""Geocoding helpers for addresses."""
from __future__ import annotations

import json
import random
import urllib.parse
import urllib.request
from typing import Dict, Optional, Tuple

from config import get_settings


def _mock_coordinates(address: str) -> Tuple[float, float]:
    """Generate deterministic mock coordinates for offline mode."""

    seed = hash(address) % (2**32)
    rng = random.Random(seed)
    # Latitude between -90 and 90, longitude between -180 and 180
    lat = rng.uniform(-85, 85)
    lng = rng.uniform(-170, 170)
    return round(lat, 6), round(lng, 6)


def geocode_address(address: str, api_key: Optional[str] = None, timeout: float = 5.0) -> Optional[Dict[str, object]]:
    """Geocode an address using the Google Maps Geocoding API.

    If no ``api_key`` is provided and none is configured, the function falls back to
    deterministic mock coordinates suitable for development and tests.
    """

    address = address.strip()
    if not address:
        return None

    settings = get_settings()
    key = api_key or settings.google_api_key

    if not key:
        lat, lng = _mock_coordinates(address)
        return {"lat": lat, "lng": lng, "source": "mock"}

    query = urllib.parse.urlencode({"address": address, "key": key})
    url = f"https://maps.googleapis.com/maps/api/geocode/json?{query}"
    req = urllib.request.Request(url)

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:  # nosec: B310
            payload = json.load(resp)
    except Exception:
        # In case of network failure, provide a mock response to keep flows unblocked
        lat, lng = _mock_coordinates(address)
        return {"lat": lat, "lng": lng, "source": "mock-fallback"}

    status = payload.get("status")
    results = payload.get("results", [])
    if status == "OK" and results:
        location = results[0]["geometry"]["location"]
        return {
            "lat": location.get("lat"),
            "lng": location.get("lng"),
            "formatted_address": results[0].get("formatted_address"),
            "source": "google",
        }

    return None
