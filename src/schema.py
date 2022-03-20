import sqlalchemy
from sqlalchemy import MetaData, func, text
from sqlalchemy.engine import Engine

from db_utils import db_url

metadata: MetaData = sqlalchemy.MetaData()

cities: sqlalchemy.sql.schema.Table = sqlalchemy.Table(
    "cities",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(length=100)),
    sqlalchemy.Column("latitude", sqlalchemy.Float),
    sqlalchemy.Column("longitude", sqlalchemy.Float),
)

engine: Engine = sqlalchemy.create_engine(db_url, pool_size=3, max_overflow=0, echo=True)
metadata.create_all(engine)
