import conf
from lib import pool
from base62 import base62_encode
import os

def readfrom(path):
    try:
        with open(path, 'r') as f:
            return f.read()
    except: pass
    return None

def get_uid_count():
    try:
        uid = readfrom(conf.UID_FILE)
        return int(uid) - 1
    except: return 0

def split_path(uid):
    length = len(uid)
    if len(uid) <= 2:
        return os.path.join('_', uid)
    if len(uid) <= 6:
        return os.path.join('__', uid[0], uid[1:3], uid[3:] or uid)
    return os.path.join(uid[0], uid[1:3], uid[3:5], uid[5:])

def get_hash_path(hash):
    return os.path.join(conf.HASH_DIR, split_path(hash))

def get_url_path(uid):
    return os.path.join(conf.URL_DIR, split_path(uid))

if __name__ == '__main__':
    import psycopg2
    count = get_uid_count()
    for i in xrange(1, count+1):
        uid = base62_encode(i)
        path = get_url_path(uid)
        url = readfrom(path)
        try:
            ret = pool.execute("insert into shurl (id, url) values (%s, %s)", (i, url))
            print ret, i, uid, url
        except psycopg2.IntegrityError as e:
            print e

