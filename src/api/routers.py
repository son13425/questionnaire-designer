"""Регистрация обработчиков."""
from fastapi import APIRouter

from api.endpoints import (data_router, field_router,
                           reference_router, user_router)


# Объект регистрации обработчиков
main_router = APIRouter()

# Добавление обработчиков в объект регистрации
main_router.include_router(data_router, tags=['Данные'])
main_router.include_router(field_router, tags=['Поля'])
main_router.include_router(reference_router, tags=['Справочники'])
main_router.include_router(user_router)
