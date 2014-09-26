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
