import os
from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, ToolMessage
from langgraph.checkpoint.memory import InMemorySaver

from guardrails import contains_pii, clean_output

from tools import (
    search_workshops,
    calculate_workshop_fee,
    list_all_workshops,
    find_cheapest_workshop,
    validate_coupon
)

# STEP 1: Load environment
load_dotenv()

# STEP 2: Create model
model = ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),temperature=0)

# STEP 3: Register tools
tools = [search_workshops,calculate_workshop_fee,list_all_workshops,find_cheapest_workshop,validate_coupon]

# STEP 4: System prompt
SYSTEM_PROMPT = """
You are a helpful Workshop AI Assistant.

You can only answer questions about:
- Available workshops
- Workshop details
- Workshop fees
- Workshop comparisons
- Discounts and coupon codes

TOOL USAGE RULES:
1. When the user asks to search for a workshop,use search_workshops.
2. When the user asks to see all workshops,use list_all_workshops.
3. When the user asks for the cheapest workshop,use find_cheapest_workshop.
4. When the user asks for workshop fees,use calculate_workshop_fee.
5. When the user provides a coupon code,pass the coupon code to calculate_workshop_fee.
6. If the user asks whether a coupon is valid,use validate_coupon.
7. Never invent workshop names, IDs, prices,or coupon codes.
8. Only apply discounts returned by the coupon tool.
9. Remember the selected workshop and participant count during the conversation.
10. If the user selects a workshop but does not specify the participant count, ask for it.
11. If the user provides a coupon code before selecting a workshop, remember the coupon code.
12. If the coupon is invalid, clearly inform the user and show the original fee without a discount.
13. For unrelated questions, respond: "I can only help with workshops and their fees."
Always provide clear and friendly answers.
"""
# STEP 5: Create agent
agent = create_agent(model=model,tools=tools,system_prompt=SYSTEM_PROMPT,checkpointer=InMemorySaver())

# STEP 6: Run application
if __name__ == "__main__":
    thread_number = 1
    previous_count = 0
    print("===================================")
    print("    Workshop AI Agent")
    print("===================================")
    print("Type /new for a new conversation")
    print("Type exit to quit")
    while True:
        question = input("\nYou: ").strip()
        if question.lower() == "exit":
            break
        if question.lower() == "/new":
            thread_number += 1
            previous_count = 0
            print("New conversation started.")
            continue
        if not question:
            continue
        # Input guardrail
        if contains_pii(question):
            print("PII detected. Please remove personal contact details.")
            continue

        config = {
            "configurable": {
                "thread_id": f"workshop-{thread_number}"
            }
        }
        try:
            result = agent.invoke(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": question
                        }
                    ]
                },
                config=config
            )
            messages = result["messages"]
            new_messages = messages[previous_count:]
            previous_count = len(messages)
            # Display tool calls and results
            for message in new_messages:
                if isinstance(message, AIMessage):
                    for call in message.tool_calls:
                        print("\n[TOOL]:", call["name"])
                        print("Arguments:", call["args"])
                elif isinstance(message, ToolMessage):
                    print(
                        "\n[TOOL RESULT]:",
                        message.content
                    )
            # Output guardrail
            final_answer = clean_output(
                messages[-1].content
            )
            print("\nAgent:", final_answer)
        except Exception as error:
            print("Error:", error)
