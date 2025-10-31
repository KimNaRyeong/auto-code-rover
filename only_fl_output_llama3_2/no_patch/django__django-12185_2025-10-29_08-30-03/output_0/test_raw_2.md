Here is the reproducer script:

```python
import django
from django.db.models import F, Value, BooleanField
from django.db.models.expressions import Case, When, Window, Lag

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
    from django.db.models.functions import Lag

    class Employee:
        pass

    Employee.objects.annotate(
        lag=Window(expression=Lag(expression='salary', offset=1), partition_by=F('department'), order_by=[F('salary').asc(), F('name').asc()]),
        is_changed=Case(When(salary=F('lag'), then=Value(False)), default=Value(True), output_field=BooleanField())
    )
except django.core.exceptions.NotSupportedError as e:
    print_stacktrace(e)
    raise AssertionError("Expected NotSupportedError")
else:
    print("Test passed. The issue is not present.")
    exit(0)
```

This script should be placed in a file named `reproducer.py` and executed with the command `python3 reproducer.py`. It will attempt to annotate an Employee model with a window expression and a conditional statement, which should raise a `NotSupportedError` due to the issue described.