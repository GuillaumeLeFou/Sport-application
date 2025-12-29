from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class BodyStatsBase(BaseModel):
    user_id: int
    measured_at: date
    body_weight: float = Field(gt=0)
    body_weight_goal: Optional[float] = Field(default=None, gt=0)
    body_fat_percentage: Optional[float] = Field(default=None, ge=0, le=100)
    notes: Optional[str] = None


class BodyStatsCreate(BodyStatsBase):
    pass


class BodyStatsUpdate(BaseModel):
    measured_at: Optional[date] = None
    body_weight: Optional[float] = Field(default=None, gt=0)
    body_weight_goal: Optional[float] = Field(default=None, gt=0)
    body_fat_percentage: Optional[float] = Field(default=None, ge=0, le=100)
    notes: Optional[str] = None


class BodyStatsResponse(BodyStatsBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
