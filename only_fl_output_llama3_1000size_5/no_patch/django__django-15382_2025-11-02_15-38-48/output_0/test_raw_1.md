Here is the reproducer script:

```python
import sys
from django.db import models
from django.db.models import Exists, Q

def print_stacktrace(e: Exception):
    import traceback
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
        from django.db import models
        class MyModel(models.Model):
            name = models.CharField(max_length=255)

        qs = MyModel.objects.filter(~models.Exists(MyModel.objects.none()), name='test')
        if not str(qs.query).startswith('SELECT'):
            raise AssertionError("WHERE block is missing")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    reproduce_issue()
```

This script should be executed by `python3 reproducer.py` in your terminal. If the issue is present, it will raise an `AssertionError`, print a stack trace, and exit with code 1.