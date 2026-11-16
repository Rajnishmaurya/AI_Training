from app.agent.llm import get_llm

print("Initializing LangChain with Qwen2.5...")

llm = get_llm()

print("Model initialized successfully!")

response = llm.invoke(
    """
    You are a professional business travel assistant.

    Explain three essential things an employee should
    pack for a business trip to Jaipur.
    """
)

print("\n===== LANGCHAIN RESPONSE =====")
print(response.content)