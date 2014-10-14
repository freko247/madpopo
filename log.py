# -*- coding: utf-8 -*-
import logging
import os
import sys

# Create logger
logger = logging.getLogger('madpopo')
logger.setLevel(logging.DEBUG)

# Create log handlers and set log level
pathname = os.path.dirname(sys.argv[0])
path = os.path.abspath(pathname)
hdlr = logging.FileHandler(path + '/madpopo.log')
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
