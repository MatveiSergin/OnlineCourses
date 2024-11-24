import aiohttp
from starlette import status

from exceptoins import ServiceException
from settings.settings import settings


class FileService:

    URL = settings.FILE_SERVICE_URL

    def __init__(self):
        ...

    async def get_content(self, course_id: int, page: int) -> bytes:
        params = {"course_id": course_id, "page": page}
        async with aiohttp.ClientSession() as session:
            async with session.get(self.URL, params=params) as response:
                if response.status != status.HTTP_200_OK:
                    raise ServiceException(f"Ошибка получения файла: {response.status}")
                return await response.read()