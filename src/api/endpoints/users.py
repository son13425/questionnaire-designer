"""Роутеры для юзеров."""
from fastapi import APIRouter

from core.user import auth_backend, fastapi_users
from schemas.users import UserCreate, UserRead, UserUpdate


# создаем роутер
router = APIRouter()


# аутентификационный роутер(/login и /logout)
router.include_router(
    # В роутер аутентификации
    # передается объект бэкенда аутентификации.
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['auth'],
)

# регистрационный роутер (/register)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['auth'],
)

# роутер пользователей (чтение из БД, удаление, обновление)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix='/users',
    tags=['users'],
)
