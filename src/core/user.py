"""Настройка системы аутентификации пользователя."""
from typing import Union, Optional
from fastapi import Depends, Request
from fastapi_users import (BaseUserManager, FastAPIUsers, IntegerIDMixin,
                           InvalidPasswordException)
from fastapi_users.authentication import (AuthenticationBackend,
                                          BearerTransport, JWTStrategy)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from db.db import get_session
from models.users import User
from schemas.users import UserCreate


async def get_user_db(session: AsyncSession = Depends(get_session)):
    """Асинхронный генератор."""
    yield SQLAlchemyUserDatabase(session, User)


# Определяем транспорт: передавать токен будем
# через заголовок HTTP-запроса Authorization: Bearer.
# Указываем URL эндпоинта для получения токена.
bearer_transport = BearerTransport(tokenUrl='auth/jwt/login')


def get_jwt_strategy() -> JWTStrategy:
    """стратегия: хранение токена в виде JWT."""
    # В специальный класс из настроек приложения
    # передаётся секретное слово, используемое для генерации токена.
    # Вторым аргументом передаём срок действия токена в секундах.
    return JWTStrategy(secret=settings.secret, lifetime_seconds=3600)


# Создаём объект бэкенда аутентификации с выбранными параметрами.
auth_backend = AuthenticationBackend(
    name='jwt',  # Произвольное имя бэкенда (должно быть уникальным).
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    """Возвращает объект класса User."""
    # Здесь можно описать свои условия валидации пароля.
    # При успешной валидации функция ничего не возвращает.
    # При ошибке валидации будет вызван специальный класс ошибки
    # InvalidPasswordException.
    async def validate_password(
        self,
        password: str,
        user: Union[UserCreate, User],
    ) -> None:
        """Валидация пароля."""
        if user.email in password:
            raise InvalidPasswordException(
                reason='Пароль не должен содержать адрес электронной почты'
            )

    # действие после успешной регистрации
    # TO DO: отправить юзеру письмо с логином и паролем
    async def on_after_register(
        self, user: User,
        request: Optional[Request] = None
    ):
        print(f"User {user.email} has registered")


async def get_user_manager(user_db=Depends(get_user_db)):
    """Возвращает объект класса UserManager."""
    yield UserManager(user_db)


# Создаём объект класса FastAPIUsers
fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


# текущий user
current_user = fastapi_users.current_user(active=True)


# superuser
current_superuser = fastapi_users.current_user(active=True, superuser=True)
