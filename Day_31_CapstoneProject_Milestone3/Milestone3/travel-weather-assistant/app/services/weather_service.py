
from datetime import date, timedelta
import time

import httpx


# --------------------------------------------------
# API CONFIGURATION
# --------------------------------------------------

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

REQUEST_TIMEOUT = httpx.Timeout(
    30.0,
    connect=15.0
)

MAX_RETRIES = 3


# --------------------------------------------------
# WEATHER CODE MAPPING
# --------------------------------------------------

WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snowfall",
    73: "Moderate snowfall",
    75: "Heavy snowfall",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}


# --------------------------------------------------
# REUSABLE API REQUEST FUNCTION WITH RETRIES
# --------------------------------------------------

def make_api_request(url: str, params: dict) -> dict:
    """
    Send an HTTP GET request with retry handling.

    Retries:
    - Network errors
    - Connection timeouts
    - HTTP 429
    - HTTP 5xx server errors
    """

    retryable_status_codes = (429, 500, 502, 503, 504)

    for attempt in range(MAX_RETRIES):

        try:
            response = httpx.get(
                url,
                params=params,
                timeout=REQUEST_TIMEOUT
            )

            response.raise_for_status()

            return response.json()

        except httpx.HTTPStatusError as exc:

            status_code = exc.response.status_code

            if status_code not in retryable_status_codes:
                raise

            if attempt == MAX_RETRIES - 1:
                raise

        except httpx.RequestError:

            if attempt == MAX_RETRIES - 1:
                raise

        wait_time = 2 ** attempt

        print(
            f"API request failed. "
            f"Retrying in {wait_time} seconds "
            f"(attempt {attempt + 1}/{MAX_RETRIES})..."
        )

        time.sleep(wait_time)

    raise RuntimeError("API request failed after retries.")


# --------------------------------------------------
# GEOCODING SERVICE
# --------------------------------------------------

def geocode_location(destination: str) -> dict:
    """
    Convert a destination name into geographic coordinates.

    Example:
        geocode_location("Jaipur")

    Returns:
        success, name, country, latitude, longitude, timezone
    """

    if not destination or not destination.strip():
        return {
            "success": False,
            "error": "Destination cannot be empty."
        }

    params = {
        "name": destination.strip(),
        "count": 1,
        "language": "en",
        "format": "json"
    }

    try:

        data = make_api_request(
            GEOCODING_URL,
            params
        )

        results = data.get("results", [])

        if not results:

            return {
                "success": False,
                "error": f"Location '{destination}' was not found."
            }

        location = results[0]

        return {
            "success": True,
            "name": location.get("name"),
            "country": location.get("country"),
            "latitude": location.get("latitude"),
            "longitude": location.get("longitude"),
            "timezone": location.get("timezone", "auto")
        }

    except httpx.HTTPError as exc:

        return {
            "success": False,
            "error": f"Geocoding API request failed: {exc}"
        }

    except (ValueError, TypeError) as exc:

        return {
            "success": False,
            "error": f"Invalid geocoding API response: {exc}"
        }


# --------------------------------------------------
# DATE VALIDATION
# --------------------------------------------------

def validate_forecast_dates(
    start_date: date,
    end_date: date
) -> dict:
    """
    Validate requested travel dates.

    Open-Meteo forecast endpoint supports forecasts
    up to 16 days ahead, depending on availability.
    This application uses a conservative 15-day limit.
    """

    today = date.today()

    last_forecast_date = today + timedelta(days=15)

    if start_date < today:

        return {
            "valid": False,
            "error": "Past travel dates are not supported."
        }

    if end_date < start_date:

        return {
            "valid": False,
            "error": "End date cannot be before start date."
        }

    if end_date > last_forecast_date:

        return {
            "valid": False,
            "error": (
                f"Forecast is available only up to "
                f"{last_forecast_date.isoformat()}. "
                f"Please choose dates within the forecast range."
            )
        }

    return {
        "valid": True
    }


# --------------------------------------------------
# WEATHER FORECAST SERVICE
# --------------------------------------------------

def get_weather_forecast(
    destination: str,
    start_date: date,
    end_date: date
) -> dict:
    """
    Retrieve weather forecasts for a destination
    and date range using Open-Meteo.

    Returns daily:
    - Maximum temperature
    - Minimum temperature
    - Precipitation probability
    - Precipitation amount
    - Weather description
    """

    # 1. Validate input dates

    date_validation = validate_forecast_dates(
        start_date,
        end_date
    )

    if not date_validation["valid"]:

        return {
            "success": False,
            "error": date_validation["error"]
        }

    # 2. Get destination coordinates

    location = geocode_location(destination)

    if not location["success"]:

        return {
            "success": False,
            "error": location["error"]
        }

    # 3. Prepare forecast API parameters

    params = {
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "daily": (
            "temperature_2m_max,"
            "temperature_2m_min,"
            "precipitation_probability_max,"
            "precipitation_sum,"
            "weather_code"
        ),
        "timezone": location["timezone"],
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat()
    }

    # 4. Call Open-Meteo forecast API

    try:

        data = make_api_request(
            FORECAST_URL,
            params
        )

        daily_data = data.get("daily")

        if not daily_data:

            return {
                "success": False,
                "error": "Weather forecast data is unavailable."
            }

        dates = daily_data.get("time", [])

        max_temps = daily_data.get(
            "temperature_2m_max", []
        )

        min_temps = daily_data.get(
            "temperature_2m_min", []
        )

        precipitation_probabilities = daily_data.get(
            "precipitation_probability_max", []
        )

        precipitation_amounts = daily_data.get(
            "precipitation_sum", []
        )

        weather_codes = daily_data.get(
            "weather_code", []
        )

        # 5. Build daily forecast response

        forecast = []

        for index, forecast_date in enumerate(dates):

            weather_code = weather_codes[index]

            forecast.append({

                "date": forecast_date,

                "temperature_max": max_temps[index],

                "temperature_min": min_temps[index],

                "precipitation_probability": (
                    precipitation_probabilities[index]
                ),

                "precipitation_sum": (
                    precipitation_amounts[index]
                ),

                "weather_code": weather_code,

                "weather_description": WEATHER_CODES.get(
                    weather_code,
                    "Unknown weather condition"
                )
            })

        # 6. Return structured result

        return {
            "success": True,

            "destination": location["name"],

            "country": location["country"],

            "timezone": location["timezone"],

            "forecast": forecast
        }

    except httpx.HTTPError as exc:

        return {
            "success": False,
            "error": f"Weather API request failed: {exc}"
        }

    except (KeyError, IndexError, TypeError, ValueError) as exc:

        return {
            "success": False,
            "error": f"Unexpected weather API response: {exc}"
        }
