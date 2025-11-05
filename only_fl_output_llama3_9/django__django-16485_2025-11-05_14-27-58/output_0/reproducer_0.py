import sys
from decimal import Decimal
from django.template.defaultfilters import floatformat

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

try:
    floatformat('0.00', 0)
    floatformat(Decimal('0.00'), 0)
except ValueError as e:
    print_stacktrace(e)
    assert False, "Expected ValueError"
    sys.exit(1)
else:
    print("Issue not present")
    sys.exit(0)
