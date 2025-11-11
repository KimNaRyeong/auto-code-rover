Here is the reproducer script:

```python
import django
from django.db import models, connection
from django.db.models import F, Max, Sum
from django.db.models.query import QuerySet
from django.core.exceptions import AssertionError

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
    try:
        from myproject.settings import *
        django.setup()
        class T(models.Model):
            id = models.AutoField(primary_key=True)
            foo = models.IntegerField()

        result = T.objects.annotate(anon=F('foo')).aggregate(foo=Max(F('anon')), sum=Sum(F('foo')))
        if 'foo' in str(result).lower():
            raise AssertionError("Issue present")
        print("Issue not present")
        exit(0)
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    main()
```

This script sets up a Django environment, defines the `T` model and performs the query that reproduces the issue. If the issue is present, it raises an `AssertionError`.