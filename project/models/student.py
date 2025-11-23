"""Student model definition."""
from __future__ import annotations

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from core.db import Base
from core.utils import utcnow


class Student(Base):
    """Represents a student assigned to a bus route."""

    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=True)
    phone_number = Column(String(30), nullable=True)
    address = Column(String(255), nullable=True)
    route_id = Column(Integer, ForeignKey("routes.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    route = relationship("Route", back_populates="students")

    def to_dict(self) -> dict:
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"<Student id={self.id} name={self.full_name}>"
