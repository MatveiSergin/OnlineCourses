from typing import AsyncGenerator

import aiohttp
from starlette import status

from exceptoins import ServiceException
from settings.settings import settings


class FileService:
    URL = settings.FILE_SERVICE_URL

    async def stream_content(self, course_id: int, page: int) -> AsyncGenerator[bytes, None]:
        params = {"course_id": course_id, "page": page}
        async with aiohttp.ClientSession() as session:
            async with session.get(self.URL, params=params) as response:
                if response.status != status.HTTP_200_OK:
                    raise ServiceException(f"Ошибка получения файла: {response.status}")
                async for chunk in response.content.iter_chunked(1024):
                    yield chunk
