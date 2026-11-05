import re
import streamlit as st

from agent import (
    run_agent,
    SYSTEM_PROMPT,
    initialize_messages,
    confirm_reservation
)
# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="AI Library Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =====================================================
# 2. CUSTOM CSS - PREMIUM LIGHT THEME
# =====================================================

st.markdown("""
<style>

.stApp {
    background: #F7F8FA;
    color: #202123;
    font-family: Inter, -apple-system, BlinkMacSystemFont,
                 "Segoe UI", sans-serif;
}

header[data-testid="stHeader"] {
    background: #F7F8FA;
}

section[data-testid="stSidebar"] {
    background: #FFFFFF;
    border-right: 1px solid #E8E9ED;
}

section[data-testid="stSidebar"] > div {
    padding-top: 25px;
}

section[data-testid="stSidebar"] h2 {
    color: #202123;
    font-size: 23px;
    font-weight: 700;
}

section[data-testid="stSidebar"] p {
    color: #777B84;
    font-size: 13px;
}

section[data-testid="stSidebar"] .stButton button {
    background: transparent;
    color: #34363A;
    border: 1px solid transparent;
    border-radius: 9px;
    text-align: left;
    font-size: 14px;
    font-weight: 500;
}

section[data-testid="stSidebar"] .stButton button:hover {
    background: #F0F1F3;
    border-color: #E5E6E9;
    color: #111111;
}

.main-title {
    text-align: center;
    font-size: 34px;
    font-weight: 700;
    letter-spacing: -1.2px;
    color: #202123;
    margin-top: 25px;
    margin-bottom: 8px;
}

.subtitle {
    text-align: center;
    color: #858994;
    font-size: 14px;
    margin-bottom: 35px;
}

div[data-testid="stChatMessage"] {
    background: transparent;
    border: none;
    padding: 16px 18px;
    border-radius: 14px;
    margin-bottom: 8px;
}

div[data-testid="stChatMessage"]:hover {
    background: #F1F2F5;
}

div[data-testid="stChatMessage"] p {
    color: #292B30;
    font-size: 15px;
    line-height: 1.75;
}

div[data-testid="stChatInput"] {
    background: #FFFFFF;
    border: 1px solid #DADCE2;
    border-radius: 18px;
    box-shadow: 0 4px 18px rgba(0,0,0,0.045);
    padding: 5px;
}

div[data-testid="stChatInput"]:focus-within {
    border-color: #A5A8B0;
}

div[data-testid="stChatInput"] textarea {
    color: #202123 !important;
    font-size: 15px;
}

.stButton button {
    border-radius: 10px;
    font-weight: 600;
    transition: all 0.2s ease;
}

.stButton button[kind="primary"] {
    background: #202123;
    color: white;
    border: 1px solid #202123;
}

.stButton button[kind="primary"]:hover {
    background: #383A40;
    border-color: #383A40;
}

hr {
    border-color: #E8E9ED;
}

.reservation-card {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 16px;
    padding: 22px;
    margin: 15px 0;
    box-shadow: 0 3px 12px rgba(0,0,0,0.035);
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# 3. SESSION STATE INITIALIZATION
# =====================================================

def initialize_state():

    if "messages" not in st.session_state:

        st.session_state.messages = initialize_messages()

    if "pending_reservation" not in st.session_state:

        st.session_state.pending_reservation = None

    if "pending_prompt" not in st.session_state:

        st.session_state.pending_prompt = None


initialize_state()


# =====================================================
# 4. HELPER FUNCTIONS
# =====================================================

def add_assistant_message(message):

    st.session_state.messages.append({

        "role": "assistant",

        "content": message

    })


def is_confirmation(message):

    message = message.strip().lower()

    patterns = [
        r"^(yes|yeah|yep|sure|confirm)$",
        r"^(yes|yeah|yep|sure),?\s+(please\s+)?(reserve|book|proceed|confirm).*$",
        r"^(please\s+)?(confirm|proceed|go ahead|book it|reserve it)$",
        r"^i confirm.*$"
    ]

    return any(
        re.match(pattern, message)
        for pattern in patterns
    )


def is_cancellation(message):

    message = message.strip().lower()

    patterns = [
        r"^(no|nope|cancel)$",
        r"^(no|please cancel).*$",
        r"^(cancel|abort)\s+(the\s+)?(reservation|booking)$"
    ]

    return any(
        re.match(pattern, message)
        for pattern in patterns
    )


def process_confirmation():

    pending = st.session_state.pending_reservation

    if not pending:
        return

    result = confirm_reservation(pending)

    if result["success"]:

        reservation = result["reservation"]

        reply = (
            "🎉 **Your reservation was successful!**\n\n"
            f"**Book:** {reservation['book_title']}\n\n"
            f"**Book ID:** {reservation['book_id']}\n\n"
            f"**Customer:** {reservation['customer_name']}\n\n"
            f"**Reservation ID:** {reservation['reservation_id']}\n\n"
            f"**Remaining copies:** {result['remaining_copies']}\n\n"
            "Thank you for using AI Library Assistant! 📚"
        )

    else:

        reply = (
            "Sorry, your reservation could not be completed.\n\n"
            f"{result['message']}"
        )

    st.session_state.pending_reservation = None

    add_assistant_message(reply)


def process_cancellation():

    st.session_state.pending_reservation = None

    add_assistant_message(
        "Your reservation request has been cancelled. 😊"
    )


# =====================================================
# 5. SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown("## 📚 AI Library")

    st.caption("Your intelligent library companion")

    st.divider()

    # NEW CHAT

    if st.button(
        "＋ New Chat",
        use_container_width=True
    ):

        st.session_state.messages = initialize_messages()

        st.session_state.pending_reservation = None

        st.session_state.pending_prompt = None

        st.rerun()

    st.divider()

    st.markdown("### Explore")

    if st.button(
        "🔍 Search Books",
        use_container_width=True
    ):

        st.session_state.pending_prompt = (
            "Show me all books in the library."
        )

        st.rerun()

    if st.button(
        "💻 Programming Books",
        use_container_width=True
    ):

        st.session_state.pending_prompt = (
            "Find books related to programming."
        )

        st.rerun()

    if st.button(
        "🤖 Artificial Intelligence",
        use_container_width=True
    ):

        st.session_state.pending_prompt = (
            "Find books related to Artificial Intelligence."
        )

        st.rerun()

    st.divider()

    st.markdown("### About")

    st.caption(
        "An AI-powered library assistant built with "
        "Python, Streamlit and OpenRouter."
    )

    st.divider()

    if st.button(
        "🗑️ Clear Conversation",
        use_container_width=True
    ):

        st.session_state.messages = initialize_messages()

        st.session_state.pending_reservation = None

        st.rerun()


# =====================================================
# 6. MAIN HEADER
# =====================================================

st.markdown(
    """
    <div class="main-title">
        📚 AI Library Assistant
    </div>

    <div class="subtitle">
        Your personal AI companion for discovering books
    </div>
    """,
    unsafe_allow_html=True
)


# =====================================================
# 7. DISPLAY CHAT HISTORY
# =====================================================

for message in st.session_state.messages:

    if message["role"] == "system":
        continue

    if message["role"] not in ["user", "assistant"]:
        continue

    avatar = (
        "🧑"
        if message["role"] == "user"
        else "📚"
    )

    with st.chat_message(
        message["role"],
        avatar=avatar
    ):

        st.markdown(message.get("content") or "")


# =====================================================
# 8. PENDING RESERVATION CARD
# =====================================================

pending = st.session_state.pending_reservation

if pending:

    st.divider()

    st.markdown("### 📖 Reservation Confirmation")

    st.write(
        "Please review your reservation details."
    )

    with st.container(border=True):

        st.markdown(
            f"### 📚 {pending['book_title']}"
        )

        st.write("**Book ID:**", pending["book_id"])

        st.write(
            "**Customer Name:**",
            pending["customer_name"]
        )

        st.write(
            "**Available Copies:**",
            pending["available_copies"]
        )

        st.info(
            "Your book has not been reserved yet. "
            "Please confirm to complete the reservation."
        )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "✅ Confirm Reservation",
            type="primary",
            use_container_width=True,
            key="confirm_reservation_button"
        ):

            try:

                process_confirmation()

            except Exception as e:

                st.error(
                    f"Reservation error: {str(e)}"
                )

            st.rerun()

    with col2:

        if st.button(
            "❌ Cancel Reservation",
            use_container_width=True,
            key="cancel_reservation_button"
        ):

            process_cancellation()

            st.rerun()


# =====================================================
# 9. CHAT INPUT
# =====================================================

prompt = st.chat_input(
    "Message AI Library Assistant..."
)


# Handle sidebar prompts

if st.session_state.pending_prompt:

    prompt = st.session_state.pending_prompt

    st.session_state.pending_prompt = None


# =====================================================
# 10. PROCESS USER MESSAGE
# =====================================================

if prompt:

    # Save user message

    st.session_state.messages.append({

        "role": "user",

        "content": prompt

    })

    # ---------------------------------
    # HANDLE PENDING RESERVATION
    # ---------------------------------

    pending = st.session_state.pending_reservation

    if pending:

        if is_confirmation(prompt):

            with st.chat_message("assistant", avatar="📚"):

                with st.spinner("Processing your reservation..."):

                    try:

                        process_confirmation()

                        latest_message = (
                            st.session_state.messages[-1]["content"]
                        )

                        st.markdown(latest_message)

                    except Exception as e:

                        st.error(
                            f"Reservation error: {str(e)}"
                        )

            st.rerun()

        elif is_cancellation(prompt):

            process_cancellation()

            st.rerun()

        else:

            reply = (
                "You currently have a pending reservation for "
                f"**{pending['book_title']}** under "
                f"**{pending['customer_name']}**.\n\n"
                "Please type **Yes, reserve** to confirm or "
                "**No, cancel** to cancel it before starting "
                "another request."
            )

            add_assistant_message(reply)

            st.rerun()

    # ---------------------------------
    # NORMAL CHAT PROCESSING
    # ---------------------------------

    with st.chat_message("user", avatar="🧑"):

        st.markdown(prompt)

    with st.chat_message("assistant", avatar="📚"):

        with st.spinner("Thinking..."):

            try:

                agent_result = run_agent(
                    st.session_state.messages
                )

                response = agent_result["response"]

                pending_reservation = agent_result[
                    "pending_reservation"
                ]

                # Save validated pending reservation

                if pending_reservation:

                    st.session_state.pending_reservation = (
                        pending_reservation
                    )

                st.markdown(response)

            except Exception as e:

                st.error(
                    "Something went wrong while processing your request."
                )

                st.exception(e)

                st.session_state.messages.pop()

                st.stop()

    st.rerun()
