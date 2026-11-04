import os
import json

from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

from tools import search_books, reserve_book


# --------------------------------------------------
# 2. Configuration
# --------------------------------------------------

ROOT = Path(__file__).resolve().parent

load_dotenv(ROOT / ".env")

API_KEY = os.getenv("OPENROUTER_API_KEY")

if not API_KEY:
    raise SystemExit(
        "Missing OPENROUTER_API_KEY. "
        "Add it to your .env file."
    )

MODEL = os.getenv(
    "OPENROUTER_MODEL",
    "openrouter/free"
)

# OpenRouter provides OpenAI-compatible API

client = OpenAI(
    api_key=API_KEY,
    base_url="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "http://localhost",
        "X-Title": "AI Library Assistant",
    },
)

print("OpenRouter initialized successfully!")
print("Selected Model:", MODEL)

tools = [
    {
        "type": "function",
        "function": {
            "name": "search_books",
            "description": (
                "Search library books using a title, "
                "author, category, or keyword."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "Book title or search keyword"
                    }
                },
                "required": ["keyword"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "reserve_book",
            "description": (
                "Reserve a book for a customer using "
                "its book ID and customer name. "
                "Always use this tool for reservation requests. "
                "The Python function itself asks for confirmation. "
                "Never claim a reservation is complete unless "
                "the tool confirms success."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "book_id": {
                        "type": "integer",
                        "description": "Unique ID of the book"
                    },
                    "customer_name": {
                        "type": "string",
                        "description": "Name of the customer"
                    }
                },
                "required": ["book_id", "customer_name"],
                "additionalProperties": False
            }
        }
    }
]

# Execute the selected Python function
def execute_tool(tool_name, arguments):
    if tool_name == "search_books":
        return search_books(**arguments)
    elif tool_name == "reserve_book":
        return reserve_book(**arguments)

    return {
        "success": False,
        "message": "Unknown tool."
    }


# Main AI Agent
def run_agent(user_input):
    messages = [
        {
            "role": "system",
            "content": """
            You are an AI Library Assistant.
            Your responsibilities:

            1. Search books using search_books.
            2. Reserve books using reserve_book.
            3. Use actual book IDs returned by searches.
            4. If the user asks to reserve a book by title,search for it first if its ID is unknown.
            5. If multiple matching books exist, ask the user which book they mean.
            6. Never claim a reservation succeeded unless the Python tool confirms success.
            7. Never invent book availability or reservation data.
            8. Explain tool results clearly to the user.
            """
        },
        {
            "role": "user",
            "content": user_input
        }
    ]

    while True:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        assistant_message = response.choices[0].message

        messages.append(assistant_message)

        # Check whether AI selected a tool
        if assistant_message.tool_calls:
            for tool_call in assistant_message.tool_calls:
                tool_name = tool_call.function.name
                arguments = json.loads(
                    tool_call.function.arguments
                )

                # Display selected tool
                print("\n[AI Agent Decision]")
                print("Selected Tool:", tool_name)
                print("Arguments:", arguments)

                # Execute Python function
                result = execute_tool(
                    tool_name,
                    arguments
                )

                print("Tool Result:", result)

                # Send result back to AI
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                })

        else:
            # Display final AI response
            print("\nLibrary Assistant:")
            print(assistant_message.content)

            break


# Run application

if __name__ == "__main__":

    print("================================")
    print("     AI LIBRARY ASSISTANT")
    print("================================")

    print("Type 'exit' to stop.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "exit":
            print("Thank you for using the Library Assistant!")
            break
        if not user_input:
            continue
        try:
            run_agent(user_input)

        except Exception as error:
            print("Error:", error)
