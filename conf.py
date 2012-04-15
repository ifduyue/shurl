import os

CACHE_SIZE = 100
ROOT_DIR = os.path.realpath(os.path.dirname(__file__))
DATA_DIR = os.path.join(ROOT_DIR, 'data')
URL_DIR = os.path.join(DATA_DIR, 'url')
HASH_DIR = os.path.join(DATA_DIR, 'hash') 
LOCK_FILE = os.path.join(DATA_DIR, 'lock')
UID_FILE = os.path.join(DATA_DIR, 'uid')
DOMAIN = 'shurl.im'

os.chdir(ROOT_DIR)
if not os.path.isdir(URL_DIR):
    os.makedirs(URL_DIR)
if not os.path.isdir(HASH_DIR): 
    os.makedirs(HASH_DIR)
