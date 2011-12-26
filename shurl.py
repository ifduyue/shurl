#!/usr/bin/env python
#-*- coding: utf-8 -*-

import bottle
bottle._HTTP_STATUS_LINES[422] = '422 Unprocessable Entity'
from bottle import *
from lib import *
import conf
import urlparse
    
@get('/')
@get('/index.html')
@view('index.html')
def index():
    urls = get_recent_urls(50)
    urls = [(base62_encode(i['_id']), i['url']) for i in urls] 
    url_count = get_url_count()
    return dict(urls=urls, url_count=url_count)


@post('/')
def root():
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
    ret = is_url_exists(url)
    if ret:
        ret = ret['_id']
    else:
        ret = new_url(url) or abort(500, '...kao!')
    uid = base62_encode(ret)
    raise HTTPResponse("", status=201, header=dict(Location="http://%s/%s"%(conf.DOMAIN, uid)))
    

@get('/:uid')
def url(uid):
    try:
        _id = base62_decode(uid)
    except:
        raise HTTPResponse("invalid uid", status=403)
    url = get_url(_id)
    if url:
        raise HTTPResponse("", status=302, header=dict(Location=url))
    raise HTTPResponse("uid not found", status=404)

if __name__ == '__main__':
    import sys
    try:
        port = int(sys.argv[1])
    except: port = 1234
    run(server=GeventServer, host='127.0.0.1', port=port, quiet=True, fast=True)

