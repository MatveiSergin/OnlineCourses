from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from database.database import db_session


class CommonCRUD:
    """Класс CRUD для работы с приложениями и версиями в БД."""

    def __init__(self, session: AsyncSession | None = None):
        """
        Инициализация класса. Если сессия не передана, то сессия создается внутри класса.

        Args:
            session: сессия
        """
        if not session:
            self.session = db_session()
        else:
            self.session = session

    def __del__(self):
        """
        Деструктор класса.

        Закрывает сессию.
        """
        self.session.close()

    async def commit(self):
        """Сохраняет изменения в базе данных."""
        await self.session.commit()
