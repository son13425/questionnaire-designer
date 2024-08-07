"""Схемы для полей анкет."""
from typing import Optional
from pydantic import BaseModel


class Fields(BaseModel):
    """Базовый класс схемы объекта Поля анкеты."""
    id: Optional[int]
    uuid: Optional[str]
    label: Optional[str]
