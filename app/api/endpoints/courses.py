import uuid

from fastapi import APIRouter, HTTPException, status, Depends

from api.permissions import check_admin, check_student_or_admin
from schemas.auth import UserOut
from schemas.courses import CourseOut, CourseUpdate, CourseCreate
from services.courses import CoursesService

courses_router = APIRouter(prefix="/courses", tags=["Courses"])


@courses_router.post(
    "/",
    response_model=CourseOut,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новый курс",
    dependencies=[Depends(check_admin)],
)
async def create_course(course_data: CourseCreate):
    """Создать новый курс."""
    return await CoursesService().create_course(course_data)


@courses_router.get(
    "/{course_id}",
    response_model=CourseOut,
    status_code=status.HTTP_200_OK,
    summary="Получить курс по ID",
    dependencies=[Depends(check_student_or_admin)],
)
async def get_course(course_id: int):
    """Получить курс по ID."""
    course = await CoursesService().get_course(course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Курс {course_id} не найден."
        )
    return course


@courses_router.get(
    "/",
    response_model=list[CourseOut],
    status_code=status.HTTP_200_OK,
    summary="Получить список всех курсов",
    dependencies=[Depends(check_student_or_admin)],
)
async def get_all_courses():
    """Получить список всех курсов."""
    return await CoursesService().get_all_courses()


@courses_router.put(
    "/{course_id}",
    response_model=CourseOut,
    status_code=status.HTTP_200_OK,
    summary="Обновить информацию о курсе",
    dependencies=[Depends(check_admin)],
)
async def update_course(course_id: int, course_data: CourseUpdate):
    """Обновить информацию о курсе."""
    updated_course = await CoursesService().update_course(course_id, course_data)
    if not updated_course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Курс {course_id} не найден."
        )
    return updated_course


@courses_router.delete(
    "/{course_id}",
    status_code=status.HTTP_200_OK,
    summary="Удалить курс",
    dependencies=[Depends(check_admin)],
)
async def delete_course(course_id: int):
    """Удалить курс."""
    await CoursesService().delete_course(course_id)


@courses_router.post(
    "/{course_id}/participants/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Добавить участника в курс",
    dependencies=[Depends(check_admin)],
)
async def add_participant(course_id: int, user_id: uuid.UUID):
    """Добавить участника в курс."""
    await CoursesService().add_participant(course_id, user_id)


@courses_router.delete(
    "/{course_id}/participants/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Удалить участника из курса",
    dependencies=[Depends(check_admin)],
)
async def remove_participant(course_id: int, user_id: uuid.UUID):
    """Удалить участника из курса."""
    await CoursesService().remove_participant(course_id, user_id)


@courses_router.get(
    "/{course_id}/participants",
    response_model=list[UserOut],
    status_code=status.HTTP_200_OK,
    summary="Получить список участников курса",
    dependencies=[Depends(check_admin)],
)
async def get_participants(course_id: int):
    """Получить список участников курса."""
    participants = await CoursesService().get_participants(course_id)
    return participants

