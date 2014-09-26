# -*- coding:utf-8 -*-
from log import logger
from analysis import sentiment
from twitterConnection import TwitterStream


def getTimeline():
    twitter_stream = TwitterStream(domain='userstream.twitter.com')
    for tweet in twitter_stream.stream.user():
        # TODO: Do something with the tweets
        print tweet.get('text')
