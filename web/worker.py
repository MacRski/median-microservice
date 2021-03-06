"""Redis task queue for median-microservice."""
from rq import Worker, Queue, Connection

from queue import redis_conn

listen = ['default']

if __name__ == '__main__':
    with Connection(redis_conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()
