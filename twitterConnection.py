# -*- coding:utf-8 -*-
import twitter
import config

auth = twitter.oauth.OAuth(config.OAUTH_TOKEN, config.OAUTH_TOKEN_SECRET,
                           config.CONSUMER_KEY, config.CONSUMER_SECRET)

twitter_api = twitter.Twitter(auth=auth)


class TwitterStream():

    """Class for creating differrent stream connections"""

    def __init__(self, domain, auth=auth, ):
        self.stream = twitter.TwitterStream(domain=domain, auth=auth)


def get_api_connection(app):
    credentials = config.OAUTH[app]
    auth = twitter.oauth.OAuth(
        credentials.get('OAUTH_TOKEN'),
        credentials.get('OAUTH_TOKEN_SECRET'),
        credentials.get('CONSUMER_KEY'),
        credentials.get('CONSUMER_SECRET')
    )
    return twitter.Twitter(auth=auth)
