"""Redis tasks for median-microservice."""
import numpy

from utils import build_unix_daterange_from_end
from worker import redis_conn


def calculate_median(end_date, **timedelta_kwargs):
    """
    Return the median of all integers stored in a range ending at `end_date`.

    Range length is dictated by `timedelta_kwargs`.

    Args:
        end_date (datetime.datetime): The end of the range.
        timedelta_kwargs (kwargs): Valid datetime.timedelta constructor kwargs.
    """
    key_list = build_unix_daterange_from_end(end_date, **timedelta_kwargs)
    value_list = []
    for key in key_list:
        value_list.extend([
            int(val)
            for val in redis_conn.lrange(key, 0, -1)
            if val
        ])
    if value_list:
        return numpy.median(numpy.array(value_list))
    return 0
