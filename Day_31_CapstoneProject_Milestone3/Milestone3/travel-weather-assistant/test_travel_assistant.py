
import json

from app.agent.travel_assistant import ask_travel_assistant


TEST_TRIP_ID = "beb29003-d5fc-409d-ac69-dda4dfd3698f"


def test_travel_assistant():

    print("\n===== TRAVEL ASSISTANT TEST =====")

    result = ask_travel_assistant(
        trip_id=TEST_TRIP_ID,
        question=(
            "What weather should I expect for my trip? "
            "What should I pack?"
        )
    )

    print(json.dumps(result, indent=2))


def test_invalid_trip():

    print("\n===== INVALID TRIP TEST =====")

    result = ask_travel_assistant(
        trip_id="invalid-trip-id",
        question="What is my destination?"
    )

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    test_travel_assistant()
    test_invalid_trip()
