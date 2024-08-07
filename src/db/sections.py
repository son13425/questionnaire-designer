"""Работа с данными разделов анкеты."""
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.base import CRUDBase
from db.fields import fields_crud
from models.sections import Sections, Chapters
from schemas.sections import SectionCreate


class CRUDSections(CRUDBase):
    """
    Расширяет базовый набор CRUD-методов специальными для разделов анкеты.
    """

    async def get_all_chapter_id_by_uuid_anket(
        self,
        uuid_anket: str,
        session: AsyncSession
    ):
        """
        Возвращает из БД уникальные id всех родителей разделов
        для заданной анкеты.
        """
        db_chapters_id = await session.execute(
            select(self.model.chapters_id).where(
                self.model.ankets_uuid == uuid_anket
            )
        )
        return db_chapters_id.scalars().all()

    async def create_section(
        self,
        new_section: SectionCreate,
        session: AsyncSession
    ):
        """
        Создает в БД новую запись в таблице разделов sections.
        """
        # конвертируем объект SectionCreate в словарь
        new_section_data = new_section.dict(exclude_unset=True)
        print()
        print(new_section_data)
        print()
        # дополнить словарь uuid
        new_section_data['uuid'] = str(uuid.uuid4())
        # запрашиваем id родительского раздела по label,
        # если есть родитель
        if 'chapter' in new_section_data:
            db_chapters_id = await chapters_crud.get_id_by_attribute(
                'label',
                new_section_data['chapter'],
                session
            )
            if db_chapters_id is None:
                db_new_chapter = await chapters_crud.create(
                    {'label': new_section_data['chapter']},
                    session
                )
                new_section_data['chapters_id'] = db_new_chapter.id
            else:
                new_section_data['chapters_id'] = db_chapters_id
            new_section_data.pop('chapter')
        # запрашиваем uuid поля зависимости по label,
        # если есть поле зависимости
        if 'dependent' in new_section_data:
            db_field_uuid = await fields_crud.get_uuid_field_by_label(
                new_section_data['dependent'],
                session
            )
            new_section_data['dependent_field_uuid'] = db_field_uuid
            new_section_data.pop('dependent')
        # создаем объект модели Section
        db_section = self.model(**new_section_data)
        session.add(db_section)
        await session.commit()
        await session.refresh(db_section)
        return db_section


class CRUDChapters(CRUDBase):
    """
    Расширяет базовый набор CRUD-методов специальными
    для родителей разделов анкеты.
    """

    async def get_all_obj_chapters_by_anket(
        self,
        list_chapters_id: list[int],
        session: AsyncSession
    ):
        """
        Возвращает из БД список объектов родителей разделов по списку их id.
        """
        result = []
        for i in list_chapters_id:
            result_item = await chapters_crud.get(i, session)
            if result_item is None:
                continue
            result.append(result_item)
        return result


# объект для работы с таблицей Sections(10 методов CRUD)
sections_crud = CRUDSections(Sections)


# объект для работы с таблицей Chapters(9 методов CRUD)
chapters_crud = CRUDChapters(Chapters)
