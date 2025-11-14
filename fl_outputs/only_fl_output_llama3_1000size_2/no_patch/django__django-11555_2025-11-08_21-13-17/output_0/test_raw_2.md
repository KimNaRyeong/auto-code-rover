Here is the reproducer script:

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
    os.environ['DJANGO_SETTINGS_MODULE'] = 'test.settings'
    from django.conf import settings
    from models import ParentModel

    try:
        class Meta:
            ordering = ['expression']

        ParentModel.objects.order_by(F('expression'))
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected the script to run without raising an exception")

if __name__ == "__main__":
    main()
```

This script should be placed in a file named `reproducer.py` and executed with `python3 reproducer.py`. It will set the DJANGO_SETTINGS_MODULE environment variable, import the settings module, and then attempt to order by an expression. If the issue is present, it will print the stack trace and raise an `AssertionError`.