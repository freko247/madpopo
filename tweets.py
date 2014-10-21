# -*- coding:utf-8 -*-
from dateutil import parser
import sys
import os
import datetime
from random import randrange

import config
import db
from log import logger
from models import Status, Tweet
from twitterConnection import TwitterStream
from twitterConnection import twitter_api


def storeTimeline():
    while 1:
        try:
            logger.info(
                'Starting to store timeline data (pid %s)' % os.getpid())
            twitter_stream = TwitterStream(domain='userstream.twitter.com')
            db.init_db()
            for msg in twitter_stream.stream.user(following=True):
                if msg.get('text'):
                    tweet = Tweet()
                    tweet.text = msg['text'].encode('utf-8')
                    tweet.created_at = parser.parse(
                        msg['created_at']).replace(tzinfo=None)
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


def getTweets(query, until=None, result_type='popular'):
    tweets = []
    today = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
    lat, lon = config.TWEET_HOME_GEO
    radius = config.TWEET_RETWEET_RADIUS
    geocode = ','.join([str(lat), str(lon), radius])
    for term in query:
        logger.debug('Getting popular tweets about: %s' % term)
        results = twitter_api.search.tweets(q=term,
                                            lang='en',
                                            result_type=result_type,
                                            count=100,
                                            until=until or today,
                                            geocode=geocode,
                                            )
        tweets += results.get('statuses')
    return tweets


def reTweet(id):
    twitter_api.statuses.retweet(id=id)


def updateStatus(text, geo=False, location='home'):
    db.init_db()
    statuses = db.session.query(Status).all()
    logger.info('Number od statuses: %d' % len(statuses))
    if text in [status.text for status in statuses]:
        logger.info('Duplicate status')
        return
    lat = None
    lon = None
    locations = {
        'home': config.TWEET_HOME_GEO,
        'work': config.TWEET_WORK_GEO,
        }
    if isinstance(location, basestring):
        # Somewhat randomize location
        lat = locations.get(location)[0]+(0.00001 * randrange(150))
        lon = locations.get(location)[1]+(0.00001 * randrange(150))
    elif location:
        lat = location[0]
        lon = location[1]
    status_data = twitter_api.statuses.update(
        status=text,
        lat=lat,
        long=lon,
        possibly_sensitive=True,)
    new_status = Status()
    new_status.status_id = status_data.get('id_str')
    new_status.created_at = parser.parse(
        status_data.get('created_at')).replace(tzinfo=None)
    new_status.lat = lat
    new_status.lon = lon
    new_status.text = text
    db.session.merge(new_status)
    db.session.commit()
    logger.info('Tweeted: %s' % text)


def main():
    storeTimeline()

if __name__ == '__main__':
    main()
