"""Модели таблиц справочников."""
from sqlalchemy import Column, String

from src.db.db import Base


class OrganizationsReferences(Base):
    """Создает модель для справочника организаций."""
    name = Column(String, unique=True, nullable=False)


class PositionsReferences(Base):
    """Создает модель для справочника должностей."""
    name = Column(String, unique=True, nullable=False)


class RegistrationGoalsReferences(Base):
    """Создает модель для справочника целей регистрации."""
    name = Column(String, unique=True, nullable=False)


class RolesReferences(Base):
    """Создает модель для справочника ролей юзера."""
    name = Column(String, unique=True, nullable=False)
