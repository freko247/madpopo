from sqlalchemy import *
from migrate import *

meta = MetaData()

tweet = Table(
    'tweet', meta,
    Column('created_at', DateTime),
    Column('id', Integer, primary_key=True),
    Column('lan', Float()),
    Column('lon', Float()),
    Column('retweet_count', Integer()),
    Column('text', String(length=500)),
    Column('tweet_id', String(20)),
    Column('user_id', String(20)),
    )


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    tweet.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    tweet.drop()
