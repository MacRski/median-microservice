"""median-microservice Redis queue."""
import os

import redis

from rq import Queue

redis_url = os.environ.get('REDISTOGO_URL', 'redis://redis')

redis_conn = redis.from_url(redis_url)

task_queue = Queue(connection=redis_conn)
