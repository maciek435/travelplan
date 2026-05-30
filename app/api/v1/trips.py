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

@router.get("/{id}", response_model=TripResponse)
async def get_trip(id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Trip).where(Trip.owner_id == current_user.id, Trip.id == id))
    trip = result.scalar_one_or_none()
    if trip is None:
        raise HTTPException(status_code=404, detail="Nie znaleziono podróży")
    return trip

@router.put("/{id}", response_model=TripResponse)
async def update_trip(id: int, trip_data: TripCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Trip).where(Trip.owner_id == current_user.id, Trip.id == id))
    trip = result.scalar_one_or_none()
    if trip is None:
        raise HTTPException(status_code=404, detail="Nie znaleziono podróży")
    
    trip.title = trip_data.title
    trip.destination = trip_data.destination
    trip.start_date = trip_data.start_date
    trip.end_date = trip_data.end_date

    await db.commit()
    await db.refresh(trip)
    
    return trip

@router.delete("/{id}")
async def delete_trip(id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Trip).where(Trip.owner_id == current_user.id, Trip.id == id))
    trip = result.scalar_one_or_none()
    if trip is None:
        raise HTTPException(status_code=404, detail="Nie znaleziono podróży")
    
    await db.delete(trip)
    await db.commit()

    return {"messsage": "podróż usunięta"}