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
    from django.db.models import DecimalField
except ImportError as e:
    print_stacktrace(e)
    raise SystemExit(1)

class DecimalModel(models.Model):
    dec_field = models.DecimalField(decimal_places=0, max_digits=4)

try:
    DecimalModel.objects.get(dec_field='12345')
except decimal.InvalidOperation as e:
    print_stacktrace(e)
    assert False, "Too large decimal query caused exception."
```

This script tries to import the `DecimalField` from Django's models module. If this fails (which it should), it prints a stack trace and raises an assertion error with code 1.