Here is the reproducer script:

```python
import django
from django.db import models
from django.db.models.functions import Value, Concat
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

class TestReproducer(TestCase):
    def setUp(self) -> None:
        self.user = models.User.objects.create_superuser('admin', 'admin@example.com', 'password')

    def test_union_annotated_diff_distinct(self):
        qs = Sample.objects.filter(name__in=['Sam1', 'Sam2 acid', 'Sam3', 'Sam4 acid', 'Dub'])
        qs1 = qs.filter(name='Dub').annotate(rank=Value(0, models.IntegerField()))
        qs2 = qs.filter(name='Sam1').annotate(rank=Value(1, models.IntegerField()))
        qs = qs1.union(qs2)
        qs = qs.order_by('name').distinct('name')  # THIS DISTINCT DOESN'T WORK
        self.assertEqual(qs.count(), 3)  # This assertion should raise an AssertionError

if __name__ == '__main__':
    try:
        test = TestReproducer()
        test.test_union_annotated_diff_distinct()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
```

You can run this script by executing `python3 reproducer.py`. If the issue is present, it should raise an `AssertionError` and print a stack trace.