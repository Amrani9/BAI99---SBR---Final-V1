"""Route model definition."""
from __future__ import annotations

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Time
from sqlalchemy.orm import relationship

from core.db import Base
from core.utils import utcnow


class Route(Base):
    """Represents a bus route."""

    __tablename__ = "routes"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    start_time = Column(Time, nullable=True)
    end_time = Column(Time, nullable=True)
    distance_km = Column(Float, nullable=True)
    duration_min = Column(Integer, nullable=True)
    bus_id = Column(Integer, ForeignKey("buses.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    bus = relationship("Bus", back_populates="routes")
    students = relationship("Student", back_populates="route", cascade="all, delete-orphan")
    daily_logs = relationship("DailyLog", back_populates="route", cascade="all, delete-orphan")

    def to_dict(self) -> dict:
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"<Route id={self.id} name={self.name}>"
