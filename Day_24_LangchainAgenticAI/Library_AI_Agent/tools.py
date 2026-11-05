
import json
from pathlib import Path
from datetime import datetime
from threading import RLock


# =====================================================
# FILE CONFIGURATION
# =====================================================

BASE_DIR = Path(__file__).resolve().parent

BOOKS_FILE = BASE_DIR / "books.json"
RESERVATIONS_FILE = BASE_DIR / "reservations.json"

# Protect JSON updates from simultaneous operations
FILE_LOCK = RLock()


# =====================================================
# JSON HELPERS
# =====================================================

def read_json(file_path):

    if not file_path.exists():

        if file_path == RESERVATIONS_FILE:
            write_json(file_path, [])
            return []

        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def write_json(file_path, data):

    temp_file = file_path.with_suffix(
        file_path.suffix + ".tmp"
    )

    with open(temp_file, "w", encoding="utf-8") as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )

    temp_file.replace(file_path)


# =====================================================
# TOOL 1: SEARCH BOOKS
# =====================================================

def search_books(keyword):

    try:

        books = read_json(BOOKS_FILE)

        keyword = str(keyword).strip().casefold()

        if not keyword:

            return {
                "success": False,
                "message": "Please provide a search keyword."
            }

        # Support requests to show all books

        if keyword in ["*", "all", "all books", "everything"]:

            matching_books = books

        else:

            matching_books = []

            for book in books:

                searchable_text = " ".join([
                    str(book.get("title", "")),
                    str(book.get("author", "")),
                    str(book.get("category", ""))
                ]).casefold()

                if keyword in searchable_text:
                    matching_books.append(book)

        if not matching_books:

            return {
                "success": False,
                "total_results": 0,
                "message": (
                    f"No books found matching '{keyword}'."
                )
            }

        return {
            "success": True,
            "total_results": len(matching_books),
            "books": matching_books
        }

    except Exception as e:

        return {
            "success": False,
            "message": f"Book search failed: {str(e)}"
        }


# =====================================================
# TOOL 2: CHECK BOOK AVAILABILITY
# =====================================================

def check_book_availability(book_id):

    try:

        books = read_json(BOOKS_FILE)

        selected_book = next(
            (
                book for book in books
                if book["id"] == book_id
            ),
            None
        )

        if selected_book is None:

            return {
                "success": False,
                "message": "Book ID not found."
            }

        copies = selected_book["available_copies"]

        return {

            "success": True,

            "book": selected_book,

            "available": copies > 0,

            "available_copies": copies,

            "message": (
                "Book is available."
                if copies > 0
                else "Book is currently unavailable."
            )

        }

    except Exception as e:

        return {
            "success": False,
            "message": f"Availability check failed: {str(e)}"
        }


# =====================================================
# TOOL 3: PREPARE RESERVATION
# =====================================================

def prepare_reservation(book_id, customer_name):

    """
    Prepare a reservation without modifying inventory.

    This function is called by the AI agent.
    Actual reservation happens only after confirmation.
    """

    try:

        if not isinstance(book_id, int) or isinstance(book_id, bool):

            return {
                "success": False,
                "message": "Invalid book ID."
            }

        if not isinstance(customer_name, str):

            return {
                "success": False,
                "message": "Invalid customer name."
            }

        customer_name = customer_name.strip()

        if not customer_name:

            return {
                "success": False,
                "message": "Customer name is required."
            }

        books = read_json(BOOKS_FILE)

        selected_book = next(
            (
                book for book in books
                if book["id"] == book_id
            ),
            None
        )

        if selected_book is None:

            return {
                "success": False,
                "message": "Book ID not found."
            }

        if selected_book["available_copies"] <= 0:

            return {
                "success": False,
                "message": "This book is currently unavailable."
            }

        pending_reservation = {

            "book_id": selected_book["id"],

            "book_title": selected_book["title"],

            "customer_name": customer_name,

            "available_copies": selected_book["available_copies"]

        }

        return {

            "success": True,

            "pending_reservation": pending_reservation,

            "message": (
                "Reservation prepared. "
                "Waiting for explicit user confirmation."
            )

        }

    except Exception as e:

        return {
            "success": False,
            "message": f"Unable to prepare reservation: {str(e)}"
        }


# =====================================================
# TOOL 4: EXECUTE RESERVATION
# =====================================================

def confirm_and_reserve(book_id, customer_name):

    """
    Execute the reservation after the user confirms.

    This function must only be called by the
    application's confirmation handler.
    """

    try:

        if not isinstance(book_id, int) or isinstance(book_id, bool):

            return {
                "success": False,
                "message": "Invalid book ID."
            }

        if not isinstance(customer_name, str):

            return {
                "success": False,
                "message": "Invalid customer name."
            }

        customer_name = customer_name.strip()

        if not customer_name:

            return {
                "success": False,
                "message": "Customer name is required."
            }

        with FILE_LOCK:

            books = read_json(BOOKS_FILE)
            reservations = read_json(RESERVATIONS_FILE)

            selected_book = next(
                (
                    book for book in books
                    if book["id"] == book_id
                ),
                None
            )

            if selected_book is None:

                return {
                    "success": False,
                    "message": "Book ID not found."
                }

            if selected_book["available_copies"] <= 0:

                return {
                    "success": False,
                    "message": "Sorry, this book is no longer available."
                }

            reservation_id = max(
                [
                    r.get("reservation_id", 0)
                    for r in reservations
                ],
                default=0
            ) + 1

            reservation = {

                "reservation_id": reservation_id,

                "book_id": book_id,

                "book_title": selected_book["title"],

                "customer_name": customer_name,

                "reservation_date": datetime.now().isoformat(
                    timespec="seconds"
                )

            }

            # Update inventory

            selected_book["available_copies"] -= 1

            # Save reservation and inventory

            write_json(BOOKS_FILE, books)

            reservations.append(reservation)

            write_json(RESERVATIONS_FILE, reservations)

            return {

                "success": True,

                "reservation": reservation,

                "remaining_copies": selected_book["available_copies"],

                "message": "Book reserved successfully!"

            }

    except Exception as e:

        return {
            "success": False,
            "message": f"Reservation failed: {str(e)}"
        }
