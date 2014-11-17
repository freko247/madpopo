# -*- coding: utf-8 -*-
'''Script for retweeting and favoriting tweets containing the pre-defined
hashtags'''
import datetime
import os
from time import sleep

from twitterConnection import TwitterStream
from tweets import reTweet, favorite
import db
from models import ReTweet
from log import logger

BOTS = ['matsie_at_dtu',
        'hybrishybris',
        'AndrenatorC',
        'CPH_Startup',
        'LakerolIs',
        'FitVeganGirl_',
        'RichardsIndie',
        'TheRexyGuy',
        'AxelCyrilian',
        'Where_is_JB_now',
        'henrikholm89',
        '2787613616',
        'Pralesworth',
        'RealAndersDuck',
        'AlyciaGerald',
        'jsmth_t',
        'zakflanigan',
        'hirihiker',
        'SirZenji',
        'meetjamesmet',
        'madpopo79',
        'cj_hitower',
        'THINKDEEPYO',
        'JackBoHorseMan',
        'Timmy_abroad',
        'SuperRexy',
        'ioapsy',
        'Shtinoehh',
        'SimonWJorgensen',
        'marcussor',
        'clintcrock',
        'zoesprings',
        'neergdave',
        'AnnasHollywood',
        'sonia_manning',
        'canuckWong',
        'sapiezynski',
        'ericfullhammer',
        'ethanwoods88',
        ]

TAGS = [(datetime.date(2014, 11, 13), '#madpopo79'),
        (datetime.date(2014, 11, 14), '#getyourflushot'),
        (datetime.date(2014, 11, 17), '#highfiveastranger'),
        ]


def main():
    logger.info('Starting interventions retweeting (pid %s)' % os.getpid())
    twitter_stream = TwitterStream(domain='stream.twitter.com', app=1)
    db.init_db()
    while 1:
        for tag_date, tag in TAGS:
            retweets = 0
            while tag_date == datetime.datetime.now().date():
                try:
                    for status in twitter_stream.stream.statuses.filter(
                            track=tag):
                        sleep(5)
                        tweet_id = status.get('id_str')
                        retweet_ids = [tweet.tweet_id for
                                       tweet in
                                       db.session.query(ReTweet).all()]
                        if tweet_id in retweet_ids:
                            continue
                        screen_name = status.get('user').get('screen_name')
                        # Retweet 10 first
                        if retweets < 10:
                            reTweet(tweet_id)
                            logger.info('Retweeted: %s' % tweet_id)
                            retweets += 1
                        # Retweet 50 if not BOT
                        elif (retweets <= 50
                              and screen_name not in BOTS):
                            reTweet(tweet_id)
                            logger.info('Retweeted: %s' % tweet_id)
                            retweets += 1
                        # Favorite tweet
                        favorite(tweet_id)
                        if (tag_date != datetime.datetime.now().date()):
                            break
                except:
                    print 'Stream connection timeout, restarting...'


if __name__ == '__main__':
    main()
