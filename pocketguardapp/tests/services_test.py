import pytz
from datetime import datetime

from pocketguardapp.services.services import parse_datetime

def test_parse_datetime():
    class testCase:
        def __init__(self, timestamp, expected):
            self.timestamp = timestamp
            self.expected = expected

    test_cases = [
            testCase("2020-01-01T00:00:00Z", datetime(2020, 1, 1, 0, 0, 0, tzinfo=pytz.UTC)),
            testCase("2020-01-01T00:00:00-04:00", datetime(2020, 1, 1, 0, 0, 0, tzinfo=pytz.FixedOffset(-240))),
            testCase("2020-01-01T00:00:00+04:00", datetime(2020, 1, 1, 0, 0, 0, tzinfo=pytz.FixedOffset(240))),
            testCase("2020-01-01T00:00:00", None),
            testCase("2020-01-01", None),
            testCase("2020", None),
            testCase("2020-01-01T00:00:00-04:00Z", None),
            testCase("2020-01-01T00:00:00Z-04:00", None),
    ]

    for test_case in test_cases:
        got = parse_datetime(test_case.timestamp)
        assert got == test_case.expected, "expected: {}, got: {}".format(test_case.expected, got)

