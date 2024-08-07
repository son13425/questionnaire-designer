"""Роутеры для разделов анкет."""
from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from core.user import current_user
from db.sections import sections_crud, chapters_crud
from db.db import get_session
from models import Sections
from schemas.sections import (Sections, SectionsResponse,
                              Chapters, ChaptersResponse,
                              SectionCreate)


router = APIRouter()


@router.get(
    '/sections/chapters/{uuid_anket}',
    response_model=Optional[list[Chapters]],
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)]
)
async def get_all_chapters_by_anket(
    uuid_anket: str,
    session: AsyncSession = Depends(get_session)
):
    """Возвращает список всех объектов Родителей разделов анкеты."""
    all_chapters = await sections_crud.get_all_chapter_id_by_uuid_anket(
        uuid_anket,
        session
    )
    if all_chapters is None:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Родительские разделы не найдены'
        )
    print()
    print()
    print(all_chapters)
    print()
    print()
    all_chapters_set = set(all_chapters)
    all_obj_chapters = chapters_crud.get_all_obj_chapters_by_anket(
        all_chapters_set,
        session
    )
    return all_obj_chapters


@router.get(
    '/sections/{uuid_anket}',
    response_model=list[Optional[Sections]],
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)]
)
async def get_all_sections_by_anket(
    uuid_anket: str,
    session: AsyncSession = Depends(get_session)
):
    """Возвращает список всех объектов разделов для заданной анкеты."""
    all_sections = await sections_crud.get_all_objs_by_attr(
        'ankets_uuid',
        uuid_anket,
        session
    )
    print()
    print()
    print(all_sections)
    print()
    print()
    return all_sections


@router.post(
    '/sections/',
    response_model=SectionsResponse,
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)]
)
async def create_new_section(
    new_section: SectionCreate,
    session: AsyncSession = Depends(get_session),
):
    """Создает новый Раздел в таблице sections."""
    new_section = await sections_crud.create_section(
        new_section,
        session
    )
    if new_section is None:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Не удалось создть раздел'
        )
    return new_section
