"""Модели таблицы юзеров"""
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, Integer, ForeignKey, String, Text

from src.db.db import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    """Создает класс пользователя"""
    # базовые поля: id, email, is_active, is_superuser, is_verified
    # добавляем пользовательские поля
    organization = Column(Integer, ForeignKey('organizations_references.id'))
    surname = Column(String, nullable=False)
    username = Column(String, nullable=False)
    patronymic = Column(String)
    position = Column(Integer, ForeignKey('positions_references.id'))
    phone = Column(String, nullable=False)
    registration_goal = Column(Integer, ForeignKey('registration_goal_references.id'))
    role = Column(Integer, ForeignKey('roles_references.id'))
