from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.workout_session import WorkoutSession
from app.schemas.workout_session import WorkoutSessionCreate, WorkoutSessionResponse

router = APIRouter(prefix="/workout_sessions", tags=["workout_sessions"])


@router.get("/{session_id}", response_model=WorkoutSessionResponse)
def get_workout_session(session_id: int, db: Session = Depends(get_db)):
    session = db.query(WorkoutSession).filter(WorkoutSession.id == session_id).first()
    if session:
        return session
    return {"message": f"Workout session with id {session_id} not found."}

@router.post("/", response_model=WorkoutSessionResponse)
def create_workout_session(data: WorkoutSessionCreate, db: Session = Depends(get_db)):
    workout_session = WorkoutSession(
        user_id=data.user_id,
        routine_id=data.routine_id,
        performed_at=data.performed_at
    )
    db.add(workout_session)
    db.commit()
    db.refresh(workout_session)
    return workout_session

@router.delete("/{session_id}")
def delete_workout_session(session_id: int, db: Session = Depends(get_db)):
    session = db.query(WorkoutSession).filter(WorkoutSession.id == session_id).first()
    if session:
        db.delete(session)
        db.commit()
        return {"message": f"Workout session with id {session_id} deleted successfully."}
    return {"message": f"Workout session with id {session_id} not found."}

@router.put("/{session_id}", response_model=WorkoutSessionResponse)
def update_workout_session(session_id: int, data: WorkoutSessionCreate, db: Session = Depends(get_db)):
    session = db.query(WorkoutSession).filter(WorkoutSession.id == session_id).first()
    if session:
        session.user_id = data.user_id         # type: ignore
        session.routine_id = data.routine_id   # type: ignore
        session.performed_at = data.performed_at # type: ignore
        db.commit()
        db.refresh(session)
        return session
    return {"message": f"Workout session with id {session_id} not found."}