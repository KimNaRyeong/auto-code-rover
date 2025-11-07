Here is the reproducer script:

```python
import decimal
from django.db.models import DecimalField, F
from django.db.models.functions import Mod

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
        from django.db.models import F, Mod

        class Model:
            value = DecimalField(max_digits=10, decimal_places=2)
            result1 = F('value') + 5
            result2 = F('value') % 5

        model = Model()
        assert isinstance(model.result1, decimal.Decimal) and isinstance(model.result2, decimal.Decimal)
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    reproduce_issue()
```

This script creates a simple Django model with two calculated fields: `result1` which is the sum of `value` and 5, and `result2` which is the MOD of `value` by 5. The `reproduce_issue` function tries to create an instance of this model, which should raise an `AssertionError` because the results are not resolved to Decimal types like they would be for other mathematical operators.