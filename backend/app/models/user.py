from sqlalchemy import Column, Float, Integer, String, Date
from app.database import Base

class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    birthday = Column(Date, nullable=False)
    weight = Column(Float)
    height = Column(Float)
