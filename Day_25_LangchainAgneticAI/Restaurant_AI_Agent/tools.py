import json
from pathlib import Path 
from langchain.tools import tool 

DATA_FILE=Path(__file__).parent/"restaurants.json"

def load_restaurants():
    with open(DATA_FILE,"r") as file:
        return json.load(file)
    
@tool
def search_restaurants(query:str)->str:
    """Search restaurants using cuisine, restaurants name, or keyword.Return price and available seats. """
    if not query or not query.strip():
        return "Please provide a cuisine name or restaurants name"
    query=query.strip().lower()
    restaurants=load_restaurants()
    matches=[]

    for restaurant in restaurants:
        searchable_text=(restaurant["name"]+" "+restaurant["cuisine"]+" "+restaurant["location"]).lower()
        if query in searchable_text:
            matches.append(restaurant)
    if not matches:
        return f"No restaurants found for {query}"
    result="Matching Restaurants: \n"
    for r in matches:
        result+=(
            f"Restauran ID: {r['id']}\n"
            f"Name: {r['name']}\n"
            f"Cuisine: {r['cuisine']}\n"
            f"Location: {r['location']}\n"
            f"Price per person: {r['price_per_person']}\n"
            f"Available Seats: {r['available_seats']}\n"
            "...............................\n"
        )
    return result

@tool
def calculate_dining_cost(restaurant_id:str,guest_count:int)->str:
    """
    Calculate estimated dining cost using Restaurant_id and number of guests and guest count must be 1 to 20
    """

    try:
        guest_count=int(guest_count)
    except (TypeError,ValueError):
        return "Invalid guest count, Please enter a whole number"
    if guest_count<1 or guest_count>20:
        return (
            "Invalid guest count"
            "The number of guests must be between 1 and 20."
        )
    restaurants=load_restaurants()
    restaurant=next(
        ( r for r in restaurants if r["id"].lower()==str(restaurant_id).strip().lower()),
        None
    )
    if restaurant is None:
        return f"Restaurant '{restaurant_id}' does not exist "
    price=restaurant['price_per_person']
    total_cost=price*guest_count

    return(
        f"Restaurant: {restaurant['name']}\n"
        f"Guests: {guest_count}\n"
        f"Price per person: {price}\n"
        f"Total cousr: {total_cost}\n"
        "This is an estimated cost"
    )
    
