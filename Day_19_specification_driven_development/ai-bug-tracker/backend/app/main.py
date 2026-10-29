
from contextlib import asynccontextmanager
from datetime import date
from typing import Literal

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy import case, func, select
from sqlalchemy.orm import Session

from app.database import Base, SessionLocal, engine
from app.models import Bug


Priority = Literal["Critical", "High", "Medium", "Low"]
BugStatus = Literal["Open", "In Progress", "Resolved"]


class BugCreate(BaseModel):
    title: str = Field(min_length=1, max_length=150)
    description: str = Field(min_length=1, max_length=5000)
    category: str = Field(default="Other", max_length=100)
    priority: Priority = "Medium"
    assignee: str = Field(default="Unassigned", max_length=100)


class BugUpdate(BaseModel):
    status: BugStatus | None = None
    assignee: str | None = Field(default=None, max_length=100)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_initials(name: str) -> str:
    if not name or name == "Unassigned":
        return "U"

    parts = name.strip().split()
    return "".join(part[0] for part in parts[:2]).upper()


def serialize_bug(bug: Bug) -> dict:
    return {
        "id": bug.bug_key,
        "title": bug.title,
        "description": bug.description,
        "category": bug.category,
        "priority": bug.priority,
        "status": bug.status,
        "assignee": bug.assignee,
        "initials": bug.initials,
        "created_at": bug.created_at.strftime("%b %d, %Y"),
    }


def seed_sample_bugs(db: Session):
    existing_bug = db.scalar(select(Bug.id).limit(1))

    if existing_bug is not None:
        return

    samples = [
        {
            "bug_key": "BUG-1042",
            "title": "Login fails after password reset",
            "description": "Users cannot log in after resetting their password.",
            "category": "Authentication",
            "priority": "Critical",
            "status": "Open",
            "assignee": "A. Sharma",
            "created_at": date(2026, 10, 29),
        },
        {
            "bug_key": "BUG-1041",
            "title": "Dashboard charts not loading",
            "description": "Charts do not load on the dashboard.",
            "category": "Dashboard",
            "priority": "High",
            "status": "In Progress",
            "assignee": "R. Kumar",
            "created_at": date(2026, 10, 28),
        },
        {
            "bug_key": "BUG-1040",
            "title": "Incorrect date in export report",
            "description": "The exported report displays an incorrect date.",
            "category": "Reporting",
            "priority": "Medium",
            "status": "Open",
            "assignee": "P. Singh",
            "created_at": date(2026, 10, 28),
        },
        {
            "bug_key": "BUG-1039",
            "title": "Profile image upload timeout",
            "description": "Uploading a profile image times out.",
            "category": "User Profile",
            "priority": "Low",
            "status": "Resolved",
            "assignee": "A. Sharma",
            "created_at": date(2026, 10, 27),
        },
        {
            "bug_key": "BUG-1038",
            "title": "Search returns duplicate results",
            "description": "Search results contain duplicate entries.",
            "category": "Search",
            "priority": "High",
            "status": "In Progress",
            "assignee": "R. Kumar",
            "created_at": date(2026, 10, 26),
        },
    ]

    for sample in samples:
        sample["initials"] = get_initials(sample["assignee"])
        db.add(Bug(**sample))

    db.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        seed_sample_bugs(db)

    yield


app = FastAPI(
    title="BugPilot API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "BugPilot API is running"}


@app.get("/api/health")
def health():
    return {"status": "healthy"}


@app.get("/api/bugs/stats")
def get_bug_stats(db: Session = Depends(get_db)):
    result = db.execute(
        select(
            func.count(Bug.id).label("total_bugs"),
            func.count(
                case((Bug.status == "Open", 1))
            ).label("open_bugs"),
            func.count(
                case((Bug.status == "In Progress", 1))
            ).label("in_progress_bugs"),
            func.count(
                case((Bug.status == "Resolved", 1))
            ).label("resolved_bugs"),
        )
    ).one()

    return {
        "total_bugs": result.total_bugs,
        "open_bugs": result.open_bugs,
        "in_progress_bugs": result.in_progress_bugs,
        "resolved_bugs": result.resolved_bugs,
    }

@app.get("/api/bugs")
def list_bugs(db: Session = Depends(get_db)):
    bugs = db.scalars(
        select(Bug).order_by(Bug.id.desc())
    ).all()

    return [serialize_bug(bug) for bug in bugs]


@app.post("/api/bugs", status_code=201)
def create_bug(
    bug_data: BugCreate,
    db: Session = Depends(get_db),
):
    highest_number = db.scalar(
        select(Bug.id).order_by(Bug.id.desc()).limit(1)
    )

    # Generate a unique display key using the largest existing key.
    all_keys = db.scalars(select(Bug.bug_key)).all()
    numbers = [
        int(key.removeprefix("BUG-"))
        for key in all_keys
        if key.startswith("BUG-")
        and key.removeprefix("BUG-").isdigit()
    ]
    next_number = max(numbers, default=1037) + 1

    bug = Bug(
        bug_key=f"BUG-{next_number}",
        title=bug_data.title.strip(),
        description=bug_data.description.strip(),
        category=bug_data.category,
        priority=bug_data.priority,
        status="Open",
        assignee=bug_data.assignee,
        initials=get_initials(bug_data.assignee),
        created_at=date.today(),
    )

    db.add(bug)
    db.commit()
    db.refresh(bug)

    return serialize_bug(bug)


@app.put("/api/bugs/{bug_id}")
def update_bug(
    bug_id: str,
    updates: BugUpdate,
    db: Session = Depends(get_db),
):
    bug = db.scalar(
        select(Bug).where(Bug.bug_key == bug_id)
    )

    if bug is None:
        raise HTTPException(status_code=404, detail="Bug not found")

    update_data = updates.model_dump(exclude_unset=True)

    if "status" in update_data:
        if update_data["status"] is None:
            raise HTTPException(
                status_code=422,
                detail="Status cannot be null",
            )
        bug.status = update_data["status"]

    if "assignee" in update_data:
        if update_data["assignee"] is None:
            raise HTTPException(
                status_code=422,
                detail="Assignee cannot be null",
            )
        bug.assignee = update_data["assignee"]
        bug.initials = get_initials(bug.assignee)

    db.commit()
    db.refresh(bug)

    return serialize_bug(bug)
