Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import datetime
from django.utils.dateparse import parse_duration, duration_iso_string

def test_parse_duration_sign_ignored():
    td = datetime.timedelta(days=-1)
    iso_string = duration_iso_string(td)
    parsed_td = parse_duration(iso_string)

    try:
        assert parsed_td.days == -1
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)

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
<|start_header_id|>