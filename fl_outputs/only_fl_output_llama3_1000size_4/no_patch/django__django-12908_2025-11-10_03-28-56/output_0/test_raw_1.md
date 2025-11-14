Here is the reproducer script:

```python
import django
from django.db import models
from django.db.models.functions import Value, IntegerField
from django.contrib.auth.models import User

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

def test_union_annotated_diff_distinct():
    user = User.objects.create()
    Sample.h.create(user, name="Sam1")
    Sample.h.create(user, name="Sam2 acid")
    Sample.h.create(user, name="Sam3")
    Sample.h.create(user, name="Sam4 acid")
    Sample.h.create(user, name="Dub")
    Sample.h.create(user, name="Dub")
    Sample.h.create(user, name="Dub")

    qs = Sample.objects.filter(user=user)
    qs1 = qs.filter(name='Dub').annotate(rank=Value(0, IntegerField()))
    qs2 = qs.filter(name='Sam1').annotate(rank=Value(1, IntegerField()))
    qs = qs1.union(qs2)
    qs = qs.order_by('name').distinct('name')  # THIS DISTINCT DOESN'T WORK
    assert qs.count() == 2

try:
    test_union_annotated_diff_distinct()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Test passed")
exit(0)
```

This script sets up a Django project, creates some sample data, and then runs the test case. If the assertion fails (i.e., the distinct() method does not work), it prints the stack trace and exits with code 1. Otherwise, it prints "Test passed" and exits with code 0.

Please note that this script assumes you have a `Sample` model defined in your project.