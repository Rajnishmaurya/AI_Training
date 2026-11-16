
import json

from app.tools.weather_tools import get_destination_weather


def test_valid_weather():
    print("\n===== VALID WEATHER TOOL TEST =====")

    result = get_destination_weather.invoke({
        "destination": "Jaipur",
        "start_date": "2026-11-18",
        "end_date": "2026-11-20"
    })

    parsed_result = json.loads(result)

    print(json.dumps(parsed_result, indent=2))


def test_invalid_date():
    print("\n===== INVALID DATE TEST =====")

    result = get_destination_weather.invoke({
        "destination": "Jaipur",
        "start_date": "invalid-date",
        "end_date": "2026-11-20"
    })

    print(json.dumps(json.loads(result), indent=2))


def test_invalid_destination():
    print("\n===== INVALID DESTINATION TEST =====")

    result = get_destination_weather.invoke({
        "destination": "InvalidCityXYZ123",
        "start_date": "2026-11-18",
        "end_date": "2026-11-20"
    })

    print(json.dumps(json.loads(result), indent=2))


if __name__ == "__main__":
    test_valid_weather()
    test_invalid_date()
    test_invalid_destination()
