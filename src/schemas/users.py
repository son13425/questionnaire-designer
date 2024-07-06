"""Схемы юзера."""

from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """Схема получения юзера."""
    pass


class UserCreate(schemas.BaseUserCreate):
    """Схема создания юзера"""
    pass


class UserUpdate(schemas.BaseUserUpdate):
    """Схема обновления юзера"""
    pass
