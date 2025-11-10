import os
from decimal import Decimal
from django.db import models

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
    from django.db import models
    class MyModel(models.Model):
        value = models.DecimalField(max_digits=10, decimal_places=5)

    obj = MyModel(value=Decimal("nan"))
    obj.save()
    MyModel.objects.get(pk=1)
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Issue present")
else:
    print("Issue fixed")
    exit(0)
