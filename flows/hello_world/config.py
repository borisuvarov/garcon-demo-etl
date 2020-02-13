"""Config file."""

import os

import redis

ENVIRONMENT = os.environ.get('Environment', 'dev')
FEED_NAME = 'hello_world_etl'

redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
