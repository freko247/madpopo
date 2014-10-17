from sqlalchemy import MetaData, Table, DateTime, Float, String, Column
from migrate import *

meta = MetaData()

retweet = Table(
    'retweet', meta,
    Column('tweet_id', String(length=20)),
    Column('retweet_date', DateTime),
    Column('sentiment', Float()),
    )


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    retweet.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    retweet.drop()
