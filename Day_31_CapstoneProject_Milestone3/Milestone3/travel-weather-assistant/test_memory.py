
from app.services.memory_service import (
    check_redis_connection,
    save_message,
    get_conversation_history,
    clear_session
)


TEST_SESSION_ID = "employee-session-EMP104"


def test_redis_connection():
    print("\n===== REDIS CONNECTION TEST =====")

    result = check_redis_connection()

    print("Redis connected:", result)


def test_save_messages():
    print("\n===== SAVE MESSAGES TEST =====")

    save_message(
        TEST_SESSION_ID,
        "user",
        "What weather should I expect in Jaipur?"
    )

    save_message(
        TEST_SESSION_ID,
        "assistant",
        "I will check the Jaipur weather forecast."
    )

    save_message(
        TEST_SESSION_ID,
        "user",
        "Will I need an umbrella there?"
    )

    print("Messages saved successfully.")


def test_retrieve_history():
    print("\n===== RETRIEVE HISTORY TEST =====")

    history = get_conversation_history(
        TEST_SESSION_ID
    )

    for message in history:
        print(f"{message['role']}: {message['content']}")


def test_session_isolation():
    print("\n===== SESSION ISOLATION TEST =====")

    other_session = "employee-session-EMP200"

    save_message(
        other_session,
        "user",
        "What is the weather in Mumbai?"
    )

    history = get_conversation_history(
        other_session
    )

    print("EMP200 session history:", history)

    original_history = get_conversation_history(
        TEST_SESSION_ID
    )

    print(
        "EMP104 message count:",
        len(original_history)
    )


def test_clear_session():
    print("\n===== CLEAR SESSION TEST =====")

    clear_session(TEST_SESSION_ID)

    history = get_conversation_history(
        TEST_SESSION_ID
    )

    print("History after clearing:", history)


if __name__ == "__main__":

    test_redis_connection()

    test_save_messages()

    test_retrieve_history()

    test_session_isolation()

    test_clear_session()
