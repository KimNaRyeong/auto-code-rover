Here is the standalone Python file `reproducer.py` that reproduces the issue:

```python
import os
from django.db import models
from django.db.models.query import QuerySet
from django.db.utils import IntegrityError

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

class M1(models.Model):
    id = models.AutoField(primary_key=True, blank=True, null=True)
    f1 = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'm1'

class M2(models.Model):
    id = models.AutoField(primary_key=True, blank=True, null=True)
    f2 = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'm2'

class M3(models.Model):
    id = models.AutoField(primary_key=True, blank=True, null=True)
    f3 = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'm3'

if __name__ == "__main__":
    try:
        o1 = M2.objects.using('default')
        o2 = M1.objects.using('default')
        u1 = o1.union(o2)
        q = u1.order_by('-f2')
        o3 = M3.objects.using('default')
        res = q.union(o3)
        print(res.count())
    except Exception as e:
        print_stacktrace(e)
        assert False, "Expected TypeError exception"
```

This script should raise an `AssertionError` when the issue is present and print a stack trace of the issue.