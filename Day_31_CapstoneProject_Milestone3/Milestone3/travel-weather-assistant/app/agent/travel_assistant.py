from app.services.memory_service import (
    save_message,
    get_conversation_history,
    save_session_context,
    get_session_context
)
import json

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from app.agent.llm import get_llm
from app.tools.trip_tools import get_trip_details
from app.tools.weather_tools import get_destination_weather


# --------------------------------------------------
# STAGE 1: RETRIEVE TRIP AND WEATHER INFORMATION
# --------------------------------------------------

def retrieve_trip_and_weather(trip_id: str) -> dict:
    """
    Stage 1:
    1. Retrieve trip details from SQLite.
    2. Retrieve weather for the saved destination and dates.
    """

    # Retrieve trip using LangChain tool
    trip_result = get_trip_details.invoke({
        "trip_id": trip_id
    })

    trip_data = json.loads(trip_result)

    # Stop if trip does not exist
    if not trip_data.get("success"):
        return {
            "success": False,
            "error": trip_data.get(
                "error",
                "Unable to retrieve trip."
            )
        }

    trip = trip_data["trip"]

    # Retrieve weather using saved trip details
    weather_result = get_destination_weather.invoke({
        "destination": trip["destination"],
        "start_date": trip["start_date"],
        "end_date": trip["end_date"]
    })

    weather_data = json.loads(weather_result)

    return {
        "success": True,
        "trip": trip,
        "weather": weather_data
    }


# --------------------------------------------------
# STAGE 2: GENERATE TRAVEL ADVISORY
# --------------------------------------------------

def generate_travel_advisory(
    trip: dict,
    weather: dict,
    question: str,
    conversation_history: list = None
) -> str:
    """
    Generate a travel advisory using trip details,
    weather data, and previous conversation messages.
    """

    conversation_history = conversation_history or []

    # Format previous conversation for the LLM
    history_text = "\n".join(
        [
            f"{message['role'].upper()}: {message['content']}"
            for message in conversation_history
        ]
    )

    if not history_text:
        history_text = "No previous conversation."

    # Do not ask the LLM to invent weather information
    if not weather.get("success"):

        error_message = weather.get(
            "error",
            "Weather forecast is currently unavailable."
        )

        return f"""
Your trip to {trip['destination']} is scheduled from
{trip['start_date']} to {trip['end_date']}.

Regarding your question: {question}

A specific weather forecast is not available for these dates.
Reason: {error_message}

Therefore, I cannot reliably determine whether rain is expected
or whether you will need an umbrella.

General business travel suggestions:
1. Pack appropriate business attire for your meetings.
2. Carry your laptop, charger, and work essentials.
3. Keep identification and travel documents accessible.
4. Consider carrying a compact umbrella as a precaution.

These are general suggestions, not weather-based recommendations.
Please check the forecast closer to your departure date.
"""

    # Generate advisory when actual weather is available
    llm = get_llm()

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
You are an AI-powered business travel and weather advisory assistant.

Use the conversation history to understand follow-up questions.

STRICT RULES:

1. Use only the supplied trip and weather information
   for factual claims about this trip.

2. Use conversation history to understand references such
   as "there", "that place", and "the trip".

3. Never invent temperatures, rainfall, weather conditions,
   destinations, dates, or forecast details.

4. Do not use general knowledge to add weather information.

5. Answer the employee's latest question directly.

6. Include the destination, travel dates, and weather summary
   when relevant.

7. Provide 3-4 practical packing or travel suggestions
   when the employee asks for a travel advisory.

8. If a weather field is missing, clearly say it is unavailable.

9. Keep the response concise and useful.
"""
        ),
        (
            "human",
            """
PREVIOUS CONVERSATION:
{conversation_history}

TRIP INFORMATION:
{trip_information}

WEATHER INFORMATION:
{weather_information}

LATEST EMPLOYEE QUESTION:
{question}

Answer the latest question using the supplied information.
"""
        )
    ])

    chain = prompt | llm | StrOutputParser()

    response = chain.invoke({
        "conversation_history": history_text,
        "trip_information": json.dumps(trip, indent=2),
        "weather_information": json.dumps(weather, indent=2),
        "question": question
    })

    return response.strip()


# --------------------------------------------------
# MAIN TRAVEL ASSISTANT
# --------------------------------------------------

def ask_travel_assistant(
    session_id: str,
    question: str,
    trip_id: str = None
) -> dict:
    """
    Execute the travel assistant with Redis-backed memory.

    First message:
        Provide session_id, question and trip_id.

    Follow-up message:
        Provide the same session_id and question.
        The trip_id is recovered from Redis.
    """

    if not session_id or not session_id.strip():
        return {
            "success": False,
            "error": "Session ID cannot be empty."
        }

    if not question or not question.strip():
        return {
            "success": False,
            "error": "Question cannot be empty."
        }

    try:
        # 1. Retrieve previous conversation
        history = get_conversation_history(session_id)

        # 2. Save trip ID for a new trip request
        if trip_id:
            save_session_context(session_id, trip_id)

        # 3. Recover trip ID for follow-up questions
        else:
            trip_id = get_session_context(session_id)

        if not trip_id:
            return {
                "success": False,
                "error": (
                    "No trip is associated with this session. "
                    "Please provide a trip ID first."
                )
            }

        # 4. Retrieve actual trip and weather information
        context = retrieve_trip_and_weather(trip_id)

        if not context["success"]:
            return {
                "success": False,
                "error": context["error"]
            }

        # 5. Generate advisory
        answer = generate_travel_advisory(
            trip=context["trip"],
            weather=context["weather"],
            question=question,
            conversation_history=history
        )

        # 6. Save this conversation turn in Redis
        save_message(
            session_id,
            "user",
            question
        )

        save_message(
            session_id,
            "assistant",
            answer
        )

        return {
            "success": True,
            "session_id": session_id,
            "trip_id": trip_id,
            "destination": context["trip"]["destination"],
            "weather_available": context["weather"].get(
                "success", False
            ),
            "answer": answer
        }

    except Exception as exc:
        return {
            "success": False,
            "error": f"Travel assistant failed: {str(exc)}"
        }

