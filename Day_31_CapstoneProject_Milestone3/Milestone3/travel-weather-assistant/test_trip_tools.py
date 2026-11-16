
import json

from app.tools.trip_tools import get_trip_details


# Existing trip ID created during your earlier CRUD test
TEST_TRIP_ID = "beb29003-d5fc-409d-ac69-dda4dfd3698f"


def test_existing_trip():
    print("\n===== EXISTING TRIP TEST =====")

    result = get_trip_details.invoke({
        "trip_id": TEST_TRIP_ID
    })

    print(json.dumps(json.loads(result), indent=2))


def test_invalid_trip():
    print("\n===== INVALID TRIP TEST =====")

    result = get_trip_details.invoke({
        "trip_id": "invalid-trip-id"
    })

    print(json.dumps(json.loads(result), indent=2))


if __name__ == "__main__":
    test_existing_trip()
    test_invalid_trip()
