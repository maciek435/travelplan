from fastapi import APIRouter, Depends, HTTPException
from app.schemas.trip import TripCreate, TripResponse
from app.models.trip import Trip
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import get_db
from app.core.deps import get_current_user
from app.models.user import User
from sqlalchemy import select

router = APIRouter()

@router.post("/", response_model=TripResponse)
async def create_trip(trip: TripCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_trip = Trip(
        title = trip.title,
        destination = trip.destination,
        start_date = trip.start_date,
        end_date = trip.end_date,
        owner_id = current_user.id
    )

    db.add(new_trip)
    await db.commit()
    await db.refresh(new_trip)
    return new_trip

@router.get("/", response_model=list[TripResponse])
async def get_users_trips(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Trip).where(Trip.owner_id == current_user.id))
    trips = result.scalars().all()
    return trips


   