"""Импорты класса Base и всех моделей для Alembic."""
from db.db import Base  # noqa
from models import (OrganizationsReferences, PositionsReferences, # noqa
                    RegistrationGoalsReferences, RolesReferences, # noqa
                    User, Ankets, Groups)  # noqa
