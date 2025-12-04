from sqlalchemy import Column, Integer, Float
from app.database import Base

class WorkoutSet(Base):
    __tablename__ = "WorkoutSet"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, index=True)
    exercise_id = Column(Integer, index=True)
    set_number = Column(Integer)
    reps = Column(Integer)
    weight = Column(Float)