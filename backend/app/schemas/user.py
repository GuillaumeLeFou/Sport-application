from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    firstname: str
    lastname: str
    age: int
    weight: float
    height: float


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    firstname: str
    lastname: str
    age: int
    weight: float
    height: float

    class Config:
        from_attributes = True
