#!/usr/bin/env python
#-*- coding: utf-8 -*-

import bottle
bottle._HTTP_STATUS_LINES[422] = '422 Unprocessable Entity'
from bottle import *
from lib import *
import conf
import pylru
import urlparse
url_cache = pylru.lrucache(conf.CACHE_SIZE)
hash_cache = pylru.lrucache(conf.CACHE_SIZE)
    
@get('/')
@get('/index.html')
@view('index.html')
def index():
    global url_cache
    urls = [] 
    for uid in url_cache:
        urls.append((uid, url_cache.peek(uid)))
        if len(urls) == 50: break
    url_count = get_url_count()
    return dict(urls=urls, url_count=url_count)


@post('/')
def root():
    global url_cache, hash_cache
    url = request.POST.get('url', '').strip()

    # is valid url ?
    scheme, netloc, path, query, fragment = urlparse.urlsplit(url)
    if len(url) <= 4 or \
       scheme == '' or netloc == '' or \
       netloc.lower().find(conf.DOMAIN) != -1 or \
       scheme not in ('http', 'https', 'ftp'):
        raise HTTPResponse("invalid url", status=422)
        
    if len(url) > 512:
        raise HTTPResponse("url too long", status=422)

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
    raise HTTPResponse("uid not found", status=404)

if __name__ == '__main__':
    import sys
    try:
        port = int(sys.argv[1])
    except: port = 1234
    run(server=GeventServer, host='127.0.0.1', port=port, quiet=True, fast=True)

