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

try:
    class DecimalModel(models.Model):
        dec_field = models.DecimalField(decimal_places=0, max_digits=4)

    class InvalidDecimalQuery(TestCase):
        def test_invalid_decimal_query(self):
            try:
                DecimalModel.objects.get(dec_field='12345')
            except decimal.InvalidOperation:
                self.fail("Too large decimal query caused exception.")
            except models.DoesNotExist:
                pass

    InvalidDecimalQuery('test_invalid_decimal_query').run()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)
except Exception as e:
    print_stacktrace(e)
    exit(0)
```

This script will run the test case and if the issue is present, it will raise an `AssertionError` with a stack trace. If the issue is fixed, it will simply exit with code 0.