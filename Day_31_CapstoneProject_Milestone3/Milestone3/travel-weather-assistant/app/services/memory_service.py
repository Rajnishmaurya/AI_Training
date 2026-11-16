
import json
import os

import redis
from dotenv import load_dotenv


# Load environment variables from project root
load_dotenv()


# --------------------------------------------------
# REDIS CONFIGURATION
# --------------------------------------------------

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))
REDIS_TTL = int(os.getenv("REDIS_TTL", "86400"))

MAX_MESSAGES = 10

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    decode_responses=True
)


# --------------------------------------------------
# REDIS CONNECTION TEST
# --------------------------------------------------

def check_redis_connection() -> bool:
    """Check whether Redis is reachable."""

    return redis_client.ping()


# --------------------------------------------------
# SAVE CONVERSATION MESSAGE
# --------------------------------------------------

def save_message(
    session_id: str,
    role: str,
    content: str
) -> bool:
    """
    Save one conversation message in Redis.

    Each session has its own Redis list.

    Args:
        session_id: Unique conversation session ID.
        role: Either user or assistant.
        content: Message content.
    """

    if not session_id or not session_id.strip():
        raise ValueError("Session ID cannot be empty.")

    if role not in ("user", "assistant"):
        raise ValueError("Role must be user or assistant.")

    if not content or not content.strip():
        raise ValueError("Message content cannot be empty.")

    key = f"travel_assistant:session:{session_id}"

    message = {
        "role": role,
        "content": content.strip()
    }

    redis_client.rpush(
        key,
        json.dumps(message)
    )

    # Keep only the most recent messages
    redis_client.ltrim(
        key,
        -MAX_MESSAGES,
        -1
    )

    # Refresh expiration after each message
    redis_client.expire(
        key,
        REDIS_TTL
    )

    return True


# --------------------------------------------------
# RETRIEVE CONVERSATION HISTORY
# --------------------------------------------------

def get_conversation_history(
    session_id: str
) -> list:
    """
    Retrieve recent conversation messages for a session.

    Returns:
        List of dictionaries containing role and content.
    """

    if not session_id or not session_id.strip():
        raise ValueError("Session ID cannot be empty.")

    key = f"travel_assistant:session:{session_id}"

    messages = redis_client.lrange(
        key,
        0,
        -1
    )

    history = []

    for message in messages:
        history.append(json.loads(message))

    return history


# --------------------------------------------------
# CLEAR SESSION HISTORY
# --------------------------------------------------

def clear_session(session_id: str) -> bool:
    """
    Delete conversation history for a specific session.
    """

    if not session_id or not session_id.strip():
        raise ValueError("Session ID cannot be empty.")

    key = f"travel_assistant:session:{session_id}"

    redis_client.delete(key)

    return True



# --------------------------------------------------
# SAVE TRIP CONTEXT FOR A SESSION
# --------------------------------------------------

def save_session_context(
    session_id: str,
    trip_id: str
) -> bool:
    """
    Associate a trip ID with a conversation session.
    """

    if not session_id or not session_id.strip():
        raise ValueError("Session ID cannot be empty.")

    if not trip_id or not trip_id.strip():
        raise ValueError("Trip ID cannot be empty.")

    key = f"travel_assistant:context:{session_id}"

    redis_client.set(
        key,
        trip_id.strip(),
        ex=REDIS_TTL
    )

    return True


# --------------------------------------------------
# RETRIEVE TRIP CONTEXT FOR A SESSION
# --------------------------------------------------

def get_session_context(session_id: str):
    """
    Retrieve the trip ID associated with a session.
    Returns None if no trip has been associated.
    """

    if not session_id or not session_id.strip():
        raise ValueError("Session ID cannot be empty.")

    key = f"travel_assistant:context:{session_id}"

    return redis_client.get(key)
