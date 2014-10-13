from sqlalchemy import String, Integer, MetaData, Table
from migrate import *


meta = MetaData()


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    tweet = Table('tweet', meta, autoload=True)
    tweet.c.user_id.alter(type=String(20))


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    tweet = Table('tweet', meta, autoload=True)
    tweet.c.lat.alter(type=Integer())
