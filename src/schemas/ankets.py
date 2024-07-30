"""Схемы для анкет."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class Ankets(BaseModel):
    """Базовый класс схемы объекта Анкета"""
    label: Optional[str]
    description: Optional[str]
    is_active: Optional[bool]
    is_open: Optional[bool]
    is_subscribe: Optional[bool]
    for_iac: Optional[bool]


class AnketUpdate(Ankets):
    """Схема для объекта обновления Анкеты"""
    group: Optional[str]


class AnketResponse(Ankets):
    """Класс схемы для возврата объекта Aнкета"""
    group: Optional[str]
    id: Optional[int]

    class Config:
        """Разрешает сериализовать ORM-модель в схему"""
        orm_mode = True


class AnketCreate(Ankets):
    """Класс схемы для создания Aнкеты"""
    label: str = Field('<без названия>', min_length=1, max_length=100)
    is_active: bool = Field(True)
    is_open: bool = Field(True)
    is_subscribe: bool = Field(True)
    for_iac: bool = Field(False)
    group: str = Field('Общие')


class AnketDB(Ankets):
    """Класс схемы для возвращения объекта Анкета из БД"""
    id: Optional[int]
    uuid: Optional[str]
    groups_id: Optional[int]

    class Config:
        """Разрешает сериализовать ORM-модель в схему"""
        orm_mode = True


class GroupBase(BaseModel):
    """Базовый класс схемы Группа анкет"""
    label: Optional[str] = Field(..., min_length=1, max_length=100)


class GroupCreate(GroupBase):
    """Класс схемы для создания Группы анкет"""
    label: str = Field(..., min_length=1, max_length=100)


class GroupDB(GroupCreate):
    """Класс схемы для возвращения объекта Группа анкет"""
    id: int

    class Config:
        """Разрешает сериализовать ORM-модель в схему"""
        orm_mode = True


class GroupsAnketsDB(BaseModel):
    """Класс схемы для Группы с ее анкетами"""
    group: GroupDB
    ankets: list[AnketDB]

    class Config:
        """Разрешает сериализовать ORM-модель в схему"""
        orm_mode = True