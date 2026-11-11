import os
from agent_framework import Agent
from agent_framework.openai import OpenAIChatCompletionClient

from tools import search_products, calculate_order_total


def create_agents():

    # Shared model client using Chat Completions API
    client = OpenAIChatCompletionClient(
        model=os.getenv(
            "OPENROUTER_MODEL",
            "liquid/lfm-3-1.7b:free"
        ),
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1"
    )

    # Agent 1: Inventory
    inventory_agent = Agent(
        client=client,
        name="InventoryAgent",
        instructions=(
            "You are an inventory search specialist. "
            "Use search_products to find products matching "
            "the user's requested topic. "
            "List matching product IDs, titles and prices. "
            "Do not calculate total fees."
        ),
        tools=[search_products]
    )

    # Agent 2: Pricing
    pricing_agent = Agent(
        client=client,
        name="PricingAgent",
        instructions=(
            "You are an inventory pricing specialist. "
            "Read the previous search results and user request. "
            "Use calculate_order_total for each matching product "
            "using the requested number of participants. "
            "Report only verified totals. "
            "Never invent prices."
        ),
        tools=[calculate_order_total]
    )

    # Agent 3: Recommendation
    recommendation_agent = Agent(
        client=client,
        name="RecommendationAgent",
        instructions=(
            "You are an inventory recommendation specialist. "
            "Read the inventory and pricing results. "
            "Recommend the best matching product within the "
            "user's total budget. "
            "Explain your recommendation briefly. "
            "Use only verified inventory data and totals."
        )
    )

    return inventory_agent, pricing_agent, recommendation_agent