import datetime


def dispatch_date(kwargs):
    return kwargs['day'], kwargs['month'], kwargs['year']


def get_current_month() -> datetime.date:
    now = datetime.datetime.now()
    return now
