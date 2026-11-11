import json
from pathlib import Path
from agent_framework import tool

DATA_FILE = Path(__file__).parent / "products.json"

def load_products():
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))

# Tool 1: Search products
@tool(approval_mode="never_require")
def search_products(topic: str) -> str:
    """Find products matching a topic or title."""

    print(f"[TOOL CALLED] search_products: {topic}")

    matches = [
        w for w in load_products()
        if topic.lower() in w["title"].lower()
    ]

    return json.dumps(matches)


# Tool 2: Calculate fees
@tool(approval_mode="never_require")
def calculate_order_total(product_id: str, participants: int) -> str:
    """Calculate total products fee for a given group size."""

    print(f"[TOOL CALLED] calculate_fee: {product_id}, {participants}")

    if participants < 1 or participants > 30:
        return "Participants must be between 1 and 30."

    for w in load_products():
        if w["id"].upper() == product_id.upper():
            return json.dumps({
                "product": w["title"],
                "participants": participants,
                "fee_per_person": w["fee"],
                "total_fee": w["fee"] * participants,
                "currency": "INR"
            })

    return "Product not found."
