import django
from django.db import models

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

def main():
    try:
        from django.db.models.fields import DecimalField
        decimal_field = DecimalField(max_digits=5, decimal_places=2)
        decimal_field.to_python({'a': 1})
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected TypeError")

if __name__ == "__main__":
    main()
