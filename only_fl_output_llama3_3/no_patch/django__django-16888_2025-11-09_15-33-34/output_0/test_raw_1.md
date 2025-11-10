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

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testbed.settings')

from django.test.utils import setup_test_environment

setup_test_environment()

class DecimalModel(models.Model):
    dec_field = models.DecimalField(decimal_places=0, max_digits=4)

class InvalidDecimalQuery(TestCase):
    def test_invalid_decimal_query(self):
        try:
            DecimalModel.objects.get(dec_field='12345')
        except decimal.InvalidOperation as e:
            print_stacktrace(e)
            self.fail("Too large decimal query caused exception.")
        except models.DoesNotExist:
            pass

if __name__ == "__main__":
    InvalidDecimalQuery().test_invalid_decimal_query()
```

This script sets the DJANGO_SETTINGS_MODULE environment variable and calls setup_test_environment() to configure Django for testing. Then it defines a DecimalModel with max_digits=4 and tests querying for a decimal value larger than this limit, which should raise an AssertionError when the issue is present, print a stack trace of the issue, and exit with code 0 when the issue is fixed.