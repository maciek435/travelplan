from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import UserCreate, UserResponse, TokenResponse
from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import get_db
from sqlalchemy import select


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

@router.post("/login", response_model=TokenResponse)
async def login_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    email = user.email
    password = user.password

    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=401, detail="Nieprawidłowe dane")
        
    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Nieprawidłowe dane")
    
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}