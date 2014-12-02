from sqlalchemy import *
from migrate import *

meta = MetaData()


new_columns = [
    Column('no_retweets', Integer()),
    Column('no_retweeted', Integer()),
    Column('avg_no_replies', Float()),
    Column('avg_no_mentions', Float()),
    ]


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    user = Table('user', meta, autoload=True)
    for col in new_columns:
            col.create(user, populate_default=False)


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    user = Table('user', meta, autoload=True)
    for col in new_columns:
        col.drop(user)
