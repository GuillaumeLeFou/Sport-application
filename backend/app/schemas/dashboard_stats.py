from datetime import date, datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


PeriodType = Literal["week", "month", "all"]


class DashboardStatsBase(BaseModel):
    user_id: int
    period_type: PeriodType
    period_start: date
    period_end: date

    total_volume: float = Field(default=0, ge=0)
    total_sessions: int = Field(default=0, ge=0)
    current_streak: int = Field(default=0, ge=0)
    pr_count: int = Field(default=0, ge=0)

    key_exercise_id: Optional[int] = None
    key_exercise_1rm: Optional[float] = Field(default=None, ge=0)

    top_muscle_id: Optional[int] = None
    top_muscle_volume: Optional[float] = Field(default=None, ge=0)

    body_weight: Optional[float] = Field(default=None, gt=0)
    body_weight_delta: Optional[float] = None

    goal_value: Optional[float] = Field(default=None, ge=0)
    goal_current: Optional[float] = Field(default=None, ge=0)
    goal_progress_percent: Optional[float] = Field(default=None, ge=0, le=100)


class DashboardStatsUpsert(DashboardStatsBase):
    """
    Upsert payload: you send all fields for a given (user_id + period_type + period_start + period_end).
    """
    pass


class DashboardStatsResponse(DashboardStatsBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    updated_at: datetime
