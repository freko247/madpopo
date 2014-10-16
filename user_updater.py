# -*- coding:utf-8 -*-
import db
import friends
from log import logger
from models import User


def main():
    logger.info('Starting friend updater.')
    db.init_db()
    friends_list = []
    for friend in db.session.query(User).all():
        friends_list.append(friend.user_id)
    friends.update_friends(friends_list)


if __name__ == '__main__':
    main()
