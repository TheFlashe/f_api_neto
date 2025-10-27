import os
import datetime
from sqlalchemy import Integer, String, DateTime, func
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

from dotenv import load_dotenv


load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5431")

PG_DSN = (f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
          f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")

engine = create_async_engine(PG_DSN)
DbSession = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase, AsyncAttrs):
    @property
    def id_dict(self):
        return {"id": self.id}


class Desc(Base):
    __tablename__ = "descs_"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=True, index=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    price: Mapped[int] = mapped_column(Integer, nullable=True, index=True)
    author: Mapped[str] = mapped_column(String, nullable=True, index=True)
    create_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=False), server_default=func.now()
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=False),
        server_default=func.now(),
        onupdate=func.now())

    @property
    def dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "author": self.author,
            "create_at": self.create_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


ORM_OBJ = Desc
ORM_CLS = type[Desc]


async def init_orm():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_orm():
    await engine.dispose()
