Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import datetime
from django.utils.dateparse import parse_duration, duration_iso_string

def test_parse_duration():
    td = datetime.timedelta(days=-1)
    iso_string = duration_iso_string(td)
    parsed_td = parse_duration(iso_string)
    assert parsed_td == td, f"Expected {td} but got {parsed_td}"

def main():
    try:
        test_parse_duration()
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
    main()
```
This script will raise an `AssertionError` when the issue is present, printing a stack trace of the error. If the issue is fixed, the script will exit with code 0.

To run the script, save it as `reproducer.py` in the root directory of your project and execute it with `python3 reproducer.py`.