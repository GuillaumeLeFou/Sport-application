from sqlalchemy import Column, Integer, DateTime
from app.database import Base

class WorkoutSession(Base):
    __tablename__ = "WorkoutSession"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    routine_id = Column(Integer, index=True)
    performed_at = Column(DateTime)