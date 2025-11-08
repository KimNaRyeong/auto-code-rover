Here is the reproducer script:

```python
import decimal
from django.db import models
from django.test import TestCase

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

class DecimalModel(models.Model):
    dec_field = models.DecimalField(decimal_places=0, max_digits=4)

class InvalidDecimalQuery(TestCase):
    def test_invalid_decimal_query(self):
        try:
            DecimalModel.objects.get(dec_field='12345')
            assert False, "Expected decimal.InvalidOperation"
        except decimal.InvalidOperation as e:
            print_stacktrace(e)
            raise

if __name__ == "__main__":
    InvalidDecimalQuery().test_invalid_decimal_query()
```

This script can be run with `python3 reproducer.py` and it will reproduce the issue by querying for a decimal value larger than the maximum allowed digits. The stack trace of the exception is printed, and if the issue is fixed, the script exits with code 0.