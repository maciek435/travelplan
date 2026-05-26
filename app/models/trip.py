from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from datetime import date, datetime
from app.db.base import Base
from sqlalchemy import ForeignKey

class Trip(Base):
    __tablename__ = "trips"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    destination: Mapped[str]
    start_date: Mapped[date]
    end_date: Mapped[date]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
