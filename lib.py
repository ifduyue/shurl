#!/usr/bin/env python
import conf
import os
import hashlib

def writeto(path, data):
    d = os.path.dirname(path)
    #if not os.path.isdir(d):
    try:
        os.makedirs(d)
    except: pass
    if os.path.exists(path):
        print path
    fh = open(path, 'w')
    fh.write(data)
    fh.close()
    
def readfrom(path):
    try:
        with open(path, 'r') as f:
            return f.read()
    except: pass
    return None

def appendto(path, data):
    fh = open(path, 'a+')
    fh.write(data)
    fh.close()

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

def sha256(s):
    return hashlib.sha256(s).hexdigest()

