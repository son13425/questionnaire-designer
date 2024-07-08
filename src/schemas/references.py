"""Схема для справочников."""
from pydantic import BaseModel


class ReferenceCreate(BaseModel):
    """Задает структуру объекта Справочник"""
    name: str
