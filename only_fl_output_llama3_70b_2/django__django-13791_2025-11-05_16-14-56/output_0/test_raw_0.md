Here is the standalone Python script `reproducer.py` to reproduce the issue:
```
import datetime
from django.utils.dateparse import parse_duration, duration_iso_string

def test_parse_duration_sign_ignored():
    td = datetime.timedelta(days=-1)
    iso_string = duration_iso_string(td)
    parsed_td = parse_duration(iso_string)

    assert parsed_td.days == -1, f"Expected days to be -1, but got {parsed_td.days}"

def main():
    try:
        test_parse_duration_sign_ignored()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
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

    main()
```
This script defines a test function `test_parse_duration_sign_ignored` that creates a timedelta object with -1 days, converts it to an ISO string using `duration_iso_string`, and then parses the ISO string back into a timedelta object using `parse_duration`. The test asserts that the resulting timedelta object has -1 days. If the assertion fails, the script catches the `AssertionError`, prints the stack trace using the provided `print_stacktrace` function, and exits with code 1. If the issue is fixed, the script will exit with code 0.