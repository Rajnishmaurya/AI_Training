import os 
import uuid
from dotenv import load_dotenv 
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver 
from langchain_openrouter import ChatOpenRouter
import traceback
from tools import (search_restaurants,calculate_dining_cost)

from guardrails import(
    validate_input,
    is_restaurant_related,
    redact_pii,
    redacted_output
)

load_dotenv()

SYSTEM_PROMPT="""
You are an AI restaurant reservation assistant.

Your responsibilities:
1. Help users discover restaurants
2. search restaurants bt cuisine or keywords
3. display restaurant prices and seating availability
4. calculate estimated dining cost
5. remember previous restaurants selection 
6. remember previous guest counts
7. handle contextual followup question 

IMPORTANT RULES:
- Only restaurant related question
- use the available python tools for restaurant information
- never invent restaurant name, restaurant prices
- never clai that a reservation is confirmed
- do not process actual payments
- do not have make real restauraunts bookins


"""

def build_agent():
    load_dotenv()
    api_key=os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY is missing from .env")
    model_name=os.getenv("OPENROUTER_MODEL","recursive/flint-v1.0:free")

    model=ChatOpenRouter(
        model=model_name,
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
        temperature=0
    )
    #Conversation memory
    memory=InMemorySaver()
    tools=[search_restaurants,calculate_dining_cost]

    agent=create_agent(
        model=model,
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
        checkpointer=memory
    )
    return agent 

def run_cli():
    agent=build_agent() 

    #Unique conversation ID
    thread_id=str(uuid.uuid4())
    conversation_started=False 
    print("\n")
    print("RESTAURANT AI ASSISTANT")
    print("\n")
    print("Type /new to start a new conversation")
    print("Type /exit to quit.")

    while True:
        user_input=input("You: ").strip()

        if not user_input:
            print("Assistant: Please enter a question.\n")
            continue 
        if user_input.lower() in ["/exit","exit","quit"]:
            print("Assistant: Goodbye")
            break 
        if user_input.lower()=="/new":
            thread_id=str(uuid.uuid4())
            conversation_started=False 
            print("Assistant: New conversation started"
            "Previously memory is cleared. \n")
            continue 
        valid,error_message=validate_input(user_input)
        if not valid:
            print(f"Assistant: {error_message}\n")
            continue
        safe_input,pii_found=redact_pii(user_input)
        if pii_found and not is_restaurant_related(safe_input):
            print("Assistant: Personal contact infromation detected"
            "It has been redacted,please ask a restaurant related question \n")
            continue
        #context followup handling 
        short_followups={
            "yes","no","that one","same restaurant","make it 6 people", "6 people","4 people","increase it to 6","what about 6"
        }

        is_followup=(conversation_started and (len(safe_input.split())<=5 or safe_input.lower() in short_followups))

        if not is_restaurant_related(safe_input) and not is_followup:
            print(
                "Assistant: I can only answer questions"
                "related to restaurants,cuisines,seating availability and dining costs. \n"
            )
            continue 
        try:
            response=agent.invoke(
                {
                    "message":[
                        {
                            "role":"user",
                            "content":safe_input
                        }
                    ]
                },
                config={
                    "configurable":{
                        "thread_id":thread_id
                    }
                }
            )

            for message in response["messages"]:
                tool_calls=getattr(
                    message,
                    "tool_calls",
                    []
                ) or []
                
                for tool_call in tool_calls:
                    print("\n [TOOL EXECUTION]")
                    print("Tool name:",tool_call["name"])
                    print("Arguments:",tool_call["args"])
            
            final_message=response["messages"][-1].content 
            if isinstance(final_message,list):
                final_message=" ".join(item.get("text","")
                if isinstance(item, dict)
                else str(item)
                for item in final_message)
            
            final_message=redacted_output(str(final_message))

            print("Final message: ", final_message)

            if pii_found:
                print("\n Privacy notice: Contact information in your message was redacted")
            
            conversation_started=True 
        except Exception as error:
            print("\n error type:", type(error).__name__)
            print("error message:",repr(error))
            traceback.print_exc()
            print("please check the complete traceback above")

if __name__=="__main__":
    run_cli()
