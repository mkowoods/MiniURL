import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

import hashlib
import base64

import redis
import json
import logging
import time
import os


#used in place of url for lookups that have no results
REDIS_NULL_TOKEN = 'NULL_TOKEN'
REDIS_ALL_URLS_CACHE_KEY = 'all_urls'

DB_HOST = os.environ['DB_HOST']
REDIS_HOST = os.environ['REDIS_HOST']

print('DB_HOST', DB_HOST, 'REDIS_HOST', REDIS_HOST)

conn_string = 'postgresql://postgres:example@{host}/postgres'.format(host=DB_HOST)
engine = create_engine(conn_string, echo=True)

r = redis.Redis(host=REDIS_HOST, port=6379, db=0)

Base = declarative_base()
Session = sessionmaker(bind=engine)

def get_key(url):
    url = url.encode('utf-8')
    k = base64.b64encode( hashlib.sha256(url).digest())[:20]
    k = k.decode('utf-8')
    k = k.replace('+', '-')
    k = k.replace('/', '_')
    return k


class URL(Base):
    __tablename__ = 'urls'
    key = Column(String(30), primary_key=True)
    url = Column(String(2048))
    created_date = Column(DateTime, default=datetime.datetime.utcnow)

    def to_json(self):
        return {'key': self.key, 'url': self.url}

    def __repr__(self):
        return "<URL(%r, %r, %s)>"%(self.key, self.url, self.created_date)


def get_all_urls():
    if r.exists(REDIS_ALL_URLS_CACHE_KEY):
        return json.loads( r.get(REDIS_ALL_URLS_CACHE_KEY) )
    else:
        session = Session()
        results = [url.to_json() for url in session.query(URL).all()]
        session.close()
        r.set(REDIS_ALL_URLS_CACHE_KEY, json.dumps(results), ex=20)
        return results

def get_by_key(key):

    cache_key = 'key:{key}'.format(key=key)
    if r.exists(cache_key):
        print("#######################")
        print('Hit Cache')
        url = r.get(cache_key).decode('utf-8')
        if url == REDIS_NULL_TOKEN:
            return None
        return url
    else:
        print("#######################")
        print("Hitting Database")
        session = Session()
        u = session.query(URL).get(key)
        session.close()
        url = u.url if u else None
        if url is None:
            print('Test ULR', url)
            r.set(cache_key, REDIS_NULL_TOKEN)
        return url

def safe_commit(session):
    try:
        session.commit()
    except:
        #TODO: Logging
        session.rollback()
    finally:
        session.close()


def add_url(url):
    url = url.strip()
    session = Session()
    key = get_key(url)
    new_url = URL(key=key, url=url)
    session.add(new_url)
    safe_commit(session)

    cache_key = 'key:{key}'.format(key=key)
    r.set(cache_key, url)
    r.delete(REDIS_ALL_URLS_CACHE_KEY)
    time.sleep(0.1) #sleep to avoid race condition
    return {'tag': key, 'url': url}

def delete_by_key(key):
    session = Session()
    url = session.query(URL).get(key)
    session.delete(url)
    safe_commit(session)
    return key


def create_tables():
    Base.metadata.create_all(engine)

    try:
        Session = sessionmaker(bind=engine)
        session = Session()

        if not session.query(URL).get('tmp'):
            print("\n", "############################", "\n")
            print('Seeding tables')
            print("\n", "############################", "\n")

            tmp = URL(key="tmp", url="https://www.google.com")
            tmp2 = URL(key="tmp2", url="https://www.amazon.com")
            session.add_all([tmp, tmp2])
            print(session.new)

            session.commit()

            print("\n", "Query all of URL Database")
            for row in session.query(URL).all():
                print(row)

    except:
        pass