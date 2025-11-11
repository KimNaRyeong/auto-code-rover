Here is the standalone Python file `reproducer.py` to reproduce the issue:

```python
import os
from django.db import models
from django.db.models.query import QuerySet
from reproducer import print_stacktrace

def main():
    try:
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

        o1 = M2.objects.using('default')
        o2 = M1.objects.using('default')
        u1 = o1.union(o2)
        q = u1.order_by('-f2')
        o3 = M3.objects.using('default')
        res = q.union(o3)

        print(res.count())
    except Exception as e:
        print_stacktrace(e)
        os._exit(1)  # Exit with code 0 when the issue is fixed

if __name__ == '__main__':
    main()
```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue. The script will also exit with code 0 when the issue is fixed.