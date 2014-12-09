from sqlalchemy import *
from migrate import *


meta = MetaData()

old_friend = Table('friend', meta,
                   Column('user_id', String(20)),
                   Column('friend_id', String(20)),
                   )

friend = Table('friends', meta,
               Column('user_id', String(20), primary_key=True),
               Column('friend_id', String(20), primary_key=True),
               )


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    old_friend.drop()
    friend.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    old_friend.create()
    friend.drop()
