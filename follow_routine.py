# -*- coding:utf-8 -*-
from datetime import datetime, timedelta

import db
from models import User
from followers import getFollowers, followUsers
from log import logger


def main():
    db.init_db()
    users = db.session.query(User).all()
    favorite = None
    user_list = []
    logger.info('Starting follow routine.')
    for user in users:
        user_list.append(user.user_id)
        if user.favorited:
            if user.favorited.date() == datetime.today().date():
                favorite = user.user_id
    if favorite:
        logger.info(
            'Following todays favorites (%s) followers' % favorite)
        favorite_followers = getFollowers(favorite)
        favorite_followers = [follower for follower
                              in favorite_followers
                              if follower not in user_list]
        followUsers(favorite_followers[:100])
        new_favorite = User()
        new_favorite.user_id = favorite_followers[0]
        new_favorite.favorited = datetime.now() + timedelta(days=6)
    else:
        logger.info('No favorite for today.')


if __name__ == '__main__':
    main()
