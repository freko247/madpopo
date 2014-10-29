# -*- coding:utf-8 -*-
from random import randrange
from urllib2 import urlopen

import db
from log import logger
from models import Status
from twitterConnection import twitter_api
from tweets import updateStatus

USER = 'Bistro_BarBelow'


def generate_text():
    verbs = ['#Renovating is',
             'Working with this is',
             'Doing some #hardwork is',
             'Making progress with the renovation is',
             'Reaching a new milestone is',
             'Painting, sanding and all that stuff is',
             'Getting down and dirty is',
             'Working with contractors is',
             ]
    adjectives = ['#fun',
                  '#awesome',
                  '#grand',
                  '#epic',
                  '#amazing',
                  '#tiresomebutrewarding',
                  '#crazy',
                  ]
    tags = ['#renovating',
            '#comingsoon',
            '#restaurant',
            '#SanFrancisco',
            '#NewInSF',
            '#decorating',
            '#colours',
            '#design',
            '#comingsoon',
            '#history',
            '#refurbishment',
            ]
    generated_text = verbs[randrange(len(verbs))]
    generated_text += ' ' + adjectives[randrange(len(adjectives))]
    for i in range(randrange(1, 4)):
        tag = tags[randrange(len(tags))]
        if tag.lower() not in generated_text.lower():
            generated_text += ' ' + tag
    if len(generated_text) > 140:
        generated_text = generate_text()
    return generated_text


def main():
    '''Script is used to post an '''
    try:
        logger.info('Starting post renovation progress script')
        tweets = twitter_api.statuses.user_timeline(screen_name=USER,
                                                    count=200
                                                    )
        filtered_tweets = []
        for tweet in tweets:
            text = tweet.get('text')
            if ('#renovation' in text
                    or '#comingsoon' in text
                    or '#refurbishment' in text):
                if tweet.get('entities').get('media'):
                    for media in tweet.get('entities').get('media'):
                        filtered_tweets.append(tweet)
        # TODO: Check with previous tweets...
        db.init_db()
        filtered_statuses = db.session.query(Status).all()
        # source ids of previously posted statuses
        filtered_statuses = [status.source_id for status in filtered_statuses
                             if status.source_id]
        # ids of found tweets
        filtered_tweet_ids = [tweet.get('id_str') for tweet in filtered_tweets]
        # Removing previously posted source tweets
        possible_statuses = [tweet_id for tweet_id in filtered_tweet_ids
                             if tweet_id not in filtered_statuses]
        # Setting the new tweet id, to the newest possible one
        possible_statuses = sorted(possible_statuses)
        if possible_statuses:
            new_source_id = possible_statuses[0]
        # Getting the source tweet
        new_source = [tweet for tweet in filtered_tweets
                      if tweet.get('id_str') == new_source_id][0]
        # TODO: Find next image to post
        medias = new_source.get('entities').get('media')
        media_url = None
        for media in medias:
            media_url = media.get('media_url')
            break
        image = urlopen(media_url)
        params = {"media[]": image.read(),
                  "status": generate_text(),
                  'location': 'work',
                  'source_id': new_source_id
                  }
        # Post tweet
        updateStatus(params)
    except Exception, err:
        logger.error('%s: %s' % (Exception, err))


if __name__ == '__main__':
    main()
