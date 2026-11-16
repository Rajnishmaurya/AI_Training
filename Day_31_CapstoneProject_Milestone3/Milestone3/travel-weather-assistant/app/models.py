
import uuid

from datetime import date, datetime

from sqlalchemy import (
    Column,
    String,
    Date,
    DateTime,
)

from app.database import Base


class Trip(Base):

    __tablename__ = "trips"

    # Unique trip identifier
    trip_id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    # Employee information
    employee_id = Column(
        String(50),
        nullable=False,
        index=True
    )

    # Travel information
    destination = Column(
        String(150),
        nullable=False
    )

    start_date = Column(
        Date,
        nullable=False
    )

    end_date = Column(
        Date,
        nullable=False
    )

    purpose = Column(
        String(255),
        nullable=False
    )

    # Trip status
    status = Column(
        String(30),
        nullable=False,
        default="planned"
    )

    # Record creation timestamp
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    def __repr__(self):
        return (
            f"Trip(trip_id={self.trip_id}, "
            f"destination={self.destination})"
        )
