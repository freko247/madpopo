from sqlalchemy import *
from migrate import *

meta = MetaData()


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    tweet = Table('tweet', meta, autoload=True)
    tweet.c.lan.alter(name='lat')


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    print 'loading table'
    tweet = Table('tweet', meta, autoload=True)
    print tweet.columns.items()
    tweet.c.lat.alter(name='lan')
