# -*- coding:utf-8 -*-
from operator import itemgetter
from random import randrange
import time

import analysis
import config
from log import logger
from tweets import getTweets


def main():
    try:
        logger.info('Starting retweet script')
        # Get tweets
        tweets = getTweets(config.TWEET_LIKES)
        # Analyze tweets
        analyzed = []
        for tweet in tweets:
            analyzed.append((analysis.sentiment(tweet.get('text')),
                             tweet.get('id')
                             )
                            )
        analyzed = sorted(analyzed, key=itemgetter(0), reverse=True)
        # Retweet the most positive tweet
        tweet = analyzed[0][1]
        tweets.reTweet(tweet)
        logger.info(
            'Retweeting tweet_id: %s, with sentiment %s ' % (
                analyzed[0][1], analyzed[0][0]))
    except Exception, err:
        logger.error('%s: %s' % (Exception, err))

if __name__ == '__main__':
    main()
