# -*- coding:utf-8 -*-
import config
import db
from followers import followUsers
from log import logger
from models import User
from tweets import getTweets
from twitterConnection import twitter_api


def main():
    logger.info('Starting follow neighbour script')
    try:
        db.init_db()
        lat, lon = config.TWEET_HOME_GEO
        radius = '100km'
        geocode = ','.join([str(lat), str(lon), radius])
        registered_users = [
            user.user_id for user in db.session.query(User).all()]
        results = getTweets([config.TWEET_LOCATION.split(',')[0]],
                            result_type='recent')
        near_tweets = []
        for tweet in results:
            if tweet.get('place'):
                if tweet.get('place').get('full_name') == 'San Francisco, CA':
                    near_tweets.append(tweet)
        near_tweets[0]
        authors = [tweet.get('user') for tweet in near_tweets]
        authors_id_list = set([author.get('id_str') for author in authors])
        follow_list = [author for author in authors_id_list
                       if author not in registered_users]
        logger.info('Found %d  new neighbours' % len(follow_list))
        followUsers(follow_list[:30])
    except Exception, err:
        logger.error('%s: %s' % (Exception, err))


if __name__ == '__main__':
    main()
