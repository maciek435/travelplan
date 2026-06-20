from pydantic import BaseModel
from datetime import date, datetime, time

class DayTaskCreate(BaseModel):
    title: str
    description: str | None
    start_time: time | None = None
    date: date
    trip_id: int
    order: int = 0
    lat: float | None = None
    lng: float | None = None
    location_name: str | None = None

class DayTaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    date: date
    start_time: time | None
    created_at: datetime | None
    trip_id: int
    order: int
    lat: float | None = None
    lng: float | None = None
    location_name: str | None = None

    model_config = {"from_attributes": True}