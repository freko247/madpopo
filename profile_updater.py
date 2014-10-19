# -*- coding:utf-8 -*-
'''Script fpr updating user settings'''
from twitterConnection import twitter_api
import config
from log import logger


def main():
    twitter_api.account.update_profile(
        location=config.TWEET_LOCATION,
        name=config.TWEET_USER_NAME,
        description=config.TWEET_USER_DESCRIPTION)
    logger.info(
        'Updated user - '
        'Location: %s '
        'Name: %s '
        'Description: %s '
        % (config.TWEET_LOCATION,
           config.TWEET_USER_NAME,
           config.TWEET_USER_DESCRIPTION))

if __name__ == '__main__':
    main()
