"""Точка входа приложения."""

import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from api.routers import main_router
from core.config import settings
from core.init__db import create_first_superuser


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

origins = [
    'http://84.201.154.109'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'OPTIONS', 'DELETE', 'PATCH', 'PUT'],
    allow_headers=[
        'Content-Type',
        'Set-Cookie',
        'Access-Control-Allow-Headers',
        'Access-Control-Allow-Origin',
        'Authorization'
    ],
)

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
