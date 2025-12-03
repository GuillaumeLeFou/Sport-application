from sqlalchemy import String, Integer, Column
from app.database import Base

class Exercise(Base):
    __tablename__ = "Exercise"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    primary_muscle = Column(String, index=True)