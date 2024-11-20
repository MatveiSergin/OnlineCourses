from pydantic import BaseModel
from datetime import datetime


class CourseCreate(BaseModel):
    title: str
    description: str | None


class CourseUpdate(BaseModel):
    title: str | None
    description: str | None


class CourseOut(BaseModel):
    id: int
    title: str
    description: str | None
    created_at: datetime
