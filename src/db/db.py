"""Базовый класс для моделей таблиц базы данных"""
from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker

from src.core.config import ECHO, settings


class PreBase:
    """Базовый класс для моделей таблиц базы данных"""
    @declared_attr
    def __tablename__(cls):
        """Присваивает название модели в нижнем регистре имени таблицы"""
        # Именем таблицы будет название модели в нижнем регистре.
        return cls.__name__.lower()

    # Во все таблицы будет добавлено поле ID.
    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)

# Создаём движок
# Настройки подключения к БД передаём из переменных окружения,
# которые заранее загружены в файл настроек
engine = create_async_engine(
    settings.database_dsn,
    echo=ECHO,
    future=True
)
# Создаем множество сессий
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_session() -> AsyncSession:
    """Внедрение зависимостей Dependency."""
    async with async_session() as session:
        yield session
