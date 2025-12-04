from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.workout_set import WorkoutSet
from app.schemas.workout_set import workoutSetCreate, workoutSetResponse

router = APIRouter(prefix="/workout_sets", tags=["workout_sets"])

@router.get("/{workout_set_id}", response_model=workoutSetResponse)
def get_workout_set(workout_set_id: int, db: Session = Depends(get_db)):
    workout_set = db.query(WorkoutSet).filter(WorkoutSet.id == workout_set_id).first()
    if workout_set:
        return workout_set
    return {"message": f"WorkoutSet with id {workout_set_id} not found."}

@router.post("/", response_model=workoutSetResponse)
def create_workout_set(data: workoutSetCreate, db: Session = Depends(get_db)):
    workout_set = WorkoutSet(
        session_id=data.workout_id,
        exercise_id=data.exercise_id,
        set_number=data.set_number,
        reps=data.reps,
        weight=data.weight
    )
    db.add(workout_set)
    db.commit()
    db.refresh(workout_set)
    return workout_set

@router.delete("/{workout_set_id}")
def delete_workout_set(workout_set_id: int, db: Session = Depends(get_db)):
    workout_set = db.query(WorkoutSet).filter(WorkoutSet.id == workout_set_id).first()
    if workout_set:
        db.delete(workout_set)
        db.commit()
        return {"message": f"WorkoutSet with id {workout_set_id} deleted successfully."}
    return {"message": f"WorkoutSet with id {workout_set_id} not found."}

@router.put("/{workout_set_id}", response_model=workoutSetResponse)
def update_workout_set(workout_set_id: int, data: workoutSetCreate, db: Session = Depends(get_db)):
    workout_set = db.query(WorkoutSet).filter(WorkoutSet.id == workout_set_id).first()
    if workout_set:
        workout_set.session_id = data.workout_id  # type: ignore
        workout_set.exercise_id = data.exercise_id        # type: ignore
        workout_set.set_number = data.set_number          # type: ignore
        workout_set.reps = data.reps                      # type: ignore
        workout_set.weight = data.weight                  # type: ignore
        db.commit()
        db.refresh(workout_set)
        return workout_set
    return {"message": f"WorkoutSet with id {workout_set_id} not found."}