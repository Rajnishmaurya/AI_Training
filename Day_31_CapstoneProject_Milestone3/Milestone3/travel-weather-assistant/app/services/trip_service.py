
from sqlalchemy.orm import Session

from app.models import Trip
from app.schemas import TripCreate


def create_trip(db: Session, trip_data: TripCreate) -> Trip:
    """
    Save a new employee trip in SQLite.
    """

    new_trip = Trip(
        employee_id=trip_data.employee_id,
        destination=trip_data.destination,
        start_date=trip_data.start_date,
        end_date=trip_data.end_date,
        purpose=trip_data.purpose,
        status="planned"
    )

    try:
        db.add(new_trip)
        db.commit()
        db.refresh(new_trip)

        return new_trip

    except Exception:
        db.rollback()
        raise


def get_trip_by_id(db: Session, trip_id: str):
    """
    Retrieve an existing trip using its unique ID.
    """

    return (
        db.query(Trip)
        .filter(Trip.trip_id == trip_id)
        .first()
    )


def get_employee_trips(db: Session, employee_id: str):
    """
    Retrieve all trips belonging to an employee.
    """

    return (
        db.query(Trip)
        .filter(Trip.employee_id == employee_id)
        .all()
    )
