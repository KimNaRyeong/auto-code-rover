import datetime
from django.core.management import call_command
from django.core.exceptions import ValidationError
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

def main():
    try:
        call_command('pause', '--for', '1 day')
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected error")

if __name__ == "__main__":
    main()
