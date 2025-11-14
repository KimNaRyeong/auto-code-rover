Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import datetime
from django.utils.dateparse import parse_duration, duration_iso_string

def test_parse_duration():
    td = datetime.timedelta(days=-1)
    iso_string = duration_iso_string(td)
    parsed_td = parse_duration(iso_string)

    assert parsed_td.days == -1, f"Expected days to be -1, but got {parsed_td.days}"

try:
    test_parse_duration()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)
else:
    print("Issue is fixed!")
    exit(0)

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
```
This script will raise an `AssertionError` if the issue is present, printing a stack trace of the error. If the issue is fixed, it will print "Issue is fixed!" and exit with code 0.