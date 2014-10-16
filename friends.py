# -*- coding:utf-8 -*-
from datetime import datetime

from dateutil import parser

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


def update_users(users, friends=False):
    db.init_db()
    for user in users:
        stored_user = db.session.query(
            User).filter_by(user_id=user['id_str']).first()
        updated_user = stored_user or User(user_id=user['id_str'])
        # Add followed_back date if user is friend and it is not set
        if (friends and not updated_user.followed_back):
            updated_user.followed_back = datetime.now()
        join_date = parser.parse(user['created_at']).replace(tzinfo=None)
        updated_user.join_date = join_date
        updated_user.tweets = user['statuses_count']
        updated_user.friends = user['friends_count']
        updated_user.followers = user['followers_count']
        updated_user.language = get_language(user['lang'])
        # TODO add following values...
        # activity = Column(Float())          # tweet_frequency
        # followed = Column(DateTime)         # Date when user was followed
        # followed_back = Column(DateTime)    # Date when user followed back
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
            logger.debug('Looking up users %d to %d' % (0, len(friends)))
        else:
            user_list += twitter_api.users.lookup(
                user_id=','.join(users[stop-max_limit:]))
            logger.debug('Looking up users %d to %d' % (
                stop-max_limit, len(friends)))
    return user_list
