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


class Users(Base):
    ''' Stores user information
    activity = Tweet frequency
    followed = Date when user was followed
    followed_back = Date when user followed back
    followers = Number of followers_count
    friends = Number of friends_count
    join_date = User join date
    language = User language
    tweets = Tweet count
    user_id = User id
    '''
    activity = Column(Float())          # tweet_frequency
    followed = Column(DateTime)         # Date when user was followed
    followed_back = Column(DateTime)    # Date when user followed back
    followers = Column(Integer())       # number of followers_count
    friends = Column(Integer())         # number of friends_count
    join_date = Column(DateTime)        # User join date
    language = Column(Integer())        # lang
    tweets = Column(Integer())          # statuses_count
    user_id = Column(Integer, primary_key=True)


class Language(Base):
    '''Language lookup table'''
    id = Column(Integer(), primary_key=True)
    language = Column(String(5))
