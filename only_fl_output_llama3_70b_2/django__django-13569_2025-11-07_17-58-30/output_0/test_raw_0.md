Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
```python
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'reproducer.settings'

import django
django.setup()

from django.db import models
from django.db.models import Count, F

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
    result = list(qs)

    if len(result) != 1 or result[0]['rc'] != 2:
        raise AssertionError("Queryset aggregation broken")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        exit(1)
```
This script creates the necessary models, inserts some data, and then runs the problematic query. If the result is not what's expected (i.e., a single row with `rc` equal to 2), it raises an `AssertionError`. The `print_stacktrace` function is used to print a detailed stack trace of the error.

To use this script, create a new Django project and app, then add the `reproducer.py` file to the root directory of the project. Run the script with `python3 reproducer.py`. If the issue is present, it should raise an `AssertionError` and print a stack trace. If the issue is fixed, it should exit with code 0.