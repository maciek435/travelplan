# Entry point aplikacji TravelPlan API
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from app.api.v1.auth import router as auth_router
from app.api.v1.trips import router as trips_router
from app.api.v1.day_tasks import router as day_tasks

app = FastAPI()
app.include_router(auth_router, prefix='/auth', tags=["auth"])
app.include_router(trips_router, prefix='/trips', tags=["trips"])
app.include_router(day_tasks, prefix='/day-tasks', tags=["day-tasks"])

@app.get('/health')
def root():
    return {"status": "ok"}
