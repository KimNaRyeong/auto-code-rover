Here is the reproducer script:

```python
import django
from django.db import models
from django.test import TestCase

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

class Reproducer(TestCase):
    def test_union_annotated_diff_distinct(self):
        from django.db.models.functions import Concat
        class Sample(models.Model):
            name = models.CharField(max_length=255)

        qs = Sample.objects.annotate(name=Concat('name', Value(' acid'), output_field=str)).annotate(rank=Value(0, IntegerField()))
        qs1 = qs.filter(name='Dub').annotate(rank=Value(1, IntegerField()))
        qs2 = qs.filter(name='Sam1').annotate(rank=Value(2, IntegerField()))
        qs = qs.union(qs1).union(qs2)
        self.assertEqual(qs.distinct('name').count(), 3)  # should raise an AssertionError

try:
    Reproducer().test_union_annotated_diff_distinct()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
```

This script will create a simple Django model, run the test case and if it fails, it will print the stack trace and exit with code 1. If the test passes, it will simply exit with code 0.

Please note that this is just an example of how you could reproduce the issue. The actual code may vary depending on your specific use case.