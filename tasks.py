"""Redis tasks for median-microservice."""
import numpy

from worker import redis_conn


def calculate_median():
    """Return the median of all integer keys stored in redis."""
    key_list = []
    for key in redis_conn.scan_iter(match='int:*'):
        count = redis_conn.get(key)
        if count:
            count = int(count)
            key_list.extend([int(key[4:]) for i in range(int(count))])
    if key_list:
        return numpy.median(numpy.array(key_list))
    return 0
