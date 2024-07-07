"""Базовые настройки приложения"""

import os


from logging import config as logging_config
from typing import Optional
from pydantic import BaseSettings, EmailStr, PostgresDsn
from src.core.logger import LOGGING


# Применяем настройки логирования
logging_config.dictConfig(LOGGING)

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Settings(BaseSettings):
    """Хранит переменные окружения."""
    name: str = 'Конструктор анкет'
    host: str = '0'
    port: int = 8000
    database_dsn: PostgresDsn = (
        'postgresql+asyncpg://postgres:postgres@localhost:5432/postgres'
    )
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    class Config:
        """Задает файл с переменными окружения."""
        env_file = '.env'


settings = Settings()

#  Настройки подключения к БД
ECHO = True
