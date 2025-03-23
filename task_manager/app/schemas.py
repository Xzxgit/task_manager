from datetime import datetime
from pydantic import BaseModel, field_validator, ConfigDict


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    due_date: datetime | None = None
    priority: int = 2

    # priority 字段数据校验
    @field_validator('priority')
    def validate_priority(cls, v):
        if v not in [1, 2, 3]:
            raise ValueError('Priority must be 1, 2 or 3')
        return v


class TaskUpdate(TaskCreate):
    title: str = None
    description: str = None
    due_date: datetime = None
    priority: int = None
    update_date: datetime = datetime.now()


class TaskResponse(TaskCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )
