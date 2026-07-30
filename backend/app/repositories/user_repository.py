# The repository is the only layer that communicates directly with the database, allowing the rest of the application to remain clean, modular, and maintainable.

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserRepository:
    """Repository class for user-related database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_email(self, email: str) -> User | None:
        """Fetch a user by email."""
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def create_user(self, user: User) -> User:
        """Create a new user in the database."""
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
