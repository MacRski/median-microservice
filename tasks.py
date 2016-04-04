"""Redis tasks for median-microservice."""
import numpy

from worker import redis_conn


def calculate_median():
    """Return the median of all integer keys stored in redis."""
    keys = redis_conn.scan_iter(match='int:*')
    if keys:
        return numpy.median(numpy.array([int(num[4:]) for num in keys]))
    return 0
