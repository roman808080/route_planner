import sqlalchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.sql import schema

from db_utils import db_url

metadata: MetaData = sqlalchemy.MetaData()

cities: schema.Table = sqlalchemy.Table(
    "cities",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(length=100)),
    sqlalchemy.Column("lattitude", sqlalchemy.Float),
    sqlalchemy.Column("longitude", sqlalchemy.Float),
)

async_engine = create_async_engine(db_url, echo=True)


async def create_all_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
