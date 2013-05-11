from datetime import datetime
from datetime import timedelta


def perdelta(start, end, delta):
    curr = start
    while curr < end:
        yield curr
        curr += delta


def sliced_time(
    start_hour=None,
    end_hour=None,
    slice_hour=None,
    shift=False
):
    """
    Slicing the time

    Default settings:
    * Start Hour = 8
    * End Hour = 18
    * Slice Hour by 40
    """
    if start_hour is None:
        start_hour = 8
    if end_hour is None:
        end_hour = 18
    if slice_hour is None:
        slice_hour = (end_hour-start_hour)*4

    current_date = datetime.now()
    start_date = current_date.replace(
        hour=start_hour,
        minute=0,
        second=0,
        microsecond=0
    )
    end_date = current_date.replace(
        hour=end_hour,
        minute=0,
        second=0,
        microsecond=0
    )
    difference = end_date - start_date
    sliced_by = timedelta(seconds=difference.total_seconds()/slice_hour)
    end_date = end_date + sliced_by
    if shift is True:
        start_date = start_date + sliced_by
        end_date = end_date + sliced_by
    return (result for result in perdelta(start_date, end_date, sliced_by))
