"""Driver model definition."""
from __future__ import annotations

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from core.db import Base
from core.utils import utcnow


class Driver(Base):
    """Represents a bus driver."""

    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=True)
    phone_number = Column(String(30), nullable=True)
    license_number = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    bus = relationship("Bus", back_populates="driver", uselist=False)
    daily_logs = relationship("DailyLog", back_populates="driver", cascade="all, delete-orphan")

    def to_dict(self) -> dict:
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"<Driver id={self.id} name={self.full_name}>"
