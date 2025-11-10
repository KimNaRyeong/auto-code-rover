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
        from django.contrib.auth.models import User
        self.user = User.objects.create_superuser('admin', 'admin@example.com', 'password')

    def test_union_annotated_diff_distinct(self):
        from django.db.models.functions import Concat, Value

        Sample = models.Model
        Sample.h.create(self.user, name="Sam1")
        Sample.h.create(self.user, name="Sam2 acid")
        Sample.h.create(self.user, name="Sam3")
        Sample.h.create(self.user, name="Sam4 acid")
        Sample.h.create(self.user, name="Dub")
        Sample.h.create(self.user, name="Dub")
        Sample.h.create(self.user, name="Dub")

        qs = Sample.objects.filter(user=self.user)
        qs1 = qs.filter(name='Dub').annotate(rank=Value(0, models.IntegerField()))
        qs2 = qs.filter(name='Sam1').annotate(rank=Value(1, models.IntegerField()))
        qs = qs1.union(qs2)
        try:
            qs = qs.order_by('name').distinct('name')  # THIS DISTINCT DOESN'T WORK
            self.assertEqual(qs.count(), 2)  # Expected to get wrapped union
        except AssertionError as e:
            print_stacktrace(e)
            exit(1)

if __name__ == '__main__':
    try:
        TestReproducer().test_union_annotated_diff_distinct()
    except Exception as e:
        print_stacktrace(e)
        exit(1)
```

This script sets up a test case that reproduces the issue. The `setUp` method creates an admin user, and the `test_union_annotated_diff_distinct` method performs the query that should raise an error when distinct is used on union. If the assertion fails (i.e., the count of the queryset is not 2), it prints the stack trace using the provided function and exits with code 1.