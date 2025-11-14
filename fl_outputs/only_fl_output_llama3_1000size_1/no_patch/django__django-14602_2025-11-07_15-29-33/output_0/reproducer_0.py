import datetime
from django.utils.dateparse import parse_time

def reproduce_issue():
    try:
        time = parse_time('0:5:')
        assert False, "Expected ValueError"
    except Exception as e:
        print_stacktrace(e)
        raise SystemExit(0)

if __name__ == "__main__":
    reproduce_issue()
