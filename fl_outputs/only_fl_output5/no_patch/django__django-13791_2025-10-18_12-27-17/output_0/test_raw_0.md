```python
import sys
from datetime import timedelta
from django.utils.dateparse import parse_duration

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)


def duration_iso_string(td):
    # Formatting timedelta to ISO 8601 duration string
    # Django does not provide a direct function for this conversion in its public API, so we implement it manually
    seconds = td.total_seconds()
    negative = seconds < 0
    seconds = abs(seconds)
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    duration_str = f"{'-' if negative else ''}P{int(days)}DT{int(hours)}H{int(minutes)}M{int(seconds)}S"
    return duration_str

def test_parse_duration_with_negative_days():
    try:
        # Create a timedelta object with -1 day
        td = timedelta(days=-1)
        # Convert the timedelta to an ISO 8601 duration string
        iso_str = duration_iso_string(td)
        # Parse the duration from the string
        parsed_td = parse_duration(iso_str)
        # Assert the parsed timedelta is identical to the original
        assert parsed_td == td, "Parsed duration does not match the input duration"
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1) # Exit with an error code to signify the test failed

if __name__ == "__main__":
    test_parse_duration_with_negative_days()
    print("Test passed.") # This message is printed only if there's no assertion error.
    sys.exit(0)
```

Please ensure you have Django installed and appropriately configured in your environment before running this script. If Django is not installed, you can install it using pip:

```shell
pip install django
```

This script will attempt to reproduce the issue as described, using the `parse_duration` function from Django's `django.utils.dateparse` module. The `AssertionError` should be raised if the bug is present (i.e., the sign of the duration is not correctly parsed), indicating the failure of the script to correctly handle durations with only day components and a negative sign.