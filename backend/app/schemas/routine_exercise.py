from pydantic import BaseModel

class RoutineExerciseCreate(BaseModel):
    routine_id: int
    exercise_id: int
    position: int
    target_sets: int
    target_reps: int
    target_weight: float

class RoutineExerciseResponse(BaseModel):
    id: int
    routine_id: int
    exercise_id: int
    position: int
    target_sets: int
    target_reps: int
    target_weight: float

    class Config:
        from_attributes = True