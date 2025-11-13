Here is a standalone Python file `reproducer.py` to reproduce the issue:
```
from django.db import models
from django.core.exceptions import ImproperlyConfigured

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
    some_field = models.CharField(max_length=255)

try:
    MyModel.objects.filter(F('some_field').lower() == 'anssi')
    raise AssertionError("Expressions in filter calls are supported")
except TypeError as e:
    print_stacktrace(e)
    exit(1)
```
This script defines a Django model `MyModel` with a field `some_field`. It then attempts to use an expression in a `.filter()` call, which should raise a `TypeError` if the issue is present. If the issue is fixed, it will raise an `AssertionError`.

You can run this script by executing `python3 reproducer.py` in the root directory of your project.