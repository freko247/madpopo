# -*- coding:utf-8 -*-
from datetime import datetime, timedelta

from followers import getFollowers, followUsers
from log import logger
from models import User
import config
import db


def main():
    try:
        follows = 100
        db.init_db()
        users = db.session.query(User).all()
        favorite = None
        user_list = []
        logger.debug('Starting follow routine.')
        for user in users:
            user_list.append(user.user_id)
            if user.favorited:
                if user.favorited.date() == datetime.today().date():
                    favorite = user.user_id
                    break
        if favorite:
            logger.debug(
                "Following todays favorite's (%s) followers" % favorite)
            favorite_followers = getFollowers(favorite, follows)
            favorite_followers_ids = [follower.get('id_str') for follower
                                      in favorite_followers[:follows]
                                      if follower not in user_list
                                      and follower != config.TWEET_USER_ID]
            followUsers(favorite_followers_ids)
            new_favorite = User()
            new_favorite.user_id = favorite_followers[0].get('id_str')
            new_favorite.favorited = datetime.now() + timedelta(days=6)
        else:
            logger.debug('No favorite for today.')
    except Exception, err:
        logger.error('%s: %s' % (Exception, err))


if __name__ == '__main__':
    main()
