import datetime
from django.utils.dateparse import parse_time

def reproduce_issue():
    try:
        time_str = '0:5:'
        result = parse_time(time_str)
        assert False, f"Expected ValueError for '{time_str}' but got {result}"
    except Exception as e:
        print_stacktrace(e)
        exit(0)

if __name__ == "__main__":
    reproduce_issue()
