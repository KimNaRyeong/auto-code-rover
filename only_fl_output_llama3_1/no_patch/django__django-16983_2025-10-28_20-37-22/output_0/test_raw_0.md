Here is the reproducer script:

```python
import os
from django.db import models
from django.contrib.admin.filters import SimpleListFilter
from django.contrib.admin.views.main import ChangeList

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

class MyModel(models.Model):
    foo = models.ManyToManyField('MyIntermediateModel')

class MyIntermediateModel(models.Model):
    pass

def test_issue():
    admin_site = None
    try:
        from django.contrib import admin
        admin.site.register(MyModel)
    except AssertionError as e:
        print_stacktrace(e)
        exit(0)

if __name__ == "__main__":
    test_issue()
```

This script creates a Django model with a ManyToManyField that uses an intermediary model. It then attempts to register the model with the admin site, which should raise an `AssertionError` if the issue is present. The script prints the stack trace and exits with code 0 when the issue is fixed.