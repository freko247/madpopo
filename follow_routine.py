# -*- coding:utf-8 -*-
from datetime import datetime, timedelta

import db
from models import User
from followers import getFollowers, followUsers
from log import logger


def main():
    follows = 100
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
            "Following todays favorite's (%s) followers" % favorite)
        favorite_followers = getFollowers(favorite, follows)
        favorite_followers_ids = [follower.get('id_str') for follower
                                  in favorite_followers[:follows]
                                  if follower not in user_list]
        followUsers(favorite_followers_ids)
        new_favorite = User()
        new_favorite.user_id = favorite_followers[0].get('id_str')
        new_favorite.favorited = datetime.now() + timedelta(days=6)
    else:
        logger.info('No favorite for today.')


if __name__ == '__main__':
    main()
