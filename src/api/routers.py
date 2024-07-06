"""Регистрация обработчиков."""
from fastapi import APIRouter

from api.endpoints import data_router, field_router, user_router


# Объект регистрации обработчиков
main_router = APIRouter()

# Добавление обработчиков в объект регистрации
main_router.include_router(data_router, tags=['data'],)
main_router.include_router(field_router, tags=['field'],)
main_router.include_router(user_router, tags=['user'],)
