"""Роутеры для справочников."""
from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_session
from db.references import (create_reference_organization,
                           create_reference_position,
                           create_reference_registration_goal,
                           create_reference_role_user,
                           get_all_obj_from_reference)
from models import (OrganizationsReferences, PositionsReferences,
                    RegistrationGoalsReferences, RolesReferences)
from schemas.references import ReferenceCreate


# создаем роутер
router = APIRouter()


@router.get('/organization/')
async def get_all_organizations(
    session: AsyncSession = Depends(get_session)
):
    """Возвращает список всех организаций из справочника организаций"""
    all_organizations = await get_all_obj_from_reference(
        OrganizationsReferences,
        session
    )
    if all_organizations is None:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='В справочнике Организаций нет записей'
        )
    return {'organizations': all_organizations}


@router.post('/organization/')
async def create_new_organization(
    organization: ReferenceCreate,
    session: AsyncSession = Depends(get_session)
):
    """Создает новую Организацию в справочнике организаций."""
    new_organization = await create_reference_organization(
        organization,
        session
    )
    return new_organization


@router.get('/position/')
async def get_all_positions(
    session: AsyncSession = Depends(get_session)
):
    """Возвращает список всех должностей из справочника организаций"""
    all_positions = await get_all_obj_from_reference(
        PositionsReferences,
        session
    )
    if all_positions is None:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='В справочнике Должностей нет записей'
        )
    return {'positions': all_positions}


@router.post('/position/')
async def create_new_position(
    position: ReferenceCreate,
    session: AsyncSession = Depends(get_session)
):
    """Создает новую Должность в справочнике должностей."""
    new_position = await create_reference_position(
        position,
        session
    )
    return new_position


@router.get('/registration_goal/')
async def get_all_goals(
    session: AsyncSession = Depends(get_session)
):
    """Возвращает список всех целей регистрации из справочника целей"""
    all_goals = await get_all_obj_from_reference(
        RegistrationGoalsReferences,
        session
    )
    if all_goals is None:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='В справочнике Цели регистрации нет записей'
        )
    return {'goals': all_goals}


@router.post('/registration_goal/')
async def create_new_registration_goal(
    goal: ReferenceCreate,
    session: AsyncSession = Depends(get_session)
):
    """Создает новую Цель регистрации в справочнике целей."""
    new_goal = await create_reference_registration_goal(
        goal,
        session
    )
    return new_goal


@router.get('/user_role/')
async def get_all_user_roles(
    session: AsyncSession = Depends(get_session)
):
    """Возвращает список всех ролей пользователя из справочника ролей"""
    all_roles = await get_all_obj_from_reference(
        RolesReferences,
        session
    )
    if all_roles is None:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='В справочнике Цели регистрации нет записей'
        )
    return {'roles': all_roles}


@router.post('/user_role/')
async def create_new_user_role(
    role: ReferenceCreate,
    session: AsyncSession = Depends(get_session)
):
    """Создает новую Роль юзера в справочнике ролей."""
    new_role = await create_reference_role_user(
        role,
        session
    )
    return new_role
