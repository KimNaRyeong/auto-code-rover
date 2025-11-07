Here is the reproducer script:

```python
import os
import sys
from django.db import models
from django.db.models.functions import Count, Random
from django.db.models.expressions import F
from django.db.models.query_utils import Q

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

def reproduce_issue():
    class Thing(models.Model):
        pass

    class Related(models.Model):
        thing = models.ForeignKey(Thing, on_delete=models.CASCADE)

    t = Thing.objects.create()
    rs = [Related.objects.create(thing=t) for _ in range(2)]

    try:
        result = Thing.objects.annotate(rc=Count('related')).order_by('?').values('id', 'rc')
        if len(result) != 1 or result[0]['rc'] != 2:
            raise AssertionError("Expected a single row with rc=2")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    reproduce_issue()
```

This script creates the `Thing` and `Related` models, populates the database with some data, and then attempts to execute the query that reproduces the issue. If the query fails or produces unexpected results, it prints a stack trace and exits with code 1.