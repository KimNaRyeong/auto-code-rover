Here is the reproducer script:

```python
import decimal
from django.db.models import DecimalField, F, Mod

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

def reproduce_issue():
    try:
        decimal.getcontext().prec = 2
        from django.db.models import DecimalField, F, Mod

        class Model:
            x = DecimalField(max_digits=10, decimal_places=2)
            y = DecimalField(max_digits=10, decimal_places=2)

        model = Model()
        result = (model.x % model.y).resolve()

        assert isinstance(result, decimal.Decimal), "MOD operator doesn't resolve to Decimal type"
    except AssertionError as e:
        print_stacktrace(e)
        raise
    else:
        exit(0)

if __name__ == "__main__":
    reproduce_issue()
```

This script creates a simple Django model with two DecimalField attributes. It then uses the MOD operator to calculate the remainder of `x` divided by `y`. The result is expected to be a Decimal type, but if it's not, an AssertionError will be raised and the stack trace printed.