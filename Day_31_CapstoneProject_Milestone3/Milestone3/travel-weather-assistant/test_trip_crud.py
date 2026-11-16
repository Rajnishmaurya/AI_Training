
from app.database import SessionLocal
from app.schemas import TripCreate
from app.services.trip_service import (
    create_trip,
    get_trip_by_id,
    get_employee_trips
)


def test_trip_operations():

    db = SessionLocal()

    try:
        # 1. Prepare employee trip information
        trip_data = TripCreate(
            employee_id="EMP104",
            destination="Jaipur",
            start_date="2026-12-10",
            end_date="2026-12-15",
            purpose="Client meeting"
        )

        # 2. Create and save trip
        saved_trip = create_trip(db, trip_data)

        print("\n===== TRIP CREATED =====")
        print("Trip ID:", saved_trip.trip_id)
        print("Employee:", saved_trip.employee_id)
        print("Destination:", saved_trip.destination)
        print("Start Date:", saved_trip.start_date)
        print("End Date:", saved_trip.end_date)
        print("Purpose:", saved_trip.purpose)
        print("Status:", saved_trip.status)

        # 3. Retrieve trip using ID
        retrieved_trip = get_trip_by_id(
            db,
            saved_trip.trip_id
        )

        print("\n===== TRIP RETRIEVED =====")
        print(retrieved_trip)

        # 4. Retrieve employee trips
        employee_trips = get_employee_trips(
            db,
            "EMP104"
        )

        print("\n===== EMPLOYEE TRIPS =====")
        print("Total trips:", len(employee_trips))

    finally:
        db.close()


if __name__ == "__main__":
    test_trip_operations()
