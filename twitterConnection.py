# -*- coding:utf-8 -*-
from time import sleep

import twitter

import config

auth = twitter.oauth.OAuth(config.OAUTH_TOKEN, config.OAUTH_TOKEN_SECRET,
                           config.CONSUMER_KEY, config.CONSUMER_SECRET)

twitter_api = twitter.Twitter(auth=auth)


class TwitterStream():

    """Class for creating differrent stream connections"""

    def __init__(self, domain, app=None):
        stream_auth = None
        if app:
            credentials = config.OAUTH[app]
            stream_auth = twitter.oauth.OAuth(
                credentials.get('OAUTH_TOKEN'),
                credentials.get('OAUTH_TOKEN_SECRET'),
                credentials.get('CONSUMER_KEY'),
                credentials.get('CONSUMER_SECRET')
            )
        self.stream = twitter.TwitterStream(
            domain=domain, auth=stream_auth or auth)


def get_api_connection(app):
    credentials = config.OAUTH[app]
    auth = twitter.oauth.OAuth(
        credentials.get('OAUTH_TOKEN'),
        credentials.get('OAUTH_TOKEN_SECRET'),
        credentials.get('CONSUMER_KEY'),
        credentials.get('CONSUMER_SECRET')
    )
    return twitter.Twitter(auth=auth)


def connection_rotator(method):
    '''API connection rotator, makes sure that application limits aren't
    exceeded'''
    methods = {'friends.ids': ['resources',
                               'friends',
                               '/friends/ids',
                               'remaining'
                               ],
               'users.lookup': ['resources',
                                'users',
                                '/users/lookup',
                                'remaining'
                                ],
               'search.tweets': ['resources',
                                 'search',
                                 '/search/tweets',
                                 'remaining'
                                 ],
               'statuses.user_timeline': ['resources',
                                          'statuses',
                                          '/statuses/user_timeline',
                                          'remaining'
                                          ],
               }
    api_limits = []
    while 1:
        for i in range(len(config.OAUTH)):
            api_limit = get_api_connection(i).application.rate_limit_status()
            for level in methods.get(method):
                api_limit = api_limit.get(level)
            if api_limit > 0:
                return get_api_connection(i), api_limit
        print 'All apis sleeping...'
        sleep(60)
