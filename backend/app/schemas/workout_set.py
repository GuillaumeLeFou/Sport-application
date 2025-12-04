from pydantic import BaseModel

class workoutSetCreate(BaseModel):
    workout_id: int
    exercise_id: int
    set_number: int
    reps: int
    weight: float

class workoutSetResponse(BaseModel):
    id: int
    session_id: int
    exercise_id: int
    set_number: int
    reps: int
    weight: float

    class Config:
        from_attributes = True