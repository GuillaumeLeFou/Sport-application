from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.routine import Routine
from app.schemas.routine import RoutineCreate, RoutineResponse

router = APIRouter(prefix="/routines", tags=["routines"])

@router.get("/user/{user_id}")
def get_routine_by_user(user_id: int, db: Session = Depends(get_db)):
    routine = db.query(Routine).filter(Routine.user_id == user_id).all()
    return routine

@router.get("/id/{routine_id}")
def get_routine(routine_id: int, db: Session = Depends(get_db)):
    routine = db.query(Routine).filter(Routine.id == routine_id).first()
    if routine:
        return routine
    return {"message": f"Routine with id {routine_id} not found."}

@router.post("/", response_model=RoutineResponse)
def create_routine(data: RoutineCreate, db: Session = Depends(get_db)):
    routine = Routine(
        user_id=data.user_id,
        name=data.name,
        description=data.description
    )
    db.add(routine)
    db.commit()
    db.refresh(routine)
    return routine

@router.delete("/{routine_id}")
def delete_routine(routine_id: int, db: Session = Depends(get_db)):
    routine = db.query(Routine).filter(Routine.id == routine_id).first()
    if routine:
        db.delete(routine)
        db.commit()
        return {"message": f"Routine with id {routine_id} deleted successfully."}
    return {"message": f"Routine with id {routine_id} not found."}


@router.put("/{routine_id}", response_model=RoutineResponse)
def update_routine(routine_id: int, data: RoutineCreate, db: Session = Depends(get_db)):
    routine = db.query(Routine).filter(Routine.id == routine_id).first()
    if routine:
        routine.user_id = data.user_id          # type: ignore
        routine.name = data.name                # type: ignore
        routine.description = data.description  # type: ignore
        db.commit()
        db.refresh(routine)
        return routine
    return {"message": f"Routine with id {routine_id} not found."}