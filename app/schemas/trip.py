from pydantic import BaseModel
from datetime import date, datetime

class TripCreate(BaseModel):
    title: str
    destination: str
    start_date: date
    end_date: date

class TripResponse(BaseModel):
    id: int
    title: str
    destination: str
    start_date: date
    end_date: date
    created_at: datetime | None
    owner_id: int

    model_config = {"from_attributes": True}