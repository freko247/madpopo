# -*- coding:utf-8 -*-
import datetime
from operator import itemgetter
from random import randrange
from time import sleep

import analysis
import config
import db
from log import logger
from models import ReTweet
from tweets import getTweets, reTweet


INITIAL_SLEEP_MAX = 15
RETWEET_COUNT_MAX = 3
TWEET_SLEEP_MAX = 5


def main():
    try:
        first_sleep = randrange(INITIAL_SLEEP_MAX)
        logger.info('Starting retweet script, but first sleeping %d minutes'
                    % first_sleep)
        sleep(60*first_sleep)
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
        # Retweet the most positive tweets
        retweet_count = randrange(RETWEET_COUNT_MAX)
        logger.info('Retweeting %d tweets' % retweet_count)
        for i in range(retweet_count):
            tweet = analyzed[i]
            reTweet(tweet[1])
            new_retweet = ReTweet()
            new_retweet.tweet_id = tweet[1]
            new_retweet.sentiment = tweet[0]
            new_retweet.retweet_date = datetime.datetime.now()
            db.session.add(new_retweet)
            db.session.commit()
            sleep_time = randrange(TWEET_SLEEP_MAX)
            logger.info(
                'Retweeting %d/%d tweet_id: %s, with sentiment %s and sleeping'
                ' for %d minutes' % (i+1,
                                     retweet_count,
                                     analyzed[0][1],
                                     analyzed[0][0],
                                     sleep_time))
            sleep(60*sleep_time)
    except Exception, err:
        logger.error('%s: %s' % (Exception, err))

if __name__ == '__main__':
    main()
