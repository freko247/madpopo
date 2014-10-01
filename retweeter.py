# -*- coding:utf-8 -*-
from operator import itemgetter
from random import randrange
import time

import analysis
import config
from log import logger
import tweets


def main():
    try:
        logger.info('Starting retweet script')
        # Get tweets
        searches = tweets.getTweets(config.TWEET_LIKES)
        # Analyze tweets
        analyzed = []
        for msgs in searches:
            for status in msgs.get('statuses'):
                analyzed.append((analysis.sentiment(status.get('text')),
                                 status.get('id')))
        analyzed = sorted(analyzed, key=itemgetter(0), reverse=True)
        # Retweet the most positive tweet
        tweet = analyzed[0][1]
        tweets.reTweet(tweet)
        logger.info('%s, retweeting tweet_id: %s, with sentiment %s ' % (i+1, tweet[1], tweet[0]))
    except Exception, err:
        logger.error('%s: %s' % (Exception, err))

if __name__ == '__main__':
    main()
