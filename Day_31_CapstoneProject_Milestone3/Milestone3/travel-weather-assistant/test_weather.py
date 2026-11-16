
from datetime import date, timedelta

from app.services.weather_service import (
    geocode_location,
    get_weather_forecast
)


def test_geocoding():

    print("\n===== GEOCODING TEST =====")

    result = geocode_location("Jaipur")

    print(result)

    return result


def test_weather():

    print("\n===== WEATHER FORECAST TEST =====")

    # Choose dates within the forecast horizon
    start_date = date.today() + timedelta(days=2)
    end_date = start_date + timedelta(days=2)

    result = get_weather_forecast(
        destination="Jaipur",
        start_date=start_date,
        end_date=end_date
    )

    if not result["success"]:
        print("Weather unavailable:", result["error"])
        return

    print("Destination:", result["destination"])
    print("Country:", result["country"])

    for forecast in result["forecast"]:

        print("\nDate:", forecast["date"])
        print(
            "Maximum temperature:",
            forecast["temperature_max"], "°C"
        )
        print(
            "Minimum temperature:",
            forecast["temperature_min"], "°C"
        )
        print(
            "Rain probability:",
            forecast["precipitation_probability"], "%"
        )
        print(
            "Precipitation:",
            forecast["precipitation_sum"], "mm"
        )
        print(
            "Weather:",
            forecast["weather_description"]
        )


if __name__ == "__main__":

    test_geocoding()
    test_weather()
