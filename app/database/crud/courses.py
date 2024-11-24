import uuid
from datetime import datetime

from sqlalchemy import delete, update, select
from typing import Sequence
from sqlalchemy.orm import joinedload

from database.crud.common import CommonCRUD
from database.models import CourseORM, CourseParticipantORM, UsersORM


class CoursesCRUD(CommonCRUD):
    async def create_course(
        self, title: str, description: str | None, created_at: datetime | None = None
    ) -> CourseORM:
        """Создает новый курс."""
        created_at = created_at or datetime.utcnow()
        new_course = CourseORM(
            title=title, description=description, created_at=created_at
        )
        self.session.add(new_course)
        await self.session.commit()
        await self.session.refresh(new_course)
        return new_course

    async def get_course(self, course_id: int) -> CourseORM | None:
        """Возвращает курс по ID."""
        result = await self.session.execute(
            select(CourseORM)
            .options(joinedload(CourseORM.participants))
            .where(CourseORM.id == course_id)
        )
        return result.scalars().first()

    async def get_all_courses(self) -> Sequence[CourseORM]:
        """Возвращает список всех курсов."""
        result = await self.session.execute(select(CourseORM))
        return result.scalars().all()

    async def update_course(
        self, course_id: int, title: str | None = None, description: str | None = None
    ) -> CourseORM | None:
        """Обновляет информацию о курсе."""
        values_to_update = {}
        if title:
            values_to_update["title"] = title
        if description:
            values_to_update["description"] = description

        if values_to_update:
            await self.session.execute(
                update(CourseORM)
                .where(CourseORM.id == course_id)
                .values(**values_to_update)
            )
            await self.session.commit()

        return await self.get_course(course_id)

    async def delete_course(self, course_id: int) -> None:
        """Удаляет курс."""
        await self.session.execute(delete(CourseORM).where(CourseORM.id == course_id))
        await self.session.commit()

    async def add_participant(self, course_id: int, user_id: uuid.UUID) -> None:
        """Добавляет участника в курс."""
        participant = CourseParticipantORM(course_id=course_id, user_id=user_id)
        self.session.add(participant)
        await self.session.commit()

    async def remove_participant(self, course_id: int, user_id: uuid.UUID) -> None:
        """Удаляет участника из курса."""
        await self.session.execute(
            delete(CourseParticipantORM).where(
                CourseParticipantORM.course_id == course_id,
                CourseParticipantORM.user_id == user_id,
            )
        )
        await self.session.commit()

    async def get_participants(self, course_id: int) -> list[UsersORM]:
        """Возвращает список участников курса."""
        course = await self.get_course(course_id)
        return course.participants if course else []

    async def check_participant(self, course_id: int, user_id: uuid) -> bool:
        result = await self.session.execute(
            select(CourseParticipantORM).where(
                CourseParticipantORM.course_id == course_id,
                CourseParticipantORM.user_id == user_id,
            )
        )

        return True if result.scalar_one_or_none() is not None else False

