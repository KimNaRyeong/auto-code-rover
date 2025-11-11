import datetime
from django.utils.dateparse import parse_datetime

def reproduce_issue():
    try:
        datetime_obj = parse_datetime("2012-04-23T10:20:30.400 -02")
        assert datetime_obj is not None, "Expected a valid datetime object"
    except Exception as e:
        print_stacktrace(e)
        raise SystemExit(1)

if __name__ == "__main__":
    reproduce_issue()
