from sqlalchemy import *
from migrate import *


meta = MetaData()

def upgrade(migrate_engine):
    meta.bind = migrate_engine
    tweet = Table('tweet', meta, autoload=True)
    i = Index('ix_tweet_user_id', tweet.c.user_id)
    i.create()

def downgrade(migrate_engine):
    meta.bind = migrate_engine
    tweet = Table('tweet', meta, autoload=True)
    i = Index('ix_tweet_user_id', tweet.c.user_id)
    i.drop()
