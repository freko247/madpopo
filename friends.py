# -*- coding:utf-8 -*-
from log import logger
from models import User
from twitterConnection import twitter_api
import config
import db
import models
from dateutil import parser
from models import User
from time import sleep
from twitterConnection import twitter_api
from lookup_functions import get_language


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


def update_users(users):
    db.init_db()
    for user in users:
        new_user = User()
        new_user.user_id = user['id_str']
        join_date = parser.parse(user['created_at']).replace(tzinfo=None)
        new_user.join_date = join_date
        new_user.tweets = user['statuses_count']
        new_user.friends = user['friends_count']
        new_user.followers = user['followers_count']
        new_user.language = get_language(user['lang'])
        # TODO add following values...
        # activity = Column(Float())          # tweet_frequency
        # followed = Column(DateTime)         # Date when user was followed
        # followed_back = Column(DateTime)    # Date when user followed back
        db.session.merge(new_user)
        db.session.commit()
    logger.info('Updating %d users' % len(users))


def update_friends(friends,
                   max_limit=100,
                   max_requests=180,
                   sleep_time=15):
    stop = max_limit
    requests = 0
    while stop < len(friends):
        users = twitter_api.users.lookup(
            user_id=','.join(friends[stop-max_limit:stop]))
        logger.info('Updating users %d to %d' % (stop-max_limit, stop))
        update_users(users)
        stop += max_limit
        requests += 1
        if requests >= max_requests:
            logger.info('Request max limit (%d), sleep for %d minutes' % (
                max_limit, sleep_time))
            sleep(60*sleep_time)
            requests = 0
    else:
        users = None
        if len(friends) < max_limit:
            users = twitter_api.users.lookup(user_id=','.join(friends))
            logger.info('Updating users %d to %d' % (0, len(friends)))
        else:
            users = twitter_api.users.lookup(
                user_id=','.join(friends[stop-max_limit:]))
            logger.info('Updating users %d to %d' % (
                stop-max_limit, len(friends)))
        update_users(users)
        requests += 1
