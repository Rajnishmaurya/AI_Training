
from datetime import date, datetime
from pydantic import BaseModel, Field, ConfigDict, model_validator
from typing import Literal


class TripCreate(BaseModel):
    """Schema for creating a new employee trip."""

    employee_id: str = Field(
        min_length=1,
        max_length=50
    )

    destination: str = Field(
        min_length=2,
        max_length=150
    )

    start_date: date

    end_date: date

    purpose: str = Field(
        min_length=3,
        max_length=255
    )

    @model_validator(mode="after")
    def validate_travel_dates(self):
        if self.start_date < date.today():
            raise ValueError("Travel start date cannot be in the past")

        if self.end_date < self.start_date:
            raise ValueError(
                "End date cannot be earlier than start date"
            )

        return self


class TripResponse(BaseModel):
    """Schema for returning saved trip information."""

    model_config = ConfigDict(from_attributes=True)

    trip_id: str
    employee_id: str
    destination: str
    start_date: date
    end_date: date
    purpose: str
    status: str
    created_at: datetime


class TripLookup(BaseModel):
    """Schema for trip lookup."""

    trip_id: str



class AssistantRequest(BaseModel):
    session_id: str = Field(min_length=1, max_length=100)
    question: str = Field(min_length=2, max_length=1000)
    trip_id: str | None = None


class AssistantResponse(BaseModel):
    success: bool
    session_id: str
    trip_id: str | None = None
    destination: str | None = None
    weather_available: bool = False
    answer: str | None = None
    error: str | None = None
