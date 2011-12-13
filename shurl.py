#!/usr/bin/env python
#-*- coding: utf-8 -*-

import bottle
bottle._HTTP_STATUS_LINES[422] = '422 Unprocessable Entity'
from bottle import *
from lib import *
from base62 import *
import conf
import pylru
import urlparse
from filelock import FileLock as lock
url_cache = pylru.lrucache(conf.CACHE_SIZE)
hash_cache = pylru.lrucache(conf.CACHE_SIZE)

def get_next_uid():
    uid = None
    with lock(conf.LOCK_FILE):
        uid = readfrom(conf.UID_FILE)
        if uid is None: uid = 1
        uid = int(uid)
        writeto(conf.UID_FILE, str(uid+1))
        uid = base62_encode(uid)
    return uid
    
@get('/')
@get('/index.html')
def index():
    return 'curl -i http://shurl.im/ -F "url=http://lyxint.com/"'

@post('/')
def root():
    global url_cache, hash_cache
    url = request.POST.get('url', '').strip()

    # is valid url ?
    scheme, netloc, path, query, fragment = urlparse.urlsplit(url)
    if len(url) <= 4 or scheme == '' or netloc == '' or  netloc.lower().find(conf.DOMAIN) != -1:
        #abort(422, 'invalid url')
        raise HTTPResponse("invalid url", status=422)

    # check whether this url exists
    hash = sha256(url)
    uid = None
    if hash in hash_cache:
        uid = hash_cache[hash]
    elif os.path.exists(get_hash_path(hash)):
        uid = readfrom(get_hash_path(hash))
    
    if uid is None:
        uid = get_next_uid() or abort(500, 'cannot get next uid')
        writeto(get_url_path(uid), url)
        writeto(get_hash_path(hash), uid)

    url_cache[uid] = url
    hash_cache[hash] = uid
    raise HTTPResponse("", status=201, header=dict(Location="http://%s/%s"%(conf.DOMAIN, uid)))
    

@get('/:uid')
def url(uid):
    global url_cache
    url = None
    if uid in url_cache:
        url = url_cache[uid]
    else:
        url = readfrom(get_url_path(uid))
    if url:
        url_cache[uid] = url
        raise HTTPResponse("", status=302, header=dict(Location=url))
    abort(404, 'uid not found')

if __name__ == '__main__':
    import sys
    try:
        port = int(sys.argv[1])
    except: port = 1234
    run(server=GeventServer, host='127.0.0.1', port=port, quiet=True, fast=True)

