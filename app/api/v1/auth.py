from fastapi import APIRouter, Depends
from app.schemas.user import UserCreate, UserResponse
from app.core.security import hash_password
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import get_db

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    new_user = User(
        name = user.name,
        email = user.email,
        hashed_password = hash_password(user.password)
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

    
    
