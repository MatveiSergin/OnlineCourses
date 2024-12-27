from pydantic import BaseModel
from datetime import datetime


class CourseCreate(BaseModel):
    title: str
    description: str | None


class CourseUpdate(CourseCreate):
    title: str | None


class CourseOut(CourseCreate):
    id: int
    created_at: datetime
