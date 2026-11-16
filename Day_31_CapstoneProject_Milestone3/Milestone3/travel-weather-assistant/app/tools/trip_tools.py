
import json

from langchain_core.tools import tool

from app.database import SessionLocal
from app.services.trip_service import get_trip_by_id


@tool
def get_trip_details(trip_id: str) -> str:
    """
    Retrieve saved travel details from the SQLite database.

    Use this tool when the user asks about an existing trip
    or provides a trip ID.

    Args:
        trip_id: Unique ID of the trip to retrieve.

    Returns:
        JSON string containing trip details or an error.
    """

    if not trip_id or not trip_id.strip():
        return json.dumps({
            "success": False,
            "error": "Trip ID cannot be empty."
        })

    db = SessionLocal()

    try:
        trip = get_trip_by_id(
            db=db,
            trip_id=trip_id.strip()
        )

        if trip is None:
            return json.dumps({
                "success": False,
                "error": f"No trip found with ID: {trip_id}"
            })

        trip_details = {
            "success": True,
            "trip": {
                "trip_id": trip.trip_id,
                "employee_id": trip.employee_id,
                "destination": trip.destination,
                "start_date": trip.start_date.isoformat(),
                "end_date": trip.end_date.isoformat(),
                "purpose": trip.purpose,
                "status": trip.status,
                "created_at": (
                    trip.created_at.isoformat()
                    if trip.created_at
                    else None
                )
            }
        }

        return json.dumps(trip_details, indent=2)

    except Exception as exc:
        return json.dumps({
            "success": False,
            "error": f"Unable to retrieve trip details: {str(exc)}"
        })

    finally:
        db.close()
