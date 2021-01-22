import datetime
import datetime as dt

from app.const import POST_DATE_FORMAT


def dispatch_date(kwargs):
    return kwargs['day'], kwargs['month'], kwargs['year']


def get_today() -> dt.date:
    return dt.datetime.today()


def generate_dates_list(start, end):
    date_range = end - start
    dates = []
    for days in range(date_range.days + 1):
        dates.append(start + dt.timedelta(days))
    return dates


def get_time_boundaries(post):
    if 'since' in post and 'until' in post:
        since = datetime.datetime.strptime(post['since'], POST_DATE_FORMAT)
        until = datetime.datetime.strptime(post['until'], POST_DATE_FORMAT)
        return since, until
    else:
        return find_thirty_days_ago_and_today()


def find_thirty_days_ago_and_today():
    until = get_today()
    since = until - datetime.timedelta(days=30)
    return since, until
