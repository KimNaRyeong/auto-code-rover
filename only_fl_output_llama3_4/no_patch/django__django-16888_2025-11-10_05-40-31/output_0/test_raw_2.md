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
    from django.db import models
    class DecimalModel(models.Model):
        dec_field = models.DecimalField(decimal_places=0, max_digits=4)
    DecimalModel.objects.get(dec_field='12345')
except Exception as e:
    print_stacktrace(e)
    exit(1)
else:
    assert False, "Expected decimal.InvalidOperation exception"
    exit(0)
```

This script will import the necessary modules and create an instance of the `DecimalModel` with a value larger than the maximum allowed digits. If it raises a `decimal.InvalidOperation`, it will print the stack trace and exit with code 1. If any other exception is raised, it will also print the stack trace and exit with code 0.