from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.bodyStats import BodyStats
from app.schemas.body_stats import BodyStatsCreate, BodyStatsResponse, BodyStatsUpdate


router = APIRouter(prefix="/body-stats", tags=["body-stats"])


@router.post("", response_model=BodyStatsResponse)
def create_body_stat(payload: BodyStatsCreate, db: Session = Depends(get_db)):
    stat = BodyStats(**payload.model_dump())
    db.add(stat)
    db.commit()
    db.refresh(stat)
    return stat


@router.get("/user/{user_id}", response_model=List[BodyStatsResponse])
def list_body_stats_by_user(
    user_id: int,
    db: Session = Depends(get_db),
    date_from: Optional[date] = Query(default=None),
    date_to: Optional[date] = Query(default=None),
):
    q = db.query(BodyStats).filter(BodyStats.user_id == user_id)

    if date_from:
        q = q.filter(BodyStats.measured_at >= date_from)
    if date_to:
        q = q.filter(BodyStats.measured_at <= date_to)

    return q.order_by(BodyStats.measured_at.asc()).all()


@router.get("/user/{user_id}/latest", response_model=Optional[BodyStatsResponse])
def get_latest_body_stat(user_id: int, db: Session = Depends(get_db)):
    return (
        db.query(BodyStats)
        .filter(BodyStats.user_id == user_id)
        .order_by(BodyStats.measured_at.desc(), BodyStats.id.desc())
        .first()
    )


@router.get("/{stat_id}", response_model=BodyStatsResponse)
def get_body_stat(stat_id: int, db: Session = Depends(get_db)):
    stat = db.query(BodyStats).filter(BodyStats.id == stat_id).first()
    if not stat:
        raise HTTPException(status_code=404, detail="Body stat not found.")
    return stat


@router.patch("/{stat_id}", response_model=BodyStatsResponse)
def update_body_stat(stat_id: int, payload: BodyStatsUpdate, db: Session = Depends(get_db)):
    stat = db.query(BodyStats).filter(BodyStats.id == stat_id).first()
    if not stat:
        raise HTTPException(status_code=404, detail="Body stat not found.")

    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(stat, k, v)

    db.commit()
    db.refresh(stat)
    return stat


@router.delete("/{stat_id}")
def delete_body_stat(stat_id: int, db: Session = Depends(get_db)):
    stat = db.query(BodyStats).filter(BodyStats.id == stat_id).first()
    if not stat:
        raise HTTPException(status_code=404, detail="Body stat not found.")

    db.delete(stat)
    db.commit()
    return {"message": "Body stat deleted."}
