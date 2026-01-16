```python
# reproducer.py
from django.utils.dateparse import parse_datetime
import sys

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

def test_parse_datetime_with_spaces():
    valid_iso_datetime_with_space = "2012-04-23T10:20:30.400 -02"
    result = parse_datetime(valid_iso_datetime_with_space)
    try:
        assert result is not None, "parse_datetime failed to parse ISO-8601 with space before timezone"
    except AssertionError as e:
        print_stacktrace(e)
        raise
    else:
        print("Test passed: ISO-8601 datetime string with space before timezone is parsed successfully.")

if __name__ == "__main__":
    test_parse_datetime_with_spaces()
```

This script uses Django's `parse_datetime` function to test its ability to parse ISO-8601 datetime strings that contain a space before the timezone (which is valid according to ISO-8601). According to the described issue, Django's `parse_datetime` function incorrectly returns `None` for valid ISO-8601 datetime strings that contain a space before the timezone. The script is designed to raise an `AssertionError` if the issue is present, indicating that `parse_datetime` failed to correctly parse the datetime string. When the issue is fixed, the script will exit with code 0, signaling that the datetime string is parsed successfully.