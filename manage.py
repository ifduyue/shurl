import os
import conf
from lib import *
import optparse
from base62 import base62_encode, base62_decode 

def view(uid):
    path = get_url_path(uid)
    print uid, readfrom(path)

def viewall():
    count = get_url_count()
    for i in xrange(1, count+1):
        view(base62_encode(i))

def delete(uid):
    path = get_url_path(uid)
    url = readfrom(path)
    os.remove(path)
    print 'deleted', path, url


if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option("-a", "--action", dest="action", default="view",
                      help="Which action to perform: [view, viewall, delete]")

    options, args = parser.parse_args()
    
    action = options.action
    action = locals()[action]
    if args:
        for i in args:
            action(i)
    else:
        action()
