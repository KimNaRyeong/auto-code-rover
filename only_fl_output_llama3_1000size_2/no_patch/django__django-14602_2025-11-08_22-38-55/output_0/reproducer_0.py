import datetime
from django.utils.dateparse import parse_time

def test_parse_time():
    try:
        result = parse_time('0:5:')
        assert False, "Expected ValueError"
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    test_parse_time()
