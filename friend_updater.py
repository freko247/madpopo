# -*- coding:utf-8 -*-
import friends
from log import logger


def main():
    logger.info('Starting friend updater.')
    friends_list = friends.getFriends()
    friends.update_friends(friends_list)


if __name__ == '__main__':
    main()
