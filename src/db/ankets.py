"""Работа с метаданными анкеты."""
import datetime
import uuid
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from models import Ankets, Groups, User
from schemas.ankets import (AnketCreate,
                            AnketUpdate,
                            GroupsAnketsDB)


# Создание объектов в таблице Ankets
async def create_anket(
    new_anket: AnketCreate,
    session: AsyncSession,
    user: User
) -> Ankets:
    """Записывает объект Анкета в таблицу ankets."""
    # конвертируем объект AnketCreate в словарь
    new_anket_data = new_anket.dict()
    # дополнить словарь uuid
    new_anket_data['uuid'] = str(uuid.uuid4())
    # дополнить словарь данными юзера
    new_anket_data['autor_id'] = user.id
    # дополнить словарь меткой времени
    new_anket_data['timestamp'] = datetime.datetime.now()
    # запрашиваем id группы по label
    db_group_id = await get_id_by_field(
        new_anket_data['group'],
        session
    )
    if db_group_id is None:
        db_new_group = await create_group(
            new_anket_data['group'],
            session
        )
        new_anket_data['groups_id'] = db_new_group.id
    else:
        new_anket_data['groups_id'] = db_group_id
    new_anket_data.pop('group')
    # создаем объект модели Ankets
    db_anket = Ankets(**new_anket_data)
    # записываем объект в базу
    session.add(db_anket)
    await session.commit()
    await session.refresh(db_anket)
    # возвращаем обновленный объект из базы
    return db_anket


# Создание объектов в таблице Groups
async def create_group(
    new_group: str,
    session: AsyncSession,
) -> Groups:
    """Записывает объект Group в таблицу groups."""
    # конвертируем объект GroupCreate в словарь
    new_group_data = {'label': new_group}
    # создаем объект модели Groups
    db_group = Groups(**new_group_data)
    # записываем объект в базу
    session.add(db_group)
    await session.commit()
    await session.refresh(db_group)
    # возвращаем обновленный объект из базы
    return db_group


# чтение объектов всех групп
async def get_all_obj_groups(
    session: AsyncSession
) -> list[Groups]:
    """Возвращает список всех объектов групп."""
    db_groups = await session.execute(select(Groups))
    return db_groups.scalars().all()


# чтение объектов всех анкет
async def get_all_obj_ankets(
    session: AsyncSession
) -> list[Ankets]:
    """Возвращает список всех объектов анкет."""
    db_ankets = await session.execute(select(Ankets))
    return db_ankets.scalars().all()


# чтение объектов всех анкет из одной группы
async def get_all_obj_ankets_same_group(
    group_id: int,
    session: AsyncSession
) -> list[Ankets]:
    """
    Возвращает список всех объектов анкет,
    принадлежащих одной группе.
    """
    db_ankets = await session.execute(
        select(Ankets).where(
            Ankets.groups_id == group_id
        )
    )
    return db_ankets.scalars().all()


# возвращает список групп с анкетами, принадлежащими группе
async def list_groups_with_ankets(
    session: AsyncSession
) -> list[GroupsAnketsDB]:
    """
    Возвращает список групп и всех объектов анкет,
    принадлежащих каждой группе.
    """
    result_list = []
    all_groups = await get_all_obj_groups(session)
    for group in all_groups:
        all_ankets_group = await get_all_obj_ankets_same_group(
            group.id,
            session
        )
        result_list.append({'group': group, 'ankets': all_ankets_group})
    return result_list


# возвращает id объекта grup по значению поля label
async def get_id_by_field(
    group_label: str,
    session: AsyncSession
) -> Optional[int]:
    """Возвращает id объекта grup по значению поля label."""
    db_group_id = await session.execute(
        select(Groups.id).where(
            Groups.label == group_label
        )
    )
    group_id = db_group_id.scalars().first()
    return group_id


# возвращает название группы по id
async def get_label_group_by_id(
    group_id: int,
    session: AsyncSession
) -> Optional[str]:
    """Возвращает название группы по id."""
    db_group_label = await session.execute(
        select(Groups.label).where(
            Groups.id == group_id
        )
    )
    group_label = db_group_label.scalars().first()
    return group_label


# возвращает из БД объект анкеты по uuid
async def get_anket_by_uuid(
    uuid_anket: str,
    session: AsyncSession
) -> Optional[Ankets]:
    """Возвращает из БД объект анкеты по uuid."""
    db_anket = await session.execute(
        select(Ankets).where(
            Ankets.uuid == uuid_anket
        )
    )
    obj_anket = db_anket.scalars().first()
    return obj_anket


# обновляет объект анкеты
async def update_anket(
    db_anket: Ankets,
    anket_in: AnketUpdate,
    session: AsyncSession
) -> Ankets:
    """Обновляет объект анкеты."""
    obj_data = jsonable_encoder(db_anket)
    update_data = anket_in.dict(exclude_unset=True)
    if 'group' in update_data:
        db_group_id = await get_id_by_field(
            update_data['group'],
            session
        )
        if db_group_id is None:
            db_new_group = await create_group(
                update_data['group'],
                session
            )
            update_data['groups_id'] = db_new_group.id
        else:
            update_data['groups_id'] = db_group_id
    for field in obj_data:
        if field in update_data:
            setattr(db_anket, field, update_data[field])
    session.add(db_anket)
    await session.commit()
    await session.refresh(db_anket)
    return db_anket
