Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.db import models
from django.db.models import Sum, Value, Coalesce
from django.test.utils import setup_test_environment

setup_test_environment()

class OrderItem(models.Model):
    quantity = models.IntegerField(default=0)

OrderItem.objects.create(pk=1, quantity=50)

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
    exit(1)

exit(0)
```
This script creates a `OrderItem` model, sets up the Django test environment, and then runs three tests:

1. A matched Queryset that should return 50.
2. An unmatched Queryset that should return 0.
3. An empty list Queryset that should return 0, but returns None due to the issue.

The script uses `assert` statements to check the results of each test. If any of the assertions fail, an `AssertionError` is raised, and the script prints a stack trace using the provided `print_stacktrace` function and exits with code 1. If all tests pass, the script exits with code 0.

To run this script, save it to a file named `reproducer.py` in the root directory of your Django project, and then execute it using `python3 reproducer.py`.