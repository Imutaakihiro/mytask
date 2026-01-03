from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date

class TaskCreate(BaseModel):
    """タスク作成用モデル（id, created_at, updated_atは不要）"""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    quadrant: int = Field(..., ge=1, le=4)  # 1-4の範囲
    completed: bool = False
    due_date: Optional[date] = None

class Task(BaseModel):
    """タスクモデル（全フィールドを含む）"""
    id: int
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    quadrant: int = Field(..., ge=1, le=4)  # 1-4の範囲
    completed: bool = False
    due_date: Optional[date] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # ORMモード（SQLAlchemyなどと連携する場合）