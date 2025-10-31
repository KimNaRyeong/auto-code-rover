import datetime
from django.core.management import call_command

def parse_duration_to_time(duration):
    # This function is not implemented in your example, but it's assumed to exist.
    pass

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
    try:
        call_command('pause', '--for', 'now', '--until', '2022-01-01')
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected the command to succeed, but it failed")

if __name__ == "__main__":
    reproduce_issue()
