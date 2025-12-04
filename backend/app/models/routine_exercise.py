from sqlalchemy import Column, Integer, Float, String
from app.database import Base

class RoutineExercise(Base):
  __tablename__ = "RoutineExercise"

  id = Column(Integer, primary_key=True, index=True)
  routine_id = Column(Integer, index=True)
  exercise_id = Column(Integer, index=True)
  position = Column(Integer)
  target_sets = Column(Integer)
  target_reps = Column(Integer)
  target_weight = Column(Float)