import django.utils.dateparse
from datetime import datetime

def reproduce_issue():
    try:
        dt = django.utils.dateparse.parse_datetime("2012-04-23T10:20:30.400 -02")
        if dt is None:
            raise AssertionError("Expected a valid datetime object, but got None")
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    reproduce_issue()
