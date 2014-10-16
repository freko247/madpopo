# -*- coding:utf-8 -*-
import config
import db
from friends import update_users, lookup_users
from followers import getFollowers
from log import logger
from models import User
from twitterConnection import twitter_api


def main():
    try:
        logger.info('Starting user updater.')
        db.init_db()
        followers_list = []
        user = twitter_api.users.show(user_id=config.TWEET_USER_ID)
        followers_list = getFollowers(
            config.TWEET_USER_ID, user.get('followers_count'))
        update_users(followers_list, friends=True)
        users_list = []
        for user in db.session.query(User).all():
            if not user.followed_back:
                users_list.append(user.user_id)
        users_list_extended = lookup_users(users_list)
        update_users(users_list_extended)
    except Exception, err:
        logger.error('%s: %s' % (Exception, err))

if __name__ == '__main__':
    main()
