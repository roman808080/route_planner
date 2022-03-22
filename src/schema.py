import sqlalchemy
from sqlalchemy import MetaData
from sqlalchemy.sql import schema

metadata: MetaData = sqlalchemy.MetaData()

cities: schema.Table = sqlalchemy.Table(
    "cities",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(length=100)),
    sqlalchemy.Column("lattitude", sqlalchemy.Float),
    sqlalchemy.Column("longitude", sqlalchemy.Float),
)
