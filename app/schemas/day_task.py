from pydantic import BaseModel
from datetime import date, datetime

class DayTaskCreate(BaseModel):
    title: str
    description: str | None
    date: date
    trip_id: int

class DayTaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    date: date
    created_at: datetime | None
    trip_id: int

    model_config = {"from_attributes": True}