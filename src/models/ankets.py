"""Модели таблиц анкет."""
from sqlalchemy import (Column, String, DateTime, ForeignKey,
                        Integer, Text, Boolean)
from sqlalchemy.orm import relationship

from db.db import Base


class Ankets(Base):
    """Создает модель для анкеты."""
    uuid = Column(String, unique=True, nullable=False)
    autor_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    label = Column(String)
    description = Column(Text)
    is_active = Column(Boolean, nullable=False)
    is_open = Column(Boolean, nullable=False)
    is_subscribe = Column(Boolean, nullable=False)
    for_iac = Column(Boolean, nullable=False)
    groups_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    sections = relationship('Sections')
    information = relationship('Information')
    files = relationship('Files')


class Groups(Base):
    """Создает модель для группы анкет."""
    label = Column(String, unique=True, nullable=False)
    ankets = relationship('Ankets')


class Information(Base):
    """Создает модель для дополнительной информации к анкете."""
    label = Column(String)
    description = Column(Text)
    sorting = Column(Integer)
    ankets_uuid = Column(String, ForeignKey('ankets.uuid'), nullable=False)


class Files(Base):
    """Создает модель объекта Прикрепленный файл."""
    label = Column(String)
    name = Column(String)
    link = Column(String)
    ankets_uuid = Column(String, ForeignKey('ankets.uuid'), nullable=False)