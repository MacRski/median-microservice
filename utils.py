"""Utility functions for median-microservice."""
from datetime import timedelta
from time import mktime


def convert_datetime_to_unix_timestamp(datetime_instance):
    """Convert a datetime instance to a valid unix timestamp."""
    return int(mktime(datetime_instance.timetuple()))


def build_unix_daterange_from_end(end_datetime, **timedelta_kwargs):
    """
    Return a generator of unix timestamps within a given range.

    The range ends on `end_datetime` and begins at a timestamp dictated
    by working backwards as far as a timedelta instance constructed from
    `timedelta_kwargs`.

    Examples:
    >>> from datetime import datetime
    # All unix time stamps from one minute in the past until now.
    >>> example_1 = build_unix_daterange(datetime.now(), minutes=1)
    # All unix time stamps from an hour and 35 minutes in the past until now.
    >>> example_2 = build_unix_daterange(datetime.now(), hours=1, minutes=35)
    """
    td = timedelta(**timedelta_kwargs)
    start_datetime = end_datetime - td
    return range(
        convert_datetime_to_unix_timestamp(start_datetime),
        convert_datetime_to_unix_timestamp(end_datetime) + 1
    )
