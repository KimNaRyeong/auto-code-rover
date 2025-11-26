import django.utils.dateparse
from datetime import datetime

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

def test_iso8601_parsing():
    valid_datetime_string = "2012-04-23T10:20:30.400 -02"
    try:
        parsed_datetime = django.utils.dateparse.parse_datetime(valid_datetime_string)
        assert parsed_datetime is not None, f"Failed to parse {valid_datetime_string}"
        print(f"Parsed datetime: {parsed_datetime}")
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue is present")

if __name__ == "__main__":
    test_iso8601_parsing()
