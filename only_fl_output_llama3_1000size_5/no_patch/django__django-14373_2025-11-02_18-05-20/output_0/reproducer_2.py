import datetime
from django.utils import dateformat

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
    year = 500
    date_string = dateformat.format(datetime.date(year, 1, 1), 'Y')
    assert len(date_string) == 4 and date_string[0] != '0', "DateFormat.Y() is not zero-padded."
    print_stacktrace(AssertionError("Issue reproduced"))

if __name__ == "__main__":
    reproduce_issue()
