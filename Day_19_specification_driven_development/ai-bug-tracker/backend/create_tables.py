
from app.database import Base, engine
from app.models import Bug

Base.metadata.create_all(bind=engine)

print("Database tables created successfully!")
print("Tables:", list(Base.metadata.tables.keys()))
