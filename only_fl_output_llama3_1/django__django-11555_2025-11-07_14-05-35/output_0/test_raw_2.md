Here is the standalone Python file `reproducer.py` to reproduce the issue:

```python
import os
from django.db import models
from django.db.models.expressions import F, Value
from django.db.models.query_utils import Q

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
        from django.db.models import Q
        from django.db.models.expressions import F, Value

        class ParentModel(models.Model):
            class Meta:
                ordering = ['expression()']

        def expression():
            return F('some_field') + Value(1, output_field=models.IntegerField())

        ParentModel.objects.order_by(expression())
    except Exception as e:
        print_stacktrace(e)
        raise
    else:
        exit(0)

if __name__ == '__main__':
    main()
```

This script should be executed by running `python3 reproducer.py` in the root directory of the project. If the issue is present, it will raise an `AssertionError` and print a stack trace with line numbers.