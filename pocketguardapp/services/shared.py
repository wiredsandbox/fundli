from pyrfc3339 import parse


def parse_datetime(date: str):
    """
    parse_datetime returns a datetime object from a string.
    It parses time of the form: 2009-01-01T14:01:02-04:00
    """
    try:
        return parse(date)
    except ValueError:
        return None
