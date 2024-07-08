"""Создает первого суперюзера если в базе нет юзеров"""
import contextlib

from fastapi_users.exceptions import UserAlreadyExists
from pydantic import EmailStr

from core.config import settings
from core.user import get_user_db, get_user_manager
from db.db import get_session
from schemas.users import UserCreate


# Превращаем асинхронные генераторы в асинхронные менеджеры контекста.
get_async_session_context = contextlib.asynccontextmanager(get_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_user(
    email: EmailStr,
    password: str,
    is_superuser: bool = False
):
    """Корутина, создающая суперюзера с переданным email и паролем"""
    try:
        # Получение объекта асинхронной сессии.
        async with get_async_session_context() as session:
            # Получение объекта класса SQLAlchemyUserDatabase.
            async with get_user_db_context(session) as user_db:
                # Получение объекта класса UserManager.
                async with get_user_manager_context(user_db) as user_manager:
                    # Создание пользователя.
                    await user_manager.create(
                        UserCreate(
                            email=email,
                            password=password,
                            is_superuser=is_superuser,
                            surname='string',
                            username='string',
                            phone='string',
                            role=4
                        )
                    )
    # В случае, если такой пользователь уже есть, ничего не предпринимать.
    except UserAlreadyExists:
        pass


async def create_first_superuser():
    """
    Корутина, проверяющая, указаны ли в настройках данные для суперюзера.
    Если да, то вызывается корутина create_user для создания суперпользователя.
    """
    if (settings.first_superuser_email is not None
            and settings.first_superuser_password is not None):
        await create_user(
            email=settings.first_superuser_email,
            password=settings.first_superuser_password,
            is_superuser=True
        )
