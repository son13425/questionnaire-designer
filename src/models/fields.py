"""Модели таблиц полей."""
from sqlalchemy import (Column, String)
from sqlalchemy.orm import relationship

from db.db import Base


class Fields(Base):
    """Создает модель поля анкеты."""
    uuid = Column(String, unique=True, nullable=False)
    label = Column(String)
    sections = relationship('Sections')
