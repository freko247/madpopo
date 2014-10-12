from sqlalchemy import *
from migrate import *

meta = MetaData()

user = Table(
    'user', meta,
    Column('activity', Float()),
    Column('followed', DateTime),
    Column('followed_back', DateTime),
    Column('followers', Integer()),
    Column('friends', Integer()),
    Column('join_date', DateTime),
    Column('language', Integer()),
    Column('tweets', Integer()),
    Column('user_id', Integer, primary_key=True)
    )

language = Table(
    'language', meta,
    Column('id', Integer(), primary_key=True),
    Column('language', String(5)),
    )


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    meta.bind = migrate_engine
    user.create()
    language.create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta.bind = migrate_engine
    language.drop()
    user.drop()
