"""Bus model definition."""
from __future__ import annotations

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from core.db import Base
from core.utils import utcnow


class Bus(Base):
    """Represents a school bus."""

    __tablename__ = "buses"

    id = Column(Integer, primary_key=True)
    label = Column(String(50), nullable=False)
    license_plate = Column(String(20), unique=True, nullable=False)
    capacity = Column(Integer, default=40, nullable=False)
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    driver = relationship("Driver", back_populates="bus")
    routes = relationship("Route", back_populates="bus", cascade="all, delete-orphan")
    daily_logs = relationship("DailyLog", back_populates="bus", cascade="all, delete-orphan")

    def to_dict(self) -> dict:
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"<Bus id={self.id} label={self.label}>"
