# -*- coding:utf-8 -*-
from dateutil import parser

import db
from log import logger
from models import Tweet
from twitterConnection import TwitterStream


def storeTimeline():
    logger.info('Starting to store timeline data')
    twitter_stream = TwitterStream(domain='userstream.twitter.com')
    db.init_db()
    for msg in twitter_stream.stream.user(following=True):
        if not msg.get('friends'):
            tweet = Tweet()
            tweet.text = msg['text'].encode('utf-8')
            tweet.created_at = parser.parse(msg['created_at']).replace(tzinfo=None)
            if msg.get('coordinates'):
                tweet.lat = msg['coordinates']['coordinates'][0]
                tweet.lon = msg['coordinates']['coordinates'][1]
            tweet.tweet_id = msg['id']
            tweet.retweet_count = msg['retweet_count']
            tweet.user_id = msg['user']['id']
            db.session.add(tweet)
            db.session.commit()
