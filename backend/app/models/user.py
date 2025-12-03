from sqlalchemy import Column, Float, Integer, String
from app.database import Base

class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    password = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    age = Column(Integer)
    weight = Column(Float)
    height = Column(Float)