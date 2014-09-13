# -*- coding: utf-8 -*-
import logging
import os

# Create logger
logger = logging.getLogger('madpopo')
logger.setLevel(logging.DEBUG)

# Create log handlers and set log level
hdlr = logging.FileHandler(os.getcwd() + '/madpopo.log')
hdlr.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)

# Add formatting
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
ch.setFormatter(formatter)

# Add handlers
logger.addHandler(hdlr)
logger.addHandler(ch)
