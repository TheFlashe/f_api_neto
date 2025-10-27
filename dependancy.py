from typing import Annotated
from fastapi import Depends
from models import DbSession
from sqlalchemy.ext.asyncio import AsyncSession


async def get_session() -> AsyncSession:
    async with DbSession() as session:
        yield session


SessionDependancy = Annotated[AsyncSession, Depends(get_session)]
