import asyncio
import os
from dotenv import load_dotenv
from agent_framework.openai import OpenAIChatCompletionClient

load_dotenv()

async def main():
    client = OpenAIChatCompletionClient(
        model=os.getenv("OPENROUTER_MODEL"),
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1",
    )

    response = await client.get_response(
        messages="Say hello in one sentence."
    )

    print(response)

    await client.close()


asyncio.run(main())