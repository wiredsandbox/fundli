import datetime


def parse_datetime(date: str):
    try:
        return datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f")
    except ValueError:
        return None
