# -*- coding:utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float

Base = declarative_base()


class Tweet(Base):
    '''Table, that stores following information about tweet:
    ["text"],
    ["coordinates"] -> [lon][lat],
    ["retweet_count"],
    ["id"],
    ["created_at"],
    ["user"]["id"].'''
    __tablename__ = "tweet"
    id = Column(Integer, primary_key=True)
    text = Column(String(length=500))
    lon = Column(Float())
    lat = Column(Float())
    retweet_count = Column(Integer())
    tweet_id = Column(String(20))
    created_at = Column(DateTime)
    user_id = Column(String(20))
