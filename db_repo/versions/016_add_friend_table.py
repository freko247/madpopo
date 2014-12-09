from sqlalchemy import *
from migrate import *

meta = MetaData()

friend = Table('friend', meta,
               Column('user_id', String(20)),
               Column('friend_id', String(20)),
               )


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    friend.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    friend.drop()
