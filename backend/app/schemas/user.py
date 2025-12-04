from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    firstname: str
    lastname: str
    age: int
    weight: float
    height: float

class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    firstname: str
    lastname: str
    age: int
    weight: float
    height: float

    class Config:
        from_attributes = True
