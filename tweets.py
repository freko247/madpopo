# -*- coding:utf-8 -*-
from dateutil import parser
import sys
import os
import datetime

import db
from log import logger
from models import Tweet
from twitterConnection import TwitterStream
from twitterConnection import twitter_api


def storeTimeline():
    try:
        logger.info('Starting to store timeline data (pid %s)' % os.getpid())
        twitter_stream = TwitterStream(domain='userstream.twitter.com')
        db.init_db()
        for msg in twitter_stream.stream.user(following=True):
            if msg.get('text'):
                tweet = Tweet()
                tweet.text = msg['text'].encode('utf-8')
                tweet.created_at = parser.parse(msg['created_at']).replace(tzinfo=None)
                if msg.get('coordinates'):
                    tweet.lon = msg['coordinates']['coordinates'][0]
                    tweet.lat = msg['coordinates']['coordinates'][1]
                tweet.tweet_id = msg['id']
                tweet.retweet_count = msg['retweet_count']
                tweet.user_id = msg['user']['id']
                db.session.add(tweet)
                db.session.commit()
        logger.error('Stream timeout or other cause for shutdown')
    except Exception, err:
        logger.error("%s, %s" % (Exception, err))
        raise


def getTweets(filter, until=None):
    searches = []
    today = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
    for query in filter:
        searches.append(twitter_api.search.tweets(q=query,
                                                  lang='en',
                                                  result_type='popular',
                                                  count=15,
                                                  until=until or today
                                                  )
                        )
    return searches


def reTweet(id):
    twitter_api.statuses.retweet(id=id)


def main():
    storeTimeline()


if __name__ == '__main__':
    main()
