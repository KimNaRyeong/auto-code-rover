import re
from django.utils.dateparse import parse_time

def test_parse_time():
    try:
        # Test case 1: trailing whitespace
        result = parse_time('0:5: ')
        assert not isinstance(result, datetime.time), "Expected ValueError but got {}".format(result)
        
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

def print_stacktrace(e: Exception):
    import traceback    
    import sys    
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

if __name__ == "__main__":
    import datetime
    test_parse_time()
