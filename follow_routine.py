# -*- coding:utf-8 -*-
from datetime import datetime, timedelta

import db
from models import User
from followers import getFollowers, followUsers


def main():
    users = db.session.query(User).all()
    favorite = None
    user_list = []
    for user in users:
        user_list.append(user.user_id)
        if user.favorited.date() == datetime.today().date():
            favorite = user.user_id
    favorite_followers = getFollowers(favorite)
    favorite_followers = [follower for follower
                          in favorite_followers
                          if follower not in user_list]
    followUsers(favorite_followers[:100])
    new_favorite = User()
    new_favorite.user_id = favorite_followers[0]
    new_favorite.favorited = datetime.now() + timedelta(days=6)

if __name__ == '__main__':
    main()
