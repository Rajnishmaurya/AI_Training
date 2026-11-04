import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent

BOOKS_FILE = BASE_DIR / "books.json"
RESERVATIONS_FILE = BASE_DIR / "reservations.json"


def read_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def write_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


# TOOL 1: SEARCH BOOKS

def search_books(keyword):
    books = read_json(BOOKS_FILE)

    keyword = keyword.lower().strip()

    matching_books = []

    for book in books:
        searchable_text = (
            book["title"] + " " +
            book["author"] + " " +
            book["category"]
        ).lower()

        if keyword in searchable_text:
            matching_books.append(book)

    if not matching_books:
        return {
            "success": False,
            "message": "No matching books found."
        }

    return {
        "success": True,
        "books": matching_books
    }


# TOOL 2: RESERVE BOOK

def reserve_book(book_id, customer_name):
    books = read_json(BOOKS_FILE)
    reservations = read_json(RESERVATIONS_FILE)
    selected_book = None
    for book in books:
        if book["id"] == book_id:
            selected_book = book
            break
    if selected_book is None:
        return {
            "success": False,
            "message": "Book ID not found."
        }
    if selected_book["available_copies"] <= 0:
        return {
            "success": False,
            "message": "Sorry, this book is currently unavailable."
        }
    # Ask for confirmation before reserving
    print("\nReservation Confirmation")
    print("------------------------")
    print("Book:", selected_book["title"])
    print("Customer:", customer_name)

    confirmation = input(
        "Do you want to confirm this reservation? (yes/no): "
    ).strip().lower()

    if confirmation not in ["yes", "y"]:
        return {
            "success": False,
            "message": "Reservation cancelled by user."
        }

    # Reduce available copies
    selected_book["available_copies"] -= 1

    # Create reservation
    reservation = {
        "reservation_id": len(reservations) + 1,
        "book_id": book_id,
        "book_title": selected_book["title"],
        "customer_name": customer_name,
        "reservation_date": datetime.now().isoformat(
            timespec="seconds"
        )
    }

    reservations.append(reservation)

    # Save updated JSON files
    write_json(BOOKS_FILE, books)
    write_json(RESERVATIONS_FILE, reservations)

    return {
        "success": True,
        "reservation": reservation,
        "remaining_copies": selected_book["available_copies"],
        "message": "Book reserved successfully!"
    }
