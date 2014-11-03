# -*- coding:utf-8 -*-
from datetime import datetime

from dateutil import parser

from followers import followUsers
from log import logger
from lookup_functions import get_language
from models import User
from time import sleep
from twitterConnection import twitter_api
import config
import db
import models


def getFriends(screen_name=config.TWEET_SCREEN_NAME):
    id_list = []
    result = twitter_api.friends.ids(screen_name=screen_name)
    logger.info(
        'Getting friends of %s' % screen_name)
    while result.get('next_cursor'):
        cursor = result.get('next_cursor')
        id_list += result.get('ids')
        result = twitter_api.friends.ids(
            cursor=cursor, screen_name=screen_name)
    else:
        id_list += result.get('ids')
    logger.info('Got %d users' % len(id_list))
    return [str(v) for v in id_list]


def update_users(users, user_followers=False):
    db.init_db()
    for user in users:
        stored_user = db.session.query(
            User).filter_by(user_id=user['id_str']).first()
        updated_user = stored_user or User(user_id=user['id_str'])
        # Follow user back if not already followed
        if user_followers and not updated_user.followed:
            followUsers([updated_user.user_id])
            updated_user.followed = datetime.now()
        # Add followed_back date if user is friend and it is not set
        if (user_followers and not updated_user.followed_back):
            updated_user.followed_back = datetime.now()
        join_date = parser.parse(user['created_at']).replace(tzinfo=None)
        updated_user.join_date = join_date
        updated_user.contributors_enabled = user.get('contributors_enabled')
        updated_user.default_profile = user.get('default_profile')
        updated_user.default_profile_image = user.get('default_profile_image')
        updated_user.favourites_count = user.get('favourites_count')
        updated_user.follow_request_sent = user.get('follow_request_sent')
        updated_user.followers_count = user.get('followers_count')
        updated_user.following = user.get('following')
        updated_user.friends_count = user.get('friends_count')
        updated_user.geo_enabled = user.get('geo_enabled')
        updated_user.is_translator = user.get('is_translator')
        updated_user.language = get_language(user.get('lang'))
        updated_user.listed_count = user.get('listed_count')
        updated_user.profile_background_color = user.get(
            'profile_background_color')
        updated_user.profile_background_image_url = user.get(
            'profile_background_image_url')
        updated_user.profile_background_image_url_https = user.get(
            'profile_background_image_url_https')
        updated_user.profile_background_tile = user.get(
            'profile_background_tile')
        updated_user.profile_banner_url = user.get('profile_banner_url')
        updated_user.profile_image_url = user.get('profile_image_url')
        updated_user.profile_image_url_https = user.get(
            'profile_image_url_https')
        updated_user.profile_link_color = user.get('profile_link_color')
        updated_user.profile_sidebar_border_color = user.get(
            'profile_sidebar_border_color')
        updated_user.profile_sidebar_fill_color = user.get(
            'profile_sidebar_fill_color')
        updated_user.profile_text_color = user.get('profile_text_color')
        updated_user.profile_use_background_image = user.get(
            'profile_use_background_image')
        updated_user.protected = user.get('protected')
        updated_user.screen_name = user.get('screen_name')
        updated_user.show_all_inline_media = user.get('show_all_inline_media')
        updated_user.statuses_count = user.get('statuses_count')
        updated_user.time_zone = user.get('time_zone')
        updated_user.url = user.get('url')
        updated_user.utc_offset = user.get('utc_offset')
        updated_user.verified = user.get('verified')
        updated_user.withheld_in_countries = user.get('withheld_in_countries')
        updated_user.withheld_scope = user.get('withheld_scope')

        for attribute in ['description', 'name', 'location']:
            try:
                data = user.get(attribute)
                data.decode('utf-8')
                updated_user.__setattr__(attribute, data)
            except:
                # logger.debug('Encoding error for %s for user: %s' %
                #              (attribute, updated_user.screen_name))
                pass

        db.session.merge(updated_user)
        db.session.commit()
    logger.info('Updating %d users' % len(users))


def lookup_users(users,
                 max_limit=100,
                 max_requests=180,
                 sleep_time=15):
    stop = max_limit
    requests = 0
    user_list = []
    while stop < len(users):
        user_list += twitter_api.users.lookup(
            user_id=','.join(users[stop-max_limit:stop]))
        logger.debug('Looking up users %d to %d' % (stop-max_limit, stop))
        stop += max_limit
        requests += 1
        if requests >= max_requests:
            logger.debug('Request max limit (%d), sleep for %d minutes' % (
                max_limit, sleep_time))
            sleep(60*sleep_time)
            requests = 0
    else:
        if len(users) < max_limit:
            user_list += twitter_api.users.lookup(user_id=','.join(users))
            logger.debug('Looking up users %d to %d' % (0, len(users)))
        else:
            user_list += twitter_api.users.lookup(
                user_id=','.join(users[stop-max_limit:]))
            logger.debug('Looking up users %d to %d' % (
                stop-max_limit, len(users)))
    return user_list
