from sqlalchemy import String, Integer, MetaData, Table
from migrate import *


meta = MetaData()


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    user = Table('user', meta, autoload=True)
    user.c.user_id.alter(type=String(20))


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    user = Table('user', meta, autoload=True)
    user.c.user_id.alter(type=Integer())
