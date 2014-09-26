# -*- coding:utf-8 -*-
import json
from operator import itemgetter

from log import logger
from twitterConnection import twitter_api
'''This module provides basic functionality for management of followers.'''


def getFollowers(screen_name, destinationFile=None):
    '''Function gets a list of users following a given user.'''
    found_followers = []
    logger.debug("Looking for followers of: %s" % screen_name)
    for i in range(15):
        cursor = -1
        logger.debug("Getting followers %d/15" % (1+i))
        if len(found_followers) > 0:
            cursor = found_followers[-1].get('next_cursor_str')
        found_followers.append(
            twitter_api.followers.list(screen_name=screen_name,
                                                 count=200,
                                                  cursor=cursor)
                                                  )
    if destinationFile:
        logger.debug("Writing to file, %s" % destinationFile)
        f = open(destinationFile, 'w')
        f.write(json.dumps(found_followers))
        f.close()
    else:
        return found_followers


def getTopFollowers(foundFollowers=None, user_count=100, source=None):
    '''Returns a sorted list, based on number of user followers. List default
    size is 100, but can be changed with argument. Source for user data can be
    file or list of user objects.'''
    if source:
        logger.debug("Retrieving follower data from file, %s" % source)
        f = open(source, 'r')
        results = json.loads(f.read())
        logger.debug("Data loaded from file.")
        f.close()
    else:
        results = foundFollowers
    followers = []
    logger.debug("Sorting list of %d users" % len(results))
    for result in results:
        for user in result.get('users'):
            followers.append((user.get('followers_count'), user.get('screen_name')))
    followers = sorted(followers, key=itemgetter(0), reverse=True)
    logger.debug("Returning %d users with most followers." % user_count)
    return followers[:user_count]


def followUsers(users):
    '''Given list of users (screen_name) will be followed.'''
    for user in users:
        logger.info("Following: %s" % user[1])
        twitter_api.friendships.create(screen_name=user[1], follow=False)


def main():
    followers = getFollowers('GordonRamsay')
    topFollowers = getTopFollowers(followers)
    followUsers(topFollowers)

if __name__ == '__main__':
    main()
