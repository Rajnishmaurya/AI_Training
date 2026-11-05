import os
import json
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

from tools import (
    search_books,
    check_book_availability,
    prepare_reservation,
    confirm_and_reserve
)
# =====================================================
# 1. ENVIRONMENT CONFIGURATION
# =====================================================

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")
API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    raise ValueError(
        "Missing OPENROUTER_API_KEY in .env"
    )
MODEL = os.getenv(
    "OPENROUTER_MODEL",
    "openrouter/free"
)
# =====================================================
# 2. OPENROUTER CLIENT
# =====================================================
client = OpenAI(
    api_key=API_KEY,
    base_url="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "http://localhost",
        "X-Title": "AI Library Assistant"
    }
)
# =====================================================
# 3. SYSTEM PROMPT
# =====================================================
SYSTEM_PROMPT = """
You are an intelligent AI Library Assistant.

Your job is to help users search books,
check availability and prepare book reservations.

AVAILABLE TOOLS:

1. search_books
2. check_book_availability
3. prepare_reservation

BOOK SEARCH RULES:

1. Always use search_books when a user asks to find, search or discover books.
2. Search by the relevant title, author, category or keyword.
3. For example, if the user asks: "Find books related to Python"

   Call search_books with:
   keyword = "python"
4. Never invent book information.
5. Show actual titles, authors, categories, book IDs and available copies returned by the tools.
6. If no books are found, explain that clearly.

AVAILABILITY RULES:
1. Always check availability before preparing
   a reservation.
2. Use the actual book ID returned by search_books.
3. Never invent available copies.
4. If the book is unavailable, explain that it cannot currently be reserved.

RESERVATION RULES:

1. If the user requests a reservation, first search for the requested book.
2. If multiple books match, ask the user which book they want.
3. Ask for the customer name if missing.
4. Check book availability.
5. Once you have the correct book ID and customer name, call prepare_reservation.
6. prepare_reservation does not actually reserve the book. It only prepares a pending reservation.

7. When prepare_reservation succeeds, clearly show the following:

   - Book title
   - Book ID
   - Customer name
   - Available copies

8. Ask the user for explicit confirmation.

9. NEVER claim that a reservation has succeeded
   merely because prepare_reservation succeeded.

10. The actual reservation is executed by the
    application after explicit user confirmation.

11. If the user declines, the reservation must
    not be executed.


GENERAL RULES:

1. Maintain conversation context.

2. Be friendly and professional.

3. Give clear, readable answers.

4. Use Markdown formatting when presenting books.

5. Never invent reservation IDs.

6. Never claim an action succeeded unless
   the corresponding Python tool confirms success.
"""


# =====================================================
# 4. TOOL DEFINITIONS
# =====================================================

tools = [

    # ---------------------------------
    # SEARCH BOOKS
    # ---------------------------------

    {
        "type": "function",

        "function": {

            "name": "search_books",

            "description": (
                "Search books by title, author, category "
                "or keyword. For example, use keyword "
                "'python' to find Python books."
            ),

            "parameters": {

                "type": "object",

                "properties": {

                    "keyword": {
                        "type": "string"
                    }

                },

                "required": ["keyword"],

                "additionalProperties": False

            }

        }

    },

    # ---------------------------------
    # CHECK AVAILABILITY
    # ---------------------------------

    {
        "type": "function",

        "function": {

            "name": "check_book_availability",

            "description": (
                "Check the available copies of a book "
                "using its actual book ID."
            ),

            "parameters": {

                "type": "object",

                "properties": {

                    "book_id": {
                        "type": "integer"
                    }

                },

                "required": ["book_id"],

                "additionalProperties": False

            }

        }

    },

    # ---------------------------------
    # PREPARE RESERVATION
    # ---------------------------------

    {
        "type": "function",

        "function": {

            "name": "prepare_reservation",

            "description": (
                "Prepare a reservation after checking "
                "availability and collecting the customer "
                "name. This does NOT reserve the book. "
                "It only returns validated reservation "
                "details for the application to request "
                "user confirmation."
            ),

            "parameters": {

                "type": "object",

                "properties": {

                    "book_id": {
                        "type": "integer"
                    },

                    "customer_name": {
                        "type": "string"
                    }

                },

                "required": [
                    "book_id",
                    "customer_name"
                ],

                "additionalProperties": False

            }

        }

    }

]


