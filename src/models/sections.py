"""Модели таблиц секций анкет."""
from sqlalchemy import (Column, String, ForeignKey,
                        Integer)
from sqlalchemy.orm import relationship

from db.db import Base


class Sections(Base):
    """Создает модель раздела анкеты."""
    uuid = Column(String, unique=True, nullable=False)
    label = Column(String)
    columns = Column(Integer)
    sorting = Column(Integer)
    ankets_uuid = Column(String, ForeignKey('ankets.uuid'), nullable=False)
    chapters_id = Column(Integer, ForeignKey('chapters.id'))
    dependent_field_uuid = Column(String, ForeignKey('fields.uuid'))


class Chapters(Base):
    """Создает модель родительской группы разделов анкет."""
    label = Column(String, unique=True, nullable=False)
    sections = relationship('Sections')
