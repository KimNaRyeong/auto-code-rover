Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import decimal
from django.db import models
from django.test import TestCase

class DecimalModel(models.Model):
    dec_field = models.DecimalField(decimal_places=0, max_digits=4)

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
    DecimalModel.objects.get(dec_field='12345')
except decimal.InvalidOperation as e:
    print_stacktrace(e)
    assert False, "Too large decimal query caused exception."
except DecimalModel.DoesNotExist:
    pass
```
This script creates a `DecimalModel` with a `dec_field` that has `max_digits=4`. It then tries to query for an object with a value larger than the maximum allowed digits. If the issue is present, it should raise a `decimal.InvalidOperation` exception, which will be caught and printed with a stack trace using the `print_stacktrace` function. The script will then exit with code 1 due to the `assert False` statement.

If the issue is fixed, the query will return a `DecimalModel.DoesNotExist` exception, which will be caught and ignored, allowing the script to exit with code 0.