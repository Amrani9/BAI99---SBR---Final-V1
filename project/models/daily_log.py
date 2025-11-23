"""Daily log model definition."""
from __future__ import annotations

from datetime import date

from sqlalchemy import Column, Date, Float, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from core.db import Base


class DailyLog(Base):
    """Operational metrics captured per day for a driver and bus."""

    __tablename__ = "daily_logs"

    id = Column(Integer, primary_key=True)
    log_date = Column(Date, default=date.today, nullable=False)
    distance_km = Column(Float, nullable=True)
    duration_min = Column(Integer, nullable=True)
    fuel_liters = Column(Float, nullable=True)
    notes = Column(Text, nullable=True)
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=False)
    bus_id = Column(Integer, ForeignKey("buses.id"), nullable=True)
    route_id = Column(Integer, ForeignKey("routes.id"), nullable=True)

    driver = relationship("Driver", back_populates="daily_logs")
    bus = relationship("Bus", back_populates="daily_logs")
    route = relationship("Route", back_populates="daily_logs")

    def to_dict(self) -> dict:
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"<DailyLog id={self.id} date={self.log_date}>"
