from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str
    days: int = Field(default=30, ge=1, le=3650)
    traffic_limit_gb: int = Field(default=100, ge=1, le=100000)


class UserUpdate(BaseModel):
    enabled: Optional[bool] = None
    traffic_limit_gb: Optional[int] = Field(default=None, ge=1, le=100000)


class AlertOut(BaseModel):
    id: int
    level: str
    code: str
    title: str
    detail: str
    solutions: str
    created_at: datetime

    class Config:
        from_attributes = True
