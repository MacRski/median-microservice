"""Redis task queue for median-microservice."""
import os

import redis
from rq import Worker, Queue, Connection

listen = ['default']

redis_url = os.environ.get('REDISTOGO_URL', 'redis://redis')

redis_conn = redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(redis_conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()
