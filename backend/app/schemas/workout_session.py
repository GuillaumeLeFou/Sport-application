from datetime import datetime
from pydantic import BaseModel

class WorkoutSessionCreate(BaseModel):
    user_id: int
    routine_id: int
    performed_at: datetime    # ISO formatted date string

class WorkoutSessionResponse(BaseModel):
    id: int
    user_id: int
    routine_id: int
    performed_at: datetime    # ISO formatted date string

    class Config:
        from_attributes = True