import os

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
# SQLALCHEMY_DATABASE_URL = (
#     "postgresql+asyncpg://postgres:postgres@127.0.0.1:5555/postgres"
# )
# running application in container:
SQLALCHEMY_DATABASE_URL = (
    "postgresql+asyncpg://postgres:postgres@postgres:5432/postgres"
)


engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


# Dependency
async def get_db() -> AsyncSession:
    async with SessionLocal() as db:
        yield db
