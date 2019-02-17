import calendar
from datetime import datetime


def utc_now_to_timestamp(datetime_string):
    time = datetime.strptime(datetime_string, "%Y-%m-%d %H:%M:%S")
    return calendar.timegm(time.timetuple())


# date changer
def change_date_format(date, format):
    """Returns adequate date format for chart representation"""
    return datetime.strptime(date, "%Y-%m-%d %H:%M:%S").strftime(format)

