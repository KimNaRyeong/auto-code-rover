Here's a Python script named `reproducer.py` that you can use to reproduce the issue described. This script first confirms the bug by showing that the sign of the ISO duration string representing only days (without hours, minutes, or seconds) is ignored when parsed back to a `timedelta`. It raises an `AssertionError` if the parsed duration does not match the expected negative value, indicating the presence of the bug.

```python
from datetime import timedelta
from django.utils.dateparse import parse_duration

def duration_iso_string(td):
    """Converts a timedelta object to an ISO 8601 duration string."""
    # Total seconds in the timedelta
    total_seconds = int(td.total_seconds())
    sign = "-" if total_seconds < 0 else ""
    total_seconds = abs(total_seconds)
    
    days, remainder = divmod(total_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    return f'{sign}P{days}DT{hours}H{minutes}M{seconds}S'

def test_parse_duration_with_days_only():
    try:
        td_negative = timedelta(days=-1)
        iso_string_negative = duration_iso_string(td_negative)
        parsed_td_negative = parse_duration(iso_string_negative)

        assert parsed_td_negative == td_negative, "Parsed timedelta does not match the original negative days only timedelta."

    except AssertionError as e:
        print_stacktrace(e)
        raise

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
    test_parse_duration_with_days_only()
```

Prior to running this script, ensure you have Django installed in your environment as it uses Django's `parse_duration` function. You can install Django by running:

```
pip install Django
```

When the issue exists, the script will raise an `AssertionError` and print the stack trace pointing to where in the script the assertion failed due to the bug. Once the issue is fixed (meaning the parsed duration correctly reflects the negative days), the script should execute without error, indicating the absence of the bug.