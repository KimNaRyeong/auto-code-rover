# reproducer.py
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone
from django.utils.timesince import timesince

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

def test_long_interval_with_tz():
    settings.configure(USE_TZ=True)
    now = timezone.now()
    past_date = now - timedelta(days=31)
    try:
        result = timesince(past_date)
        assert "month" in result, "The timesince function did not return expected '1 month' string."
        print("No issue detected. Exiting with code 0.")
        exit(0)
    except Exception as e:
        print_stacktrace(e)
        assert False, "timesince() raised an exception with >1 month interval."

if __name__ == "__main__":
    test_long_interval_with_tz()
