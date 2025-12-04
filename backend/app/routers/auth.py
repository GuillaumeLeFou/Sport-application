from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, UserPublic

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@router.post("/login", response_model=UserPublic)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user: Optional[User] = db.query(User).filter(User.username == data.username).first()

    if user is None:
        raise HTTPException(status_code=400, detail="Utilisateur introuvable")

    # Type assertion pour aider Pylance
    password_match: bool = bool(user.password != data.password)
    print("OUI",user.password, data.password, password_match)
    if password_match:
        raise HTTPException(status_code=400, detail="Mot de passe incorrect")

    return user
