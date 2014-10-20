from sqlalchemy import MetaData, Table, DateTime, Float, String, Column
from migrate import *

meta = MetaData()

status = Table(
    'status', meta,
    Column('created_at', DateTime),
    Column('lat', Float()),
    Column('lon', Float()),
    Column('status_id', String(length=20), primary_key=True),
    Column('text', String(length=500)),
    )


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    status.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    status.drop()
