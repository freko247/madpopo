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
    __tablename__ = 'user'
    activity = Column(Float())          # tweet_frequency
    favorited = Column(DateTime)        # Date when user was 'the favorite'
    followed = Column(DateTime)         # Date when user was followed
    followed_back = Column(DateTime)    # Date when user followed back
    followers = Column(Integer())       # number of followers_count
    friends = Column(Integer())         # number of friends_count
    join_date = Column(DateTime)        # User join date
    language = Column(Integer())        # lang
    tweets = Column(Integer())          # statuses_count
    unfollowed = Column(DateTime)         # Date when user was followed
    user_id = Column(String(20), primary_key=True)

    # TODO: Below columns are to be added to table
    #       Field descriptions can be found at:
    #       https://dev.twitter.com/overview/api/users
    #       After this file is updated, update 009_Add_all_user_fields
    # contributors_enabled = Column(Boolean())
    # created_at = Column(DateTime())
    # default_profile = Column(Boolean())
    # default_profile_image = Column(Boolean())
    # description = Column(String(1000))
    # entities # Skip this field
    # favourites_count = 
    # follow_request_sent = 
    # following = 
    # followers_count  # Update existing
    # friends_count  # Update existing
    # geo_enabled = 
    # # id  # use existing
    # # id_str  # use existing
    # is_translator = 
    # lang = 
    # listed_count = 
    # location = 
    # name = 
    # notifications = 
    # profile_background_color = 
    # profile_background_image_url = 
    # profile_background_image_url_https = 
    # profile_background_tile = 
    # profile_banner_url = 
    # profile_image_url = 
    # profile_image_url_https = 
    # profile_link_color = 
    # profile_sidebar_border_color = 
    # profile_sidebar_fill_color = 
    # profile_text_color = 
    # profile_use_background_image =  
    # protected = 
    # screen_name = 
    # show_all_inline_media = 
    # status = 
    # statuses_count  # Update exisisting
    # time_zone = 
    # url = 
    # utc_offset = 
    # verified = 
    # withheld_in_countries = 
    # withheld_scope = 


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
