# -*- coding: utf-8 -*-
import logging
import os

logger = logging.getLogger('madpopo')
hdlr = logging.FileHandler(os.getcwd() + '/madpopo.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)
