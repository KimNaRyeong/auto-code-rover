Here is a new standalone Python file `reproducer.py` to reproduce the issue:
```
import os
import sys
from django.conf import settings
from django.db import models
from django.test import TestCase
from django.db.models import Sum, Value
from django.db.models.functions import Coalesce

settings.configure(
    DEBUG=True,
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}},
    INSTALLED_APPS=('reproducer', ),
)

class OrderItem(models.Model):
    quantity = models.IntegerField()

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
    # Create the tables
    models.Model.__subclasses__()

    # Create some test data
    OrderItem.objects.create(pk=1, quantity=50)

    # Test with matched Queryset. Sum will return 50
    result = OrderItem.objects.filter(pk__in=[1]).aggregate(test=Coalesce(Sum('quantity'), Value(0)))
    assert result['test'] == 50

    # Test with unmatched Queryset. Sum will return 0
    result = OrderItem.objects.filter(pk__in=[-1]).aggregate(test=Coalesce(Sum('quantity'), Value(0)))
    assert result['test'] == 0

    # Test with unmatched Queryset (using empty list). EmptyResultSet returned because of empty list. Sum should return 0, but returns None
    result = OrderItem.objects.filter(pk__in=[]).aggregate(test=Coalesce(Sum('quantity'), Value(0)))
    assert result['test'] == 0

except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)

sys.exit(0)
```
This script sets up a minimal Django environment, defines the `OrderItem` model, and runs the three tests. If any of the assertions fail, it prints a stack trace using the provided `print_stacktrace` function and exits with code 1. If all tests pass, it exits with code 0.