# =====================================================
# 5. TOOL EXECUTION
# =====================================================

def execute_tool(tool_name, arguments):

    if tool_name == "search_books":

        return search_books(**arguments)

    elif tool_name == "check_book_availability":

        return check_book_availability(**arguments)

    elif tool_name == "prepare_reservation":

        return prepare_reservation(**arguments)

    return {

        "success": False,

        "message": "Unknown tool."

    }


# =====================================================
# 6. INITIALIZE CONVERSATION
# =====================================================

def initialize_messages():

    return [

        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },

        {
            "role": "assistant",
            "content": (
                "Hello! 👋 Welcome to your AI Library Assistant.\n\n"
                "I can help you discover books, check availability "
                "and reserve books. What would you like to do today?"
            )
        }

    ]


# =====================================================
# 7. RUN AGENT
# =====================================================

def run_agent(messages):

    max_iterations = 8

    pending_reservation = None

    for _ in range(max_iterations):

        response = client.chat.completions.create(

            model=MODEL,

            messages=messages,

            tools=tools,

            tool_choice="auto",

            temperature=0.3

        )

        assistant_message = response.choices[0].message

        # Save assistant message

        messages.append(
            assistant_message.model_dump(exclude_none=True)
        )

        # ---------------------------------
        # HANDLE TOOL CALLS
        # ---------------------------------

        if assistant_message.tool_calls:

            for tool_call in assistant_message.tool_calls:

                tool_name = tool_call.function.name

                try:

                    arguments = json.loads(
                        tool_call.function.arguments
                    )

                    print("\nSelected Tool:", tool_name)

                    print("Arguments:", arguments)

                    result = execute_tool(
                        tool_name,
                        arguments
                    )

                    print("Tool Result:", result)

                    # Capture trusted pending reservation

                    if (
                        tool_name == "prepare_reservation"
                        and result.get("success")
                    ):

                        pending_reservation = result[
                            "pending_reservation"
                        ]

                    # Return tool result to LLM

                    messages.append({

                        "role": "tool",

                        "tool_call_id": tool_call.id,

                        "content": json.dumps(result)

                    })

                except Exception as e:

                    messages.append({

                        "role": "tool",

                        "tool_call_id": tool_call.id,

                        "content": json.dumps({

                            "success": False,

                            "message": str(e)

                        })

                    })

        # ---------------------------------
        # FINAL AI RESPONSE
        # ---------------------------------

        else:

            return {

                "response": assistant_message.content or "",

                "pending_reservation": pending_reservation

            }

    return {

        "response": (
            "I'm having difficulty completing your request. "
            "Please try again."
        ),

        "pending_reservation": pending_reservation

    }


# =====================================================
# 8. CONFIRM RESERVATION
# =====================================================

def confirm_reservation(pending):

    """
    Execute a reservation using validated pending
    reservation details supplied by the application.
    """

    if not isinstance(pending, dict):

        return {
            "success": False,
            "message": "Invalid pending reservation."
        }

    required_fields = [
        "book_id",
        "book_title",
        "customer_name"
    ]

    if not all(field in pending for field in required_fields):

        return {
            "success": False,
            "message": "Incomplete reservation details."
        }

    # Revalidate the book and customer before execution

    if not isinstance(pending["book_id"], int):

        return {
            "success": False,
            "message": "Invalid book ID."
        }

    if not isinstance(pending["customer_name"], str):

        return {
            "success": False,
            "message": "Invalid customer name."
        }

    if not pending["customer_name"].strip():

        return {
            "success": False,
            "message": "Customer name is required."
        }

    return confirm_and_reserve(

        book_id=pending["book_id"],

        customer_name=pending["customer_name"]

    )
