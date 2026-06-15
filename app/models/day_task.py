from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from datetime import date, datetime, time as time_type
from app.db.base import Base
from sqlalchemy import ForeignKey

class DayTask(Base):
    __tablename__ = "day_task"

    id: Mapped[int] = mapped_column(primary_key=True)
    trip_id: Mapped[int] = mapped_column(ForeignKey("trips.id"))
    date: Mapped[date]
    start_time: Mapped[time_type | None] = mapped_column(default=None)
    title: Mapped[str]
    description: Mapped[str | None] = mapped_column(default=None)
    is_done: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)