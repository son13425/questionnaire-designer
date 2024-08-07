"""Работа с метаданными полей."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.base import CRUDBase
from models.fields import Fields


class CRUDFields(CRUDBase):
    """
    Расширяет базовый набор CRUD-методов специальными для полей анкеты.
    """

    async def get_uuid_field_by_label(
        self,
        label: str,
        session: AsyncSession
    ):
        """Возвращает из БД uuid поля по его label."""
        db_field_uuid = await session.execute(
            select(self.model.uuid).where(
                self.model.label == label
            )
        )
        return db_field_uuid.scalars().first()


# объект для работы с таблицей fields(8 методов CRUD)
fields_crud = CRUDFields(Fields)
