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
    raise AssertionError("Too large decimal query caused exception.")
except Exception as e:
    print_stacktrace(e)
```
This script creates a `DecimalModel` with a `dec_field` that has `max_digits=4`. It then tries to query for an object with a value of `'12345'`, which is larger than the maximum allowed digits. If the query raises a `decimal.InvalidOperation` exception, it prints the stack trace and raises an `AssertionError`. If any other exception is raised, it also prints the stack trace.

You can run this script by executing `python3 reproducer.py` in the root directory of your project.