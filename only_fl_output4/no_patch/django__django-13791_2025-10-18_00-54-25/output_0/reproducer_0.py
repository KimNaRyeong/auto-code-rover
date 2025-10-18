# reproducer.py
from django.utils.dateparse import parse_duration
from django.core.serializers.json import DjangoJSONEncoder
from datetime import timedelta
import json

def duration_iso_string(td):
    # Returns an ISO formatted duration string for a given timedelta object
    return json.dumps(td, cls=DjangoJSONEncoder).strip('"')

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

def test_parse_duration_with_negative_days():
    try:
        # Generate the timedelta object with negative days and no time
        td = timedelta(days=-1)
        # Convert timedelta object to ISO duration string
        iso_str = duration_iso_string(td)
        # Parse the duration from the ISO string
        parsed_duration = parse_duration(iso_str)
        # Assert the parsed duration equals the original timedelta object
        assert parsed_duration == td, "The parsed duration does not match the original timedelta object."

    except AssertionError as e:
        print_stacktrace(e)
        raise e

if __name__ == "__main__":
    test_parse_duration_with_negative_days()
