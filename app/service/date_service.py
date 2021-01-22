import datetime
import datetime as dt


def dispatch_date(kwargs):
    return kwargs['day'], kwargs['month'], kwargs['year']


def get_current_month() -> datetime.date:
    now = datetime.datetime.now()
    return now


def generate_dates_list(start, end):
    date_range = end - start
    dates = []
    for days in range(date_range.days + 1):
        dates.append(start + dt.timedelta(days))
    return dates
