"""Модели таблицы юзеров"""
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, Integer, ForeignKey, String

from db.db import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    """Создает класс пользователя"""
    # базовые поля: id, email, is_active, is_superuser, is_verified
    # добавляем пользовательские поля
    organization = Column(
        Integer,
        ForeignKey('organizationsreferences.id')
    )
    surname = Column(
        String,
        nullable=False
    )
    username = Column(
        String,
        nullable=False
    )
    patronymic = Column(String)
    position = Column(
        Integer,
        ForeignKey('positionsreferences.id')
    )
    phone = Column(
        String,
        nullable=False
    )
    registration_goal = Column(
        Integer,
        ForeignKey('registrationgoalsreferences.id')
    )
    role = Column(
        Integer,
        ForeignKey('rolesreferences.id')
    )
