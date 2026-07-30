# We'll have hundreds of database operations.
# Instead of every endpoint doing:
# connection = ...
# cursor = ...

# every API simply writes:
# db: AsyncSession = Depends(get_db)

# FastAPI automatically:
# Opens the connection
# Manages the session
# Cleans it up afterward

# This keeps our code clean and avoids connection leaks.
from app.core.config import settings
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


engine = create_async_engine(
    settings.database_url,
    echo=False,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
