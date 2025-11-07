Certainly! Below is a self-contained Python script named `reproducer.py` designed to reproduce the issue described. It tests the behavior of Django's `parse_duration` function with an ISO 8601 duration string representing a negative duration that only includes days. The script will raise an `AssertionError` if the issue is present (i.e., if the sign of the days is ignored by `parse_duration`), and it prints a clear stack trace of where the issue was detected. The script will not raise an error and will exit with a status code of 0 if the issue is fixed.

```python
# reproducer.py

import datetime
from django.utils.dateparse import parse_duration
from django.core.serializers.json import DjangoJSONEncoder

def duration_iso_string(delta):
    return DjangoJSONEncoder().default(delta)

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
    td = datetime.timedelta(days=-1)
    iso_str = duration_iso_string(td)
    result = parse_duration(iso_str)
    try:
        assert result == td, f"Expected {td}, got {result}"
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)
    else:
        print("Test passed. No issue found.")

if __name__ == "__main__":
    test_parse_duration_with_negative_days()
```

Please ensure that Django is installed in your Python environment before running this script. You can install Django using pip if you haven't already:

```shell
pip install Django
```

Execute the script with Python 3:

```shell
python3 reproducer.py
```

This script specifically checks if the `parse_duration` function correctly handles ISO 8601 duration strings representing negative durations when only days are specified. If the duration is incorrectly parsed (i.e., as positive instead of negative), the script prints a detailed stack trace and exits with code 1, indicating failure. If the test passes (meaning the parsing behavior is as expected), it prints a success message and exits with code 0.