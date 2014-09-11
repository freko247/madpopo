# -*- coding:utf-8 -*-
import json
import twitter

from operator import itemgetter

import config
from log import logger

CONSUMER_KEY = config.CONSUMER_KEY
CONSUMER_SECRET = config.CONSUMER_SECRET
OAUTH_TOKEN = config.OAUTH_TOKEN
OAUTH_TOKEN_SECRET = config.OAUTH_TOKEN_SECRET

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)

twitter_api = twitter.Twitter(auth=auth)


def getFollowers(destinationFile=None):
    found_followers = []
    for i in range(15):
        cursor = -1
        if len(found_followers) > 0:
            cursor = found_followers[-1].get('next_cursor_str')
        found_followers.append(
            twitter_api.followers.list(screen_name='GordonRamsay',
                                                 count=2000,
                                                 cursor=cursor)
                                                 )
    if destinationFile:
        f = open(destinationFile, 'w')
        f.write(json.dumps(found_followers))
        f.close()
    else:
        return found_followers


def getTopFollowers(foundFollowers=None, user_count=100, source=None):
    if source:
        f = open(source, 'r')
        results = json.loads(f.read())
        f.close()
    else:
        results = foundFollowers
    followers = []
    for result in results:
        for user in result.get('users'):
            followers.append((user.get('followers_count'), user.get('name')))
    followers = sorted(followers, key=itemgetter(0), reverse=True)
    return followers[:100]


def followUsers(users):
    for user in users:
        logger.info("Following: %s" % user[1])
        twitter_api.friendships.create(screen_name=user[1])


def main():
    followers = getFollowers()
    topFollowers = getTopFollowers(followers, source="followers3")
    followUsers(topFollowers)

if __name__ == '__main__':
    main()
