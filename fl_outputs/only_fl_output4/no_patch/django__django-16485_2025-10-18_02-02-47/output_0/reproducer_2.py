# reproducer.py
import os
import sys

# Setting up minimal Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reproducer_settings')

from django.conf import settings
settings.configure(
    DEBUG=True,
    SECRET_KEY='not_very_secret_in_this_case',
)

from django.template.defaultfilters import floatformat
from decimal import Decimal
import django
django.setup()

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

def reproduce_issue():
    try:
        # Attempting operations that are reported to raise ValueError
        floatformat('0.00', 0)
        floatformat(Decimal('0.00'), 0)
        # If no exception of ValueError is raised, the issue is presumed fixed
        print("No issue found, the function behaves as expected.")
    except ValueError as e:
        print_stacktrace(e)
        # Asserting the issue's presence with a specific message
        if "valid range for prec is [1, MAX_PREC]" in str(e):
            raise AssertionError("The issue is present.")
        else:
            print("An unexpected ValueError occurred.")
    except Exception as e:
        print("An unexpected error occurred.")
        print_stacktrace(e)

if __name__ == "__main__":
    reproduce_issue()
