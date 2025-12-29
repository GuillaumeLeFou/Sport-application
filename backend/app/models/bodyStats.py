from sqlalchemy import Column, Integer, Float, Date, DateTime, String, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class BodyStats(Base):
    __tablename__ = "body_stats"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("User.id"), nullable=False)

    measured_at = Column(Date, nullable=False)
    body_weight = Column(Float, nullable=False)
    body_weight_goal = Column(Float, nullable=True)
    body_fat_percentage = Column(Float, nullable=True)

    notes = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
