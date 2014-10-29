from sqlalchemy import *
from migrate import *

meta = MetaData()


new_columns = [
    Column('contributors_enabled', Boolean()),
    Column(' created_at', DateTime()),
    Column(' default_profile', Boolean()),
    Column('default_profile_image', Boolean()),
    Column('description', String(1000)),
    Column('favourites_count', Integer()),
    Column('follow_request_sent', Boolean()),
    Column('following', Boolean()),
    Column('geo_enabled', Boolean()),
    Column('is_translator', Boolean()),
    Column('listed_count', Integer()),
    Column('location', String(200)),
    Column('name', String(200)),
    Column('profile_background_color', String(6)),
    Column('profile_background_image_url', String(200)),
    Column('profile_background_image_url_https', String(200)),
    Column('profile_background_tile', Boolean()),
    Column('profile_banner_url', String(200)),
    Column('profile_image_url', String(200)),
    Column('profile_image_url_https', String(200)),
    Column('profile_link_color', String(6)),
    Column('profile_sidebar_border_color', String(6)),
    Column('profile_sidebar_fill_color', String(6)),
    Column('profile_text_color', String(6)),
    Column('profile_use_background_image', Boolean()),
    Column('protected', Boolean()),
    Column('screen_name', String(200)),
    Column('show_all_inline_media', Boolean()),
    Column('time_zone', String(200)),
    Column('url', String(200)),
    Column('utc_offset', Integer()),
    Column('verified', Boolean()),
    Column('withheld_in_countries', Boolean()),
    Column('withheld_scope', Boolean()),
    ]


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    user = Table('user', meta, autoload=True)
    user.c.followers.alter(name='followers_count')
    user.c.friends.alter(name='friends_count')
    user.c.tweets.alter(name='statuses_count')
    for col in new_columns:
            col.create(user, populate_default=False)


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    user = Table('user', meta, autoload=True)
    for col in new_columns:
        col.drop(user)
    user.c.followers_count.alter(name='followers')
    user.c.friends_count.alter(name='friends')
    user.c.statuses_count.alter(name='tweets')
