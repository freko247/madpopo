# -*- coding:utf-8 -*-
import datetime
from operator import itemgetter
from random import randrange
import time

import analysis
import config
import db
from log import logger
from models import ReTweet
from tweets import getTweets, reTweet


def main():
    try:
        logger.info('Starting retweet script')
        # Get tweets
        tweets = getTweets(config.TWEET_LIKES)
        # Analyze tweets
        analyzed = []
        db.init_db()
        retweets = [tweet.tweet_id for
                    tweet in db.session.query(ReTweet).all()]
        for tweet in tweets:
            if tweet.get('id_str') not in retweets:
                analyzed.append((analysis.sentiment(tweet.get('text')),
                                 tweet.get('id_str')
                                 )
                                )
        analyzed = sorted(analyzed, key=itemgetter(0), reverse=True)
        # Retweet the most positive tweet
        tweet = analyzed[0]
        reTweet(tweet[1])
        new_retweet = ReTweet()
        new_retweet.tweet_id = tweet[1]
        new_retweet.sentiment = tweet[0]
        new_retweet.retweet_date = datetime.datetime.now()
        db.session.add(new_retweet)
        db.session.commit()
        logger.info(
            'Retweeting tweet_id: %s, with sentiment %s ' % (
                analyzed[0][1], analyzed[0][0]))
    except Exception, err:
        logger.error('%s: %s' % (Exception, err))

if __name__ == '__main__':
    main()
