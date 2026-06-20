from fastapi import APIRouter, Depends, HTTPException
from app.schemas.day_task import DayTaskCreate, DayTaskResponse
from app.models.day_task import DayTask
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import get_db
from app.core.deps import get_current_user
from app.models.user import User
from sqlalchemy import select
from app.models.trip import Trip
from pydantic import BaseModel

router = APIRouter()

class OrderUpdate(BaseModel):
    task_ids: list[int]

@router.post("/", response_model=DayTaskResponse)
async def create_day_task(day_task: DayTaskCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):

    trip = await db.get(Trip, day_task.trip_id)
    if trip is None or trip.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Brak dostępu")
    
    new_day_task = DayTask(
        trip_id = day_task.trip_id,
        date = day_task.date,
        start_time = day_task.start_time,
        title = day_task.title,
        description = day_task.description,
        lat = day_task.lat,
        lng = day_task.lng,
        location_name = day_task.location_name,   
    )

    db.add(new_day_task)
    await db.commit()
    await db.refresh(new_day_task)
    return new_day_task

@router.get("/{trip_id}", response_model=list[DayTaskResponse])
async def get_day_task(trip_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(DayTask).where(DayTask.trip_id == trip_id))
    day_tasks = result.scalars().all()
    return day_tasks

@router.put("/{id}", response_model=DayTaskResponse)
async def update_day_task(id: int, day_task_data: DayTaskCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    
    trip = await db.get(Trip, day_task_data.trip_id)
    if trip is None or trip.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Brak dostępu")
    
    result = await db.execute(select(DayTask).where(DayTask.id == id))
    day_task = result.scalar_one_or_none()
    if day_task is None:
        raise HTTPException(status_code=404, detail="Nie znaleziono tasków")
    
    day_task.date = day_task_data.date
    day_task.title = day_task_data.title
    day_task.start_time = day_task_data.start_time
    day_task.description = day_task_data.description
    day_task.lat = day_task_data.lat
    day_task.lng = day_task_data.lng
    day_task.location_name = day_task_data.location_name  
    
    await db.commit()
    await db.refresh(day_task)
    
    return day_task

@router.delete("/{id}")
async def delete_day_task(id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(DayTask).where(DayTask.id == id))
    day_task = result.scalar_one_or_none()
    if day_task is None:
        raise HTTPException(status_code=404, detail="Nie znaleziono taska")

    await db.delete(day_task)
    await db.commit()

    return {"message": "task usunięty"}

@router.put("/reorder/{trip_id}")
async def reorder_task(trip_id: int, order: OrderUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    for index, task_id in enumerate(order.task_ids):
        result = await db.execute(select(DayTask).where(DayTask.id == task_id))
        task = result.scalar_one_or_none()
        if task:
            task.order = index
    await db.commit()
    return {"message": "kolejność zaktualizowana"}