Here is the reproducer script:

```python
from django.db.models import F, DecimalField, IntegerField
from django.db.models.functions import Mod as DjangoMod
from decimal import Decimal
import traceback
import sys

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def reproduce_issue():
    decimal_value = Decimal('1.5')
    integer_value = 2
    result = (DjangoMod(F('value'), F(integer_value)) for value in [decimal_value, integer_value])
    if not all(isinstance(r, Decimal) for r in result):
        raise AssertionError("MOD operator does not resolve output to Decimal type")

if __name__ == "__main__":
    try:
        reproduce_issue()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        print("Issue reproduced successfully")
        exit(0)
```

This script creates a query that uses the MOD operator with a decimal value and an integer value. It checks if all results are of type Decimal, and raises an AssertionError if not.