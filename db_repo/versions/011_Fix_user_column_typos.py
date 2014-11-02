from sqlalchemy import *
from migrate import *

meta = MetaData()


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    user = Table('user', meta, autoload=True)
    created_at = user.c.get(' created_at')
    created_at.alter(name='created_at')
    default_profile = user.c.get(' default_profile')
    default_profile.alter(name='default_profile')


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    user = Table('user', meta, autoload=True)
    user.c.created_at.alter(name=' created_at')
    user.c.default_profile.alter(name=' default_profile')
