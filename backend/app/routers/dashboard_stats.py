from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.dashboardStats import DashboardStats
from app.schemas.dashboard_stats import DashboardStatsResponse, DashboardStatsUpsert


router = APIRouter(prefix="/dashboard-stats", tags=["dashboard-stats"])


@router.get("/user/{user_id}", response_model=List[DashboardStatsResponse])
def list_dashboard_stats(
    user_id: int,
    db: Session = Depends(get_db),
    period_type: Optional[str] = Query(default=None),  # "week"|"month"|"all"
):
    q = db.query(DashboardStats).filter(DashboardStats.user_id == user_id)
    if period_type:
        q = q.filter(DashboardStats.period_type == period_type)
    return q.order_by(DashboardStats.period_start.desc()).all()


@router.get("/user/{user_id}/current", response_model=Optional[DashboardStatsResponse])
def get_current_dashboard_stats(
    user_id: int,
    period_type: str = Query(...),   # required
    period_start: date = Query(...), # required
    period_end: date = Query(...),   # required
    db: Session = Depends(get_db),
):
    return (
        db.query(DashboardStats)
        .filter(
            DashboardStats.user_id == user_id,
            DashboardStats.period_type == period_type,
            DashboardStats.period_start == period_start,
            DashboardStats.period_end == period_end,
        )
        .first()
    )


@router.post("/upsert", response_model=DashboardStatsResponse)
def upsert_dashboard_stats(payload: DashboardStatsUpsert, db: Session = Depends(get_db)):
    existing = (
        db.query(DashboardStats)
        .filter(
            DashboardStats.user_id == payload.user_id,
            DashboardStats.period_type == payload.period_type,
            DashboardStats.period_start == payload.period_start,
            DashboardStats.period_end == payload.period_end,
        )
        .first()
    )

    data = payload.model_dump()

    if existing:
        for k, v in data.items():
            setattr(existing, k, v)
        db.commit()
        db.refresh(existing)
        return existing

    row = DashboardStats(**data)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@router.delete("/{dashboard_stat_id}")
def delete_dashboard_stat(dashboard_stat_id: int, db: Session = Depends(get_db)):
    row = db.query(DashboardStats).filter(DashboardStats.id == dashboard_stat_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Dashboard stat not found.")
    db.delete(row)
    db.commit()
    return {"message": "Dashboard stat deleted."}
