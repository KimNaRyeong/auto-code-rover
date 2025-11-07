Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import unittest
from decimal import Decimal
from django.forms.fields import DecimalField
from django.core.exceptions import ValidationError

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

def test_decimal_validator():
    try:
        DecimalField(max_digits=8, decimal_places=7).clean('0E+1')
    except ValidationError as e:
        print_stacktrace(e)
        assert False, "'0E+1' is an invalid decimal"

if __name__ == "__main__":
    import os
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django.conf.global_settings")
    test_decimal_validator()
```
This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue. The script will exit with code 0 when the issue is fixed.

Please note that I added the line `os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django.conf.global_settings")` to configure Django settings before accessing them. This should fix the `ImproperlyConfigured` error you were seeing.