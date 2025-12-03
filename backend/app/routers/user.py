from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        return user
    return {"message": f"User with id {user_id} not found."}


@router.post("/", response_model=UserResponse)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    user = User(
        username=data.username,
        email=data.email,
        password=data.password,
        firstname=data.firstname,
        lastname=data.lastname,
        age=data.age,
        weight=data.weight,
        height=data.height
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return {"message": f"User with id {user_id} deleted successfully."}
    return {"message": f"User with id {user_id} not found."}

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, data: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.email = data.email # type: ignore
        user.password = data.password # type: ignore
        user.firstname = data.firstname # type: ignore
        user.lastname = data.lastname # type: ignore
        user.age = data.age # type: ignore
        user.weight = data.weight # type: ignore
        user.height = data.height # type: ignore
        db.commit()
        db.refresh(user)
        return user
    return {"message": f"User with id {user_id} not found."}