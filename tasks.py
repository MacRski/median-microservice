"""Redis tasks for median-microservice."""
from itertools import izip
import numpy

from worker import redis_conn


def calculate_median():
    """Return the median of all integer keys stored in redis."""
    keys = [
        key
        for key in redis_conn.scan_iter(match='int:*')
    ]
    counts = redis_conn.mget(keys)
    key_list = []
    if keys:
        for key, count in izip(keys, counts):
            if count is None:
                count = '1'
            key_list.extend([int(key[4:]) for i in range(int(count))])
        return numpy.median(numpy.array(key_list))
    return 0
