import uuid
from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy import ForeignKey, Integer, String, Text, DateTime, Enum
from sqlalchemy.orm import Mapped, relationship, mapped_column

from database.database import ModelORM
from enam import Role


class UsersORM(SQLAlchemyBaseUserTableUUID, ModelORM):
    __tablename__ = "users"
    name: Mapped[str]
    surname: Mapped[str]
    role: Mapped[Role] = mapped_column(Enum(Role), default=Role.STUDENT)

    enrolled_courses: Mapped[list["CourseORM"]] = relationship(
        "CourseORM",
        secondary="course_participants",
        back_populates="participants",
    )

    def __repr__(self):
        return f"<Users {self.name} {self.surname} {self.role}>"


class CourseParticipantORM(ModelORM):
    __tablename__ = "course_participants"

    course_id: Mapped[int] = mapped_column(
        ForeignKey("courses.id"), primary_key=True, nullable=False
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"), primary_key=True, nullable=False
    )


class CourseORM(ModelORM):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    participants: Mapped[list[UsersORM]] = relationship(
        "UsersORM",
        secondary="course_participants",
        back_populates="enrolled_courses",
    )

    def __repr__(self):
        return f"<Course {self.title}; {self.created_at}>"
