"""Точка входа приложения."""

import uvicorn

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from api.routers import main_router
from core.config import settings
from core.init_db import create_first_superuser


# Инициализация объекта приложения
app = FastAPI(
    title=settings.name,
    default_response_class=ORJSONResponse,
    # адреса документации
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json'
)
# Подключение роутеров
app.include_router(main_router)


@app.on_event('startup')
async def startup():
    """Создает первого пользователя(суперюзера)"""
    await create_first_superuser()


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=settings.host,
        port=settings.port,
        reload=True
    )
