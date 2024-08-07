"""Схемы для разделов анкет."""
from typing import Optional
from pydantic import BaseModel, Field


class Sections(BaseModel):
    """Базовый класс схемы объекта Раздел анкеты."""
    id: Optional[int]
    uuid: Optional[str]
    label: Optional[str]
    columns: Optional[int]
    sorting: Optional[int]
    ankets_uuid: Optional[str]
    chapters_id: Optional[int]
    dependent_field_uuid: Optional[str]


class SectionCreate(Sections):
    """Базовый класс схемы запроса для создания объекта Раздел анкеты."""
    label: str = Field('<без названия>')
    columns: int = Field(1, min=1, max=3)
    sorting:  int = Field(999)
    chapter: Optional[str]
    ankets_uuid: str
    dependent: Optional[str]


class SectionsResponse(Sections):
    """Схема ответа объекта Раздел"""

    class Config:
        """Разрешает сериализовать ORM-модель в схему"""
        orm_mode = True


class Chapters(BaseModel):
    """Базовый класс схемы объекта Родитель Раздела анкеты."""
    id: Optional[int]
    label: Optional[str]


class ChaptersResponse(Chapters):
    """Схема ответа объекта Родитель Раздела анкеты."""

    class Config:
        """Разрешает сериализовать ORM-модель в схему"""
        orm_mode = True
