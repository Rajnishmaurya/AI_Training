
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import (
    TripCreate,
    TripResponse,
    AssistantRequest,
    AssistantResponse,
)
from app.services.trip_service import create_trip, get_trip_by_id
from app.agent.travel_assistant import ask_travel_assistant

router = APIRouter()


@router.post("/trips", response_model=TripResponse, status_code=201)
def create_new_trip(
    trip_data: TripCreate,
    db: Session = Depends(get_db)
):
    try:
        return create_trip(db, trip_data)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to create trip: {str(exc)}"
        )


@router.get("/trips/{trip_id}", response_model=TripResponse)
def retrieve_trip(
    trip_id: str,
    db: Session = Depends(get_db)
):
    trip = get_trip_by_id(db, trip_id)

    if not trip:
        raise HTTPException(
            status_code=404,
            detail="Trip not found"
        )

    return trip


@router.post(
    "/assistant/ask",
    response_model=AssistantResponse
)
def ask_assistant(request: AssistantRequest):
    result = ask_travel_assistant(
        session_id=request.session_id,
        question=request.question,
        trip_id=request.trip_id
    )

    if not result.get("success"):
        raise HTTPException(
            status_code=400,
            detail=result.get("error", "Assistant request failed")
        )

    return result
