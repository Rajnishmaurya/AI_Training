import json
from pathlib import Path
from langchain.tools import tool

BASE_DIR = Path(__file__).parent

WORKSHOPS_FILE = BASE_DIR / "workshops.json"
COUPONS_FILE = BASE_DIR / "coupons.json"

def get_workshops():
    return json.loads(
        WORKSHOPS_FILE.read_text(encoding="utf-8")
    )

def get_coupons():
    return json.loads(
        COUPONS_FILE.read_text(encoding="utf-8")
    )

# TOOL 1: Search workshops by title
@tool
def search_workshops(keyword: str) -> str:
    """Search available workshops by title."""

    matches = [
        w for w in get_workshops()
        if keyword.lower() in w["title"].lower()
    ]
    return json.dumps(matches)

# TOOL 2: Calculate workshop fee
@tool
def calculate_workshop_fee(
    workshop_id: str,
    participants: int,
    coupon_code: str = ""
) -> str:
    """
    Calculate workshop fee for participants.
    Apply a valid coupon discount if provided.
    """

    if participants < 1 or participants > 30:
        return "Participant count must be between 1 and 30."

    for workshop in get_workshops():
        if workshop["id"] == workshop_id:
            original_total = workshop["fee"] * participants
            discount_percentage = 0
            discount_amount = 0
            coupon_status = "No coupon applied"

            # Validate coupon
            if coupon_code:
                coupons = get_coupons()
                for coupon in coupons:
                    if (
                        coupon["code"].upper()
                        == coupon_code.strip().upper()
                        and coupon["active"]
                    ):
                        discount_percentage = coupon["discount"]
                        discount_amount = round(
                            original_total * discount_percentage / 100,
                            2
                        )
                        coupon_status = "Coupon applied successfully"
                        break
                else:
                    coupon_status = "Invalid or inactive coupon code"
            final_total = round(
                original_total - discount_amount, 2
            )
            return json.dumps({
                "workshop": workshop["title"],
                "workshop_id": workshop_id,
                "participants": participants,
                "price_per_person": workshop["fee"],
                "original_total": original_total,
                "coupon_code": coupon_code or None,
                "coupon_status": coupon_status,
                "discount_percentage": discount_percentage,
                "discount_amount": discount_amount,
                "final_total": final_total
            })

    return "Workshop not found."

# TOOL 3: List all workshops
@tool
def list_all_workshops() -> str:
    """List all available workshops with their details."""
    workshops = get_workshops()
    if not workshops:
        return "No workshops are currently available."
    return json.dumps(workshops)

# TOOL 4: Find cheapest workshop
@tool
def find_cheapest_workshop() -> str:
    """Find the workshop with the lowest participation fee."""
    workshops = get_workshops()
    if not workshops:
        return "No workshops are currently available."

    cheapest = min(
        workshops,
        key=lambda workshop: workshop["fee"]
    )
    return json.dumps({
        "workshop": cheapest["title"],
        "workshop_id": cheapest["id"],
        "fee": cheapest["fee"]
    })

# TOOL 5: Validate coupon code
@tool
def validate_coupon(coupon_code: str) -> str:
    """Check whether a coupon code is valid and active."""
    coupons = get_coupons()
    for coupon in coupons:
        if (
            coupon["code"].upper()
            == coupon_code.strip().upper()
            and coupon["active"]
        ):
            return json.dumps({
                "valid": True,
                "coupon_code": coupon["code"],
                "discount": coupon["discount"],
                "message": "Coupon is valid."
            })

    return json.dumps({
        "valid": False,
        "message": "Invalid or inactive coupon code."
    })

if __name__ == "__main__":
    print("\n--- Search Workshops ---")
    print(search_workshops.invoke({
        "keyword": "Python"
    }))
    print("\n--- Calculate Fee ---")
    print(calculate_workshop_fee.invoke({
        "workshop_id": "W101",
        "participants": 4,
        "coupon_code": "SAVE10"
    }))
    print("\n--- All Workshops ---")
    print(list_all_workshops.invoke({}))
    print("\n--- Cheapest Workshop ---")
    print(find_cheapest_workshop.invoke({}))
    print("\n--- Validate Coupon ---")
    print(validate_coupon.invoke({
        "coupon_code": "SAVE10"
    }))
