from sqlalchemy import String, Integer, Column
from app.database import Base

class Muscle(Base):
    __tablename__ = "Muscle"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)