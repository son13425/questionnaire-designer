"""Модели таблиц справочников."""
from sqlalchemy import Column, String

from app.core.db import Base


class ReferencesBase(Base):
    """Создает базовый класс для моделей справочников."""
    # Название элемента справочника должно быть не больше 100 символов,
    # уникальным и непустым.
    name = Column(String(100), unique=True, nullable=False)


class OrganizationsReferences(ReferencesBase):
    """Создает модель для справочника организаций."""
    pass


class PositionsReferences(ReferencesBase):
    """Создает модель для справочника должностей."""
    pass


class RegistrationGoalsReferences(ReferencesBase):
    """Создает модель для справочника целей регистрации."""
    pass
