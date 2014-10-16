# -*- coding:utf-8 -*-
from models import User
import db
from datetime import datetime, timedelta
from followers import unfollowUsers
from log import logger


def main():
    try:
        logger.info('Running unfollow routine.')
        db.init_db()
        q = db.session.query(User).all()
        unfriend_list = []
        for user in q:
            # check if user is unfollowed
            # chech when user was followed longer than 24h ago
            # check if user has followed back
            yesterday = datetime.now()-timedelta(days=1)
            if (not user.unfollowed
                and user.followed < yesterday
                and not user.followed_back):
                unfriend_list.append(user.user_id)
        unfollowUsers(unfriend_list)
    except Exception, err:
        logger.error('%s: %s' % (Exception, err))


if __name__ == '__main__':
    main()
