from sqlalchemy import Column, Integer, Float, Date, DateTime, String, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class DashboardStats(Base):
    __tablename__ = "dashboard_stats"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("User.id"), nullable=False)

    period_type = Column(String, nullable=False)   # "week" | "month" | "all"
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)

    total_volume = Column(Float, default=0)
    total_sessions = Column(Integer, default=0)
    current_streak = Column(Integer, default=0)
    pr_count = Column(Integer, default=0)

    key_exercise_id = Column(Integer, ForeignKey("Exercise.id"), nullable=True)
    key_exercise_1rm = Column(Float, nullable=True)

    top_muscle_id = Column(Integer, ForeignKey("Muscle.id"), nullable=True)
    top_muscle_volume = Column(Float, nullable=True)

    body_weight = Column(Float, nullable=True)
    body_weight_delta = Column(Float, nullable=True)

    goal_value = Column(Float, nullable=True)
    goal_current = Column(Float, nullable=True)
    goal_progress_percent = Column(Float, nullable=True)

    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
