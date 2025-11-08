Here is the reproducer script:

```python
import os
import django
from django.db import models
from decimal import Decimal
from django.core.exceptions import AssertionError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_project.settings')
django.setup()

class MyModel(models.Model):
    value = models.DecimalField(max_digits=10, decimal_places=5)

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
    MyModel.objects.create(value="nan")
    obj = MyModel.objects.get(value=Decimal("nan"))
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Issue reproduced")

print("Issue not reproduced, exiting with code 0")
exit(0)
```

This script sets up a Django project and model, creates an instance of the model with a value of "nan", and then tries to retrieve that instance from the database. If the issue is present, it will print the stack trace and raise an AssertionError.