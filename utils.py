import datetime
import pytz


def now():
    datetime_ = format(datetime.datetime.now(pytz.utc), '%Y-%m-%d %H:%M:%S')

    return datetime_
