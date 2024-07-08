"""Модели таблиц справочников."""
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from db.db import Base


class OrganizationsReferences(Base):
    """Создает модель для справочника организаций."""
    name = Column(String, unique=True, nullable=False)
    users = relationship('User')


class PositionsReferences(Base):
    """Создает модель для справочника должностей."""
    name = Column(String, unique=True, nullable=False)
    users = relationship('User')


class RegistrationGoalsReferences(Base):
    """Создает модель для справочника целей регистрации."""
    name = Column(String, unique=True, nullable=False)
    users = relationship('User')


class RolesReferences(Base):
    """Создает модель для справочника ролей юзера."""
    name = Column(String, unique=True, nullable=False)
    users = relationship('User')
