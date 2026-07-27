# Create the ORM base class for SQLAlchemy models. This base class will be used to define all the models in the application.

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass
