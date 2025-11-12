Here is the reproducer script:

```python
import os
import django
from django.db import models
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reproducer.settings')
django.setup()

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
    from reproducer.models import MyModel
    obj = MyModel(value=Decimal("nan"))
    obj.save()
    MyModel.objects.get(pk=1)
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Issue not fixed")
```

This script sets up a Django project, creates a model with a DecimalField, saves an instance with the value "nan", and then tries to retrieve that instance. If the issue is present, it prints the stack trace and raises an AssertionError.