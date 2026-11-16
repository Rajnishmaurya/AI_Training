
import json
from datetime import date

from langchain_core.tools import tool

from app.services.weather_service import get_weather_forecast


@tool
def get_destination_weather(
    destination: str,
    start_date: str,
    end_date: str
) -> str:
    """
    Retrieve actual weather forecast information for a destination
    and travel date range using the Open-Meteo API.

    Use this tool when the user asks about weather at a destination.

    Args:
        destination: City or destination name, for example Jaipur.
        start_date: Travel start date in YYYY-MM-DD format.
        end_date: Travel end date in YYYY-MM-DD format.

    Returns:
        JSON string containing actual weather forecast data
        or an error explaining why the forecast is unavailable.
    """

    # 1. Validate destination
    if not destination or not destination.strip():
        return json.dumps({
            "success": False,
            "error": "Destination cannot be empty."
        })

    # 2. Parse and validate dates
    try:
        parsed_start_date = date.fromisoformat(start_date)
        parsed_end_date = date.fromisoformat(end_date)

    except (ValueError, TypeError):
        return json.dumps({
            "success": False,
            "error": "Invalid date format. Use YYYY-MM-DD."
        })

    # 3. Retrieve actual weather information
    try:
        result = get_weather_forecast(
            destination=destination.strip(),
            start_date=parsed_start_date,
            end_date=parsed_end_date
        )

        return json.dumps(result, indent=2)

    except Exception as exc:
        return json.dumps({
            "success": False,
            "error": f"Unable to retrieve weather information: {str(exc)}"
        })
