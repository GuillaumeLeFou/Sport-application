from sqlalchemy import Column, Float, Integer, String
from app.database import Base

class Routine(Base):
    __tablename__ = "Routine"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    name = Column(String, index=True)
    description = Column(String)