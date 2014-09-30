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
        # Get tweets
        searches = tweets.getTweets(config.TWEET_LIKES)
        # Analyze tweets
        analyzed = []
        for msgs in searches:
            for status in msgs.get('statuses'):
                analyzed.append((analysis.sentiment(status.get('text')),
                                 status.get('id')))
        analyzed = sorted(analyzed, key=itemgetter(0), reverse=True)
        # Retweet the five most positive tweets
        for i, tweet in enumerate([tweet for tweet in analyzed if tweet[0] > 1][0]):
            print tweet
            tweets.reTweet(tweet[1])
            sleep_minutes = randrange(1, 3)
            time.sleep(60*sleep_minutes)
            logger.info('%s, retweeting tweet_id: %s, with sentiment %s ' % (i+1, tweet[1], tweet[0]))
    except Exception, err:
        logger.error('%s: %s' % (Exception, err))

if __name__ == '__main__':
    main()
