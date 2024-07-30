"""Роутеры для анкет."""
from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from core.user import current_user
from db.ankets import (create_anket, create_group, get_all_obj_ankets,
                       get_all_obj_ankets_same_group, list_groups_with_ankets,
                       get_anket_by_uuid, get_label_group_by_id, update_anket)
from db.db import get_session
from db.references import get_all_obj_from_reference
from models import User, Groups
from schemas.ankets import (AnketCreate, AnketDB, Ankets,
                            GroupBase, GroupCreate, GroupDB,
                            GroupsAnketsDB, AnketResponse,
                            AnketUpdate)


router = APIRouter()


@router.post(
    '/ankets/',
    response_model=list[GroupsAnketsDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)]
)
async def create_new_anket(
    anket: AnketCreate,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(current_user)
):
    """Создает новую Анкету в таблице ankets."""
    new_anket = await create_anket(
        anket,
        session,
        user
    )
    if new_anket is None:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Не удалось создть анкету'
        )
    list_ankets = await list_groups_with_ankets(session)
    if list_ankets is None:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='В базе данных нет анкет'
        )
    return list_ankets


@router.post(
    '/groups/',
    response_model=GroupDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)]
)
async def create_new_group(
    group: GroupCreate,
    session: AsyncSession = Depends(get_session)
):
    """Создает новую Группу анкет в таблице groups."""
    new_group = await create_group(
        group.label,
        session
    )
    return new_group


@router.get(
    '/ankets/',
    response_model=list[GroupsAnketsDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)]
)
async def get_all_ankets(
    session: AsyncSession = Depends(get_session)
):
    """Возвращает список всех анкет с разбивкой на группы."""
    all_ankets = await list_groups_with_ankets(session)
    if all_ankets is None:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='В базе данных нет анкет'
        )
    return all_ankets


@router.get(
    '/ankets/{uuid_anket}',
    response_model=AnketResponse,
    response_model_exclude_none=True
)
async def get_anket(
    uuid_anket: str,
    session: AsyncSession = Depends(get_session)
):
    """Возвращает объект анкеты по uuid."""
    obj_anket = await get_anket_by_uuid(
        uuid_anket,
        session
    )
    if obj_anket is None:
        raise HTTPException(
            status_code=404,
            detail='Группа не найдена'
        )
    group_label = await get_label_group_by_id(
        obj_anket.groups_id,
        session
    )
    anket_dict = jsonable_encoder(obj_anket)
    anket_dict['group'] = group_label
    return anket_dict


@router.patch(
    '/ankets/{uuid_anket}',
    response_model=list[GroupsAnketsDB],
    response_model_exclude_none=True
)
async def partially_update_anket(
    uuid_anket: str,
    anket_in: AnketUpdate,
    session: AsyncSession = Depends(get_session)
):
    """Обновляет объект анкеты в БД"""
    db_anket = await get_anket_by_uuid(uuid_anket, session)
    if db_anket is None:
        raise HTTPException(
            status_code=404,
            detail='Анкета не найдена'
        )
    new_anket = await update_anket(db_anket, anket_in, session)
    if new_anket is None:
        raise HTTPException(
            status_code=404,
            detail='Анкета не найдена'
        )
    list_ankets = await list_groups_with_ankets(session)
    if list_ankets is None:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='В базе данных нет анкет'
        )
    return list_ankets


@router.get(
    '/groups/',
    response_model=list[GroupDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)]
)
async def get_all_groups(
    session: AsyncSession = Depends(get_session)
):
    """Возвращает список всех групп анкет."""
    all_groups = await get_all_obj_from_reference(
        Groups,
        session
    )
    if all_groups is None:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='В базе данных нет групп анкет'
        )
    return all_groups
