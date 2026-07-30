# Why UUID?

# Most tutorials use:

# 1
# 2
# 3
# 4
# 5

# Those are predictable.

# Anyone can guess:

# /users/6
# /users/7
# /users/8

# Enterprise systems usually use UUIDs.

# Example:

# 4bfa1b2e-0f55-4c4c-a8ab-f0d48e60d74c

# Impossible to guess.

# Better for distributed systems.

import uuid
from enum import Enum

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from app.database.base import Base
from app.models.base import TimestampMixin


class UserRole(str, Enum):
    """Enumeration of user roles."""

    ADMIN = "admin"
    DEVELOPER = "developer"
    ANALYST = "analyst"
    VIEWER = "viewer"


class User(Base, TimestampMixin):
    """SQLAlchemy model for the User table."""

    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    role: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default=UserRole.VIEWER.value,
    )
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        default=True,
    )
