from sqlalchemy import Integer, Column
from app.database import Base

class ExerciseSecondaryMuscle(Base):
    __tablename__ = "ExerciseSecondaryMuscle"

    id = Column(Integer, primary_key=True, index=True)
    exercise_id = Column(Integer, index=True)
    muscle_id = Column(Integer, index=True)