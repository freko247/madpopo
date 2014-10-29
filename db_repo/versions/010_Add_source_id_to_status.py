from sqlalchemy import *
from migrate import *

meta = MetaData()


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    status = Table('status', meta, autoload=True)
    col = Column('source_id', String(50))
    col.create(status, populate_default=False)


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    status = Table('status', meta, autoload=True)
    col = Column('source_id', String(50))
    col.drop(status)
