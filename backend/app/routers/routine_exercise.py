from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.routine_exercise import RoutineExercise
from app.schemas.routine_exercise import RoutineExerciseCreate, RoutineExerciseResponse

router = APIRouter(prefix="/routineExercise", tags=["routineExercise"])

@router.get("/{routine_exercise_id}", response_model=RoutineExerciseResponse)
def get_routine_exercise(routine_exercise_id: int, db: Session = Depends(get_db)):
    routine_exercise = db.query(RoutineExercise).filter(RoutineExercise.id == routine_exercise_id).first()
    if routine_exercise:
        return routine_exercise
    return {"message": f"RoutineExercise with id {routine_exercise_id} not found."}

@router.post("/", response_model=RoutineExerciseResponse)
def create_routine_exercise(data: RoutineExerciseCreate, db: Session = Depends(get_db)):
    routine_exercise = RoutineExercise(
        routine_id=data.routine_id,
        exercise_id=data.exercise_id,
        position=data.position,
        target_sets=data.target_sets,
        target_reps=data.target_reps,
        target_weight=data.target_weight
    )
    db.add(routine_exercise)
    db.commit()
    db.refresh(routine_exercise)
    return routine_exercise

@router.delete("/{routine_exercise_id}")
def delete_routine_exercise(routine_exercise_id: int, db: Session = Depends(get_db)):
    routine_exercise = db.query(RoutineExercise).filter(RoutineExercise.id == routine_exercise_id).first()
    if routine_exercise:
        db.delete(routine_exercise)
        db.commit()
        return {"message": f"RoutineExercise with id {routine_exercise_id} deleted successfully."}
    return {"message": f"RoutineExercise with id {routine_exercise_id} not found."}

@router.put("/{routine_exercise_id}", response_model=RoutineExerciseResponse)
def update_routine_exercise(routine_exercise_id: int, data: RoutineExerciseCreate, db: Session = Depends(get_db)):
    routine_exercise = db.query(RoutineExercise).filter(RoutineExercise.id == routine_exercise_id).first()
    if routine_exercise:
        routine_exercise.routine_id = data.routine_id       # type: ignore
        routine_exercise.exercise_id = data.exercise_id     # type: ignore
        routine_exercise.position = data.position           # type: ignore
        routine_exercise.target_sets = data.target_sets     # type: ignore
        routine_exercise.target_reps = data.target_reps     # type: ignore
        routine_exercise.target_weight = data.target_weight # type: ignore
        db.commit()
        db.refresh(routine_exercise)
        return routine_exercise
    return {"message": f"RoutineExercise with id {routine_exercise_id} not found."}