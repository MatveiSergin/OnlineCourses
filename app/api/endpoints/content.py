from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from starlette.responses import Response, StreamingResponse

from api.permissions import check_student_or_admin
from database.models import UsersORM
from services.courses import CoursesService
from services.file_service import FileService
from user import current_user

content_router = APIRouter(prefix="/content", tags=["Content"])

@content_router.get(
    "/{course_id}/content",
    status_code=status.HTTP_200_OK,
    summary="Получить контент курса",
    dependencies=[Depends(check_student_or_admin)],
)
async def get_content(course_id: int, page: int, user: UsersORM = Depends(current_user)):
    if await CoursesService().check_participant(course_id, user.id):
        return StreamingResponse(
            FileService().stream_content(course_id, page),
            media_type="application/octet-stream",
        )

    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Ошибка при получении контента курса"
    )