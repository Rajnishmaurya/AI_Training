
from app.database import init_db, DATABASE_PATH
from app.models import Trip

print("Initializing SQLite database...")

init_db()

print("Database initialized successfully!")
print(f"Database location: {DATABASE_PATH}")
