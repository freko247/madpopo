from sqlalchemy import MetaData, Table, Column, DateTime
from migrate import *


meta = MetaData()


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    user = Table('user', meta, autoload=True)
    col = Column('favorited', DateTime)
    col.create(user, populate_default=False)


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    user = Table('user', meta, autoload=True)
    col = Column('favorited', DateTime)
    col.drop(user)
