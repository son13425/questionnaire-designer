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


class Groups(Base):
    """Создает модель для группы анкет."""
    label = Column(String, unique=True, nullable=False)
    ankets = relationship('Ankets')
