from pydantic import BaseModel

class RoutineCreate(BaseModel):
    user_id: int
    name: str
    description: str
  
class RoutineResponse(BaseModel):
    id: int
    user_id: int
    name: str
    description: str

    class Config:
        from_attributes = True