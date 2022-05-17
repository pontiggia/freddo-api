from sqlalchemy import Column, Table
from sqlalchemy.sql.sqltypes import Integer, String
from ..config.database import meta, engine

users = Table('users', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String(255)),
    Column('email', String(255)),
    Column('customerSince', String(255)),
    Column('phone', String(255)),
    Column('customerId', String(255)))

meta.create_all(engine)