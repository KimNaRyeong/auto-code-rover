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
    value = '0E+1'
    field = DecimalField(max_digits=8, decimal_places=7)
    try:
        field.clean(value)
    except ValidationError as e:
        print_stacktrace(e)
        assert False, f"'{value}' is an invalid decimal"

if __name__ == "__main__":
    import os
    os.environ['DJANGO_SETTINGS_MODULE'] = 'django.conf.global_settings'
    import django
    django.setup()
    test_decimal_validator()
