import re
from django.utils.dateparse import parse_time

def test_parse_time():
    # Test case 1: trailing space should not be accepted
    try:
        parse_time('0:5: ')
        assert False, "Trailing space should not be accepted"
    except ValueError:
        pass  # Expected behavior

    # Test case 2: other invalid inputs (add more examples as needed)
    # ...

def main():
    test_parse_time()

if __name__ == "__main__":
    try:
        main()
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
