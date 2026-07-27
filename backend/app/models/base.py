# What is a Mixin?
# Suppose we create these models:
# User
# Agent
# Document
# Conversation
# Evaluation

# Every one needs:
# created_at
# updated_at

# Without a mixin:
# class User(Base):
#     created_at = ...
#     updated_at = ...

# class Agent(Base):
#     created_at = ...
#     updated_at = ...

# class Document(Base):
#     created_at = ...
#     updated_at = ...

# That's duplicate code.

# Instead:
# class User(Base, TimestampMixin):
# Done.

# Every model automatically gets:
# created_at
# updated_at

from datetime import datetime
from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column


class TimestampMixin:
    """Mixin class to add created_at and updated_at timestamp columns to a model."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
