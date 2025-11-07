Here's how you can structure your `reproducer.py` file to achieve your goals. The script first attempts to reproduce the issue using Django's `parse_duration` and `duration_iso_string` functionalities. Then, it checks for the expected outcome and raises an `AssertionError` if the test fails, printing a detailed stack trace of the assertion error.

```python
import sys
from datetime import timedelta
from django.utils.duration import duration_iso_string
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

def test_parse_duration_with_negative_days():
    try:
        # Creating a timedelta object with negative days
        td = timedelta(days=-1)
        # Converting timedelta object to ISO 8601 string using duration_iso_string
        iso_string = duration_iso_string(td)
        # Parsing the ISO 8601 string back to a timedelta object using parse_duration
        parsed_td = parse_duration(iso_string)
        # Asserting that the days attribute of the parsed timedelta object should be -1
        assert parsed_td.days == -1, "The parsed duration does not have the correct number of days."
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)  # Exiting with code 1 indicates the issue is present

    print("Test passed. The issue is fixed.")
    sys.exit(0)  # Exiting with code 0 indicates the issue is fixed

if __name__ == "__main__":
    test_parse_duration_with_negative_days()
```

Before running this script, ensure that Django is installed in your environment and properly configured, since it relies on Django-specific functions `duration_iso_string` and `parse_duration`. If your Django project settings are not setup, you may run into errors related to Django's configuration. You might need to set the `DJANGO_SETTINGS_MODULE` environment variable or adjust the script to configure Django settings at runtime for testing purposes.