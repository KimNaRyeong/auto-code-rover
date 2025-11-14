Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
```python
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.db import models
from django.db.models import Count, F
from django.test.utils import setup_test_environment

setup_test_environment()

class Thing(models.Model):
    pass

class Related(models.Model):
    thing = models.ForeignKey(Thing, on_delete=models.CASCADE)

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
    t = Thing.objects.create()
    rs = [Related.objects.create(thing=t) for _ in range(2)]

    qs = Thing.objects.annotate(rc=Count('related')).order_by('?').values('id', 'rc')

    try:
        assert len(qs) == 1, "QuerySet aggregation broken"
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == '__main__':
    main()
```
This script sets up a Django test environment, creates the necessary models and data, and then runs the problematic query. If the issue is present, it raises an `AssertionError` with a message indicating that the QuerySet aggregation is broken. The `print_stacktrace` function is used to print a detailed stack trace of the error.

If you run this script with `python3 reproducer.py`, it should raise an `AssertionError` and print a stack trace if the issue is present, or exit with code 0 if the issue is fixed.