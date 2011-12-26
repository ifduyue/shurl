#!/usr/bin/env python
import conf
import os
from base62 import *
import pymongo
import datetime

def get_next_uid():
    collection = get_mongodb_shurl_db().uid
    ret = collection.find_and_modify({'_id': 0}, update={'$inc': {'uid': 1}}, upsert=True, new=True) 
    return ret['uid']

def get_url_count():
    collection = get_mongodb_shurl_db().uid
    ret = collection.find_one({'_id': 0})
    return 0 if ret is None else ret.get('uid', 0)

def get_recent_urls(limit=50):
    collection = get_mongodb_shurl_db().url
    ret = collection.find({}, limit=limit, sort=[('visited_at', pymongo.DESCENDING)])
    if ret: return list(ret)
    else: return []

def get_url(_id):
    collection = get_mongodb_shurl_db().url
    ret = collection.find_and_modify({'_id': _id}, {'$set': {'visited_at': datetime.datetime.now()}})
    if ret: return ret.get('url', None)
    return None

def is_url_exists(url):
    collection = get_mongodb_shurl_db().url
    ret = collection.find_one({'url': url})
    return ret

def new_url(url):
    uid = get_next_uid()
    collection = get_mongodb_shurl_db().url
    now = datetime.datetime.now() 
    return collection.insert({'_id': uid, 'url': url, 'created_at': now, 'visited_at': now})

_connection = None
def get_mongodb_connection():
    '''
    # under gevent, this will cause: 
    # AssertionError: ids don't match
    global _connection
    if _connection is None:
        _connection = pymongo.Connection(conf.MONGODB_HOST, conf.MONGODB_PORT)
    return _connection
    '''
    return pymongo.Connection(conf.MONGODB_HOST, conf.MONGODB_PORT)

def get_mongodb_shurl_db():
    c = get_mongodb_connection()
    return c.shurl
