# -*- coding:utf-8 -*-
import json
from operator import itemgetter
from datetime import datetime
from time import sleep

from log import logger
from twitterConnection import twitter_api
import db
from models import User
'''This module provides basic functionality for management of followers.'''


def getFollowers(user_id, follows):
    '''Function gets a list of users following a given user.'''
    try:
        found_followers = []
        logger.debug("Looking for followers of: %s" % user_id)
        requests = follows/200 or 1
        request_counter = 0
        for i in range(requests):
            cursor = -1
            logger.debug("Getting followers %d/%d" % ((1+i), requests))
            if len(found_followers) > 0:
                cursor = found_followers[-1].get('next_cursor_str')
            found_followers.append(
                twitter_api.followers.list(user_id=user_id,
                                           count=200,
                                           cursor=cursor)
                )
            request_counter += 1
            if request_counter == 15:
                sleep(60*15)
                request_counter = 0
            logger.debug("Found %d followers" % (
                len(found_followers[i].get('users'))))
        followers_list = []
        for segment in found_followers:
            followers_list += segment.get('users')
        return followers_list
    except Exception, err:
        logger.error('%s: %s' % (Exception, err))


# def getTopFollowers(foundFollowers=None, user_count=100, source=None):
#     '''Returns a sorted list, based on number of user followers. List default
#     size is 100, but can be changed with argument. Source for user data can be
#     file or list of user objects.'''
#     if source:
#         logger.debug("Retrieving follower data from file, %s" % source)
#         f = open(source, 'r')
#         results = json.loads(f.read())
#         logger.debug("Data loaded from file.")
#         f.close()
#     else:
#         results = foundFollowers
#     followers = []
#     logger.debug("Sorting list of %d users" % len(results))
#     for result in results:
#         for user in result.get('users'):
#             followers.append((user.get('followers_count'), user.get('str_id')))
#     followers = sorted(followers, key=itemgetter(0), reverse=True)
#     logger.debug("Returning %d users with most followers." % user_count)
#     return followers[:user_count]


def followUsers(users):
    '''Given list of users (user_id) will be followed.'''
    db.init_db()
    for user in users:
        logger.info("Following: %s" % user)
        try:
            twitter_api.friendships.create(user_id=user, follow=False)
            new_user = User()
            new_user.followed = datetime.now()
            new_user.user_id = user
            db.session.merge(new_user)
            db.session.commit()
        except Exception, err:
            logger.info('%s: %s' % (Exception, err))


def unfollowUsers(users):
    '''Given list of users (user_id) will be unfollowed.'''
    db.init_db()
    for user in users:
        logger.info("Unfollowing: %s" % user)
        try:
            twitter_api.friendships.destroy(user_id=user)
            unfriend = db.session.query(User).filter_by(user_id=user).first()
            unfriend.unfollowed = datetime.now()
            db.session.merge(unfriend)
            db.session.commit()
        except Exception, err:
            logger.info("Could not unfollow: %s/n%s: %s" % (
                user, Exception, err))


def main():
    # followers = getFollowers('GordonRamsay')
    # topFollowers = getTopFollowers(followers)
    # followUsers([user[1] for user in topFollowers])
    pass


if __name__ == '__main__':
    main()
