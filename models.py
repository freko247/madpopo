# -*- coding:utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean

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


class User(Base):
    ''' Stores user information
    '''
    __tablename__ = 'user'
    activity = Column(Float())          # tweet_frequency
    favorited = Column(DateTime)        # Date when user was 'the favorite'
    followed = Column(DateTime)         # Date when user was followed
    followed_back = Column(DateTime)    # Date when user followed back
    followers_count = Column(Integer())       # number of followers_count
    friends_count = Column(Integer())         # number of friends_count
    join_date = Column(DateTime)        # User join date
    language = Column(Integer())        # lang
    statuses_count = Column(Integer())          # statuses_count
    unfollowed = Column(DateTime)         # Date when user was followed
    user_id = Column(String(20), primary_key=True)
    contributors_enabled = Column(Boolean())
    created_at = Column(DateTime())
    default_profile = Column(Boolean())
    default_profile_image = Column(Boolean())
    description = Column(String(1000))
    favourites_count = Column(Integer())
    follow_request_sent = Column(Boolean())
    following = Column(Boolean())
    geo_enabled = Column(Boolean())
    is_translator = Column(Boolean())
    listed_count = Column(Integer())
    location = Column(String(200))
    name = Column(String(200))
    profile_background_color = Column(String(6))
    profile_background_image_url = Column(String(200))
    profile_background_image_url_https = Column(String(200))
    profile_background_tile = Column(Boolean())
    profile_banner_url = Column(String(200))
    profile_image_url = Column(String(200))
    profile_image_url_https = Column(String(200))
    profile_link_color = Column(String(6))
    profile_sidebar_border_color = Column(String(6))
    profile_sidebar_fill_color = Column(String(6))
    profile_text_color = Column(String(6))
    profile_use_background_image = Column(Boolean())
    protected = Column(Boolean())
    screen_name = Column(String(200))
    show_all_inline_media = Column(Boolean())
    # status = Column(String(500))
    # statuses_count  # Update exisisting
    time_zone = Column(String(200))
    url = Column(String(200))
    utc_offset = Column(Integer())
    verified = Column(Boolean())
    withheld_in_countries = Column(Boolean())
    withheld_scope = Column(Boolean())
    no_retweets = Column(Integer())
    no_retweeted = Column(Integer())
    avg_no_replies = Column(Float())
    avg_no_mentions = Column(Float())


class Language(Base):
    '''Language lookup table'''
    __tablename__ = "language"
    id = Column(Integer(), primary_key=True)
    language = Column(String(5))


class ReTweet(Base):
    '''Table of retweets'''
    __tablename__ = 'retweet'
    tweet_id = Column(String(20), primary_key=True)
    retweet_date = Column(DateTime)
    sentiment = Column(Float)


class Status(Base):
    '''Table, that stores status updates:'''
    __tablename__ = "status"
    created_at = Column(DateTime)
    lat = Column(Float())
    lon = Column(Float())
    status_id = Column(String(20), primary_key=True)
    text = Column(String(length=500))
    source_id = Column(String(50))
