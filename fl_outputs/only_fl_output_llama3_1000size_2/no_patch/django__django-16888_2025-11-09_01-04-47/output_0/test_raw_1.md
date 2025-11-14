Here is the reproducer script:

```python
import decimal
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

try:
    class DecimalModel(models.Model):
        dec_field = models.DecimalField(max_digits=4, decimal_places=0)

    try:
        DecimalModel.objects.get(dec_field='12345')
    except (decimal.InvalidOperation, models.DoesNotExist) as e:
        print_stacktrace(e)
        raise AssertionError("Too large decimal query caused exception.")
except Exception as e:
    print_stacktrace(e)
    exit(1)
```

This script will create a `DecimalField` with `max_digits=4`, then try to get an object from the model where the field value is '12345'. If the issue is present, it will raise an `AssertionError` with a stack trace. If the issue is fixed, it will simply exit with code 0.