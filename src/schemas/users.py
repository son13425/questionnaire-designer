"""Схемы юзера."""
from fastapi_users import schemas
from typing import Optional


class UserRead(schemas.BaseUser[int]):
    """Схема получения юзера."""
    organization: Optional[int]
    surname: str
    name: str
    patronymic: Optional[str]
    position: Optional[int]
    phone: str
    registration_goal: Optional[int]
    role: int


class UserCreate(schemas.BaseUserCreate):
    """Схема создания юзера"""
    organization: Optional[int]
    surname: str
    name: str
    patronymic: Optional[str]
    position: Optional[int]
    phone: str
    registration_goal: Optional[int]
    role: int


class UserUpdate(schemas.BaseUserUpdate):
    """Схема обновления юзера"""
    organization: Optional[int]
    surname: str
    name: str
    patronymic: Optional[str]
    position: Optional[int]
    phone: str
    registration_goal: Optional[int]
    role: int
