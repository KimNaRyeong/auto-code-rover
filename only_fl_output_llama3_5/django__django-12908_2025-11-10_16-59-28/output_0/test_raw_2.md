Here is the reproducer script:

```python
import django
from django.db import models
from django.test import TestCase
from django.db.models.functions import Concat, Value
from django.db.models import IntegerField

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

class Sample(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

class Reproducer(TestCase):

    def setUp(self) -> None:
        self.user = self.get_or_create_admin_user()
        Sample.objects.create(user=self.user, name="Sam1")
        Sample.objects.create(user=self.user, name="Sam2 acid")
        Sample.objects.create(user=self.user, name="Sam3")
        Sample.objects.create(user=self.user, name="Sam4 acid")
        Sample.objects.create(user=self.user, name="Dub")
        Sample.objects.create(user=self.user, name="Dub")
        Sample.objects.create(user=self.user, name="Dub")

    def test_union_annotated_diff_distinct(self):
        qs = Sample.objects.filter(user=self.user)
        qs1 = qs.filter(name='Dub').annotate(rank=Value(0, IntegerField()))
        qs2 = qs.filter(name='Sam1').annotate(rank=Value(1, IntegerField()))
        qs = qs1.union(qs2)
        qs = qs.order_by('name').distinct('name')  # THIS DISTINCT DOESN'T WORK
        self.assertEqual(qs.count(), 2)  # This assertion should raise an AssertionError

try:
    Reproducer().test_union_annotated_diff_distinct()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Issue not reproduced. It seems the issue is fixed.")
exit(0)
```

This script will reproduce the issue if it exists, and it should raise an `AssertionError` when the issue is present and print a stack trace of the issue.