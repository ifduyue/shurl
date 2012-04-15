import os

CACHE_SIZE = 1000
ROOT_DIR = os.path.realpath(os.path.dirname(__file__))
DATA_DIR = os.path.join(ROOT_DIR, 'data')
URL_DIR = os.path.join(DATA_DIR, 'url')
HASH_DIR = os.path.join(DATA_DIR, 'hash') 
LOCK_FILE = os.path.join(DATA_DIR, 'lock')
UID_FILE = os.path.join(DATA_DIR, 'uid')
DOMAIN = 'shurl.im'

psql_db = 'dbname=shurl user=postgres password=nicai'
