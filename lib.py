import conf
from psycopg2_pool import PostgresConnectionPool
from base62 import base62_encode

pool = PostgresConnectionPool(conf.psql_db, maxsize=3)
 
def get_url_count():
    count = pool.fetchone("select last_value from shurl_id_seq;")
    return count[0]

def get_url_by_uid(uid):
    ret = pool.fetchone("select url from shurl where id = %s limit 1;", (uid,))
    if ret:
        return ret[0]
    return None

def get_uid_by_url(url):
    ret = pool.fetchone("select id from shurl where url = %s limit 1;", (url,))
    if ret:
        return base62_encode(ret[0])
    return None

def shorten_url(url):
    ret = pool.fetchone("insert into shurl (url) values (%s) returning id;", (url,))
    if ret:
        uid = base62_encode(ret[0])
    else:
        uid = None

    return uid

