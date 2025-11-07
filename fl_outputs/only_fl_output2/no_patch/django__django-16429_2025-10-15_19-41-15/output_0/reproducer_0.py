# reproducer.py

from django.conf import settings
from django.utils import timezone
from django.utils.timesince import timesince
import datetime

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

def reproduce_issue():
    settings.configure(USE_TZ=True)

    now = timezone.now()
    past_date = now - datetime.timedelta(days=31)

    try:
        result = timesince(past_date)
        assert result == "1\xa0month", f"Expected '1\xa0month', got '{result}' instead."
        print("The issue is fixed.")
    except TypeError as e:
        print_stacktrace(e)
        assert False, "The issue is present."

if __name__ == "__main__":
    reproduce_issue()
