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

def main():
    try:
        class DecimalModel(models.Model):
            dec_field = models.DecimalField(decimal_places=0, max_digits=4)

        DecimalModel.objects.get(dec_field='12345')
        assert False, "Expected decimal.InvalidOperation exception"
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Failed to reproduce the issue")

if __name__ == "__main__":
    main()
```

This script can be run by executing `python3 reproducer.py`. If the issue is present, it will print a stack trace and raise an `AssertionError`.