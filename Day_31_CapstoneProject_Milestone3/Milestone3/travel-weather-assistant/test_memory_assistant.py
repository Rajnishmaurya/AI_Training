
from app.agent.travel_assistant import ask_travel_assistant
from app.services.memory_service import (
    get_conversation_history,
    clear_session
)

TEST_SESSION_ID = "travel-session-EMP104"

TEST_TRIP_ID = "beb29003-d5fc-409d-ac69-dda4dfd3698f"


def test_first_message():

    print("\n===== FIRST MESSAGE =====")

    result = ask_travel_assistant(
        session_id=TEST_SESSION_ID,
        trip_id=TEST_TRIP_ID,
        question="What weather should I expect for my trip?"
    )

    print(result)


def test_follow_up():

    print("\n===== FOLLOW-UP MESSAGE =====")

    result = ask_travel_assistant(
        session_id=TEST_SESSION_ID,
        question="Will I need an umbrella there?"
    )

    print(result)


def test_conversation_history():

    print("\n===== CONVERSATION HISTORY =====")

    history = get_conversation_history(TEST_SESSION_ID)

    for message in history:
        print(f"{message['role']}: {message['content']}")


if __name__ == "__main__":

    # Start with a clean session
    clear_session(TEST_SESSION_ID)

    test_first_message()

    test_follow_up()

    test_conversation_history()
