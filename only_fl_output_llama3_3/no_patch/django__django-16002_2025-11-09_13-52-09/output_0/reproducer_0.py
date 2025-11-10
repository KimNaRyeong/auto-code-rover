import os
import django
from django.db import models
from decimal import Decimal
from django.core.exceptions import AssertionError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reproducer.settings')
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
    obj = MyModel(value=Decimal("nan"))
    obj.save()
    MyModel.objects.get(pk=1)
except AssertionError as e:
    print_stacktrace(e)
    exit(0)
else:
    raise AssertionError("Issue not reproduced")
