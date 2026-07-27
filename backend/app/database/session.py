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

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.core.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
