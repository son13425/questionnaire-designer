"""Работа с данными справочников"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import (OrganizationsReferences, PositionsReferences,
                    RegistrationGoalsReferences, RolesReferences)
from schemas.references import ReferenceCreate


# Создание объектов в справочниках
# TO DO: реализовать проверку уникальности новой записи
async def create_reference_organization(
    new_references: ReferenceCreate,
    session: AsyncSession
) -> OrganizationsReferences:
    """Записывает объект Организация в таблицу organizationsreference"""
    # конвертируем объект ReferenceCreate в словарь
    new_organization_data = new_references.dict()
    # создаем объект модели OrganizationsReferences
    db_organization = OrganizationsReferences(**new_organization_data)
    # записываем объект в базу
    session.add(db_organization)
    await session.commit()
    await session.refresh(db_organization)
    # возвращаем обновленный объект из базы
    return db_organization


async def create_reference_position(
    new_references: ReferenceCreate,
    session: AsyncSession
) -> PositionsReferences:
    """Записывает объект Должность в таблицу positionsreference"""
    new_position_data = new_references.dict()
    db_position = PositionsReferences(**new_position_data)
    session.add(db_position)
    await session.commit()
    await session.refresh(db_position)
    return db_position


async def create_reference_registration_goal(
    new_references: ReferenceCreate,
    session: AsyncSession
) -> RegistrationGoalsReferences:
    """
    Записывает объект Цель регистрации в таблицу registrationgoalsreferences.
    """
    new_goal_data = new_references.dict()
    db_goal = RegistrationGoalsReferences(**new_goal_data)
    session.add(db_goal)
    await session.commit()
    await session.refresh(db_goal)
    return db_goal


async def create_reference_role_user(
    new_references: ReferenceCreate,
    session: AsyncSession
) -> RolesReferences:
    """Записывает объект Роль пользователя в таблицу rolesreferences"""
    new_role_data = new_references.dict()
    db_role = RolesReferences(**new_role_data)
    session.add(db_role)
    await session.commit()
    await session.refresh(db_role)
    return db_role


# чтение объектов в справочниках
async def get_all_obj_from_reference(
        model,
        session: AsyncSession
) -> list[str]:
    """Возвращает список name всех объектов в справочнике"""
    db_names = await session.execute(select(model.name))
    return db_names.scalars().all()
