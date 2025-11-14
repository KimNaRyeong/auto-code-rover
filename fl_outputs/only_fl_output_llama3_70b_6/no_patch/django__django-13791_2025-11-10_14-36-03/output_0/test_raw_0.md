Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import datetime
from django.utils.dateparse import parse_duration, duration_iso_string

def test_parse_duration_sign_ignored():
    td = datetime.timedelta(days=-1)
    iso_string = duration_iso_string(td)
    parsed_td = parse_duration(iso_string)

    try:
        assert parsed_td.days == -1, f"Expected days to be -1, but got {parsed_td.days}"
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
    test_parse_duration_sign_ignored()
```
This script will raise an `AssertionError` when the issue is present, printing a stack trace of the error. If the issue is fixed, the script will exit with code 0.

To run the script, save it to a file named `reproducer.py` in the root directory of your project and execute it using `python3 reproducer.py`.