import uuid

from database.crud.courses import CoursesCRUD
from exceptoins import ServiceException
from schemas.auth import UserOut
from schemas.courses import CourseCreate, CourseOut, CourseUpdate


class CoursesService:

    courses_crud = CoursesCRUD()

    async def create_course(self, course_data: CourseCreate) -> CourseOut:
        """Создает новый курс."""
        new_course = await self.courses_crud.create_course(
            title=course_data.title,
            description=course_data.description,
        )
        return CourseOut.model_validate(new_course, from_attributes=True)

    async def get_course(self, course_id: int) -> CourseOut | None:
        """Возвращает информацию о курсе по его ID."""
        course = await self.courses_crud.get_course(course_id)
        return (
            CourseOut.model_validate(course, from_attributes=True) if course else None
        )

    async def get_all_courses(self) -> list[CourseOut]:
        """Возвращает список всех курсов."""
        courses = await self.courses_crud.get_all_courses()
        return [
            CourseOut.model_validate(course, from_attributes=True) for course in courses
        ]

    async def update_course(
        self, course_id: int, course_data: CourseUpdate
    ) -> CourseOut | None:
        """Обновляет данные курса."""
        updated_course = await self.courses_crud.update_course(
            course_id=course_id,
            title=course_data.title,
            description=course_data.description,
        )
        return (
            CourseOut.model_validate(updated_course, from_attributes=True)
            if updated_course
            else None
        )

    async def delete_course(self, course_id: int) -> None:
        """Удаляет курс по его ID."""
        await self.courses_crud.delete_course(course_id)

    async def add_participant(self, course_id: int, user_id: uuid.UUID) -> None:
        """Добавляет участника в курс."""
        await self.courses_crud.add_participant(course_id, user_id)

    async def remove_participant(self, course_id: int, user_id: uuid.UUID) -> None:
        """Удаляет участника из курса."""
        await self.courses_crud.remove_participant(course_id, user_id)

    async def get_participants(self, course_id: int) -> list[UserOut]:
        """Возвращает список участников курса."""
        participants = await self.courses_crud.get_participants(course_id)
        return [
            UserOut.model_validate(participant, from_attributes=True)
            for participant in participants
        ]
