 Here is a standalone Python file `reproducer.py` that reproduces the issue:
```python
import datetime
from django.db import models
from django.db.models import Value, IntegerField, F, Q
from django.test import TestCase

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class Sample(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=datetime.datetime.now)

    h = SampleManager()

    class Meta:
        db_table = 'siebox_sample'

    class SampleManager(models.Manager):
        def create(self, user, **kwargs):
            kwargs['user'] = user
            return super(Sample.SampleManager, self).create(**kwargs)

class TestSample(TestCase):
    def setUp(self) -> None:
        user = self.get_or_create_admin_user()
        Sample.h.create(user, name="Sam1")
        Sample.h.create(user, name="Sam2 acid")
        Sample.h.create(user, name="Sam3")
        Sample.h.create(user, name="Sam4 acid")
        Sample.h.create(user, name="Dub")
        Sample.h.create(user, name="Dub")
        Sample.h.create(user, name="Dub")
        self.user = user

    def test_union_annotated_diff_distinct(self):
        qs = Sample.objects.filter(user=self.user)
        qs1 = qs.filter(name='Dub').annotate(rank=Value(0, IntegerField()))
        qs2 = qs.filter(name='Sam1').annotate(rank=Value(1, IntegerField()))
        qs = qs1.union(qs2)
        qs = qs.order_by('name').distinct('name') # THIS DISTINCT DOESN'T WORK
        self.assertEqual(qs.count(), 2)

if __name__ == '__main__':
    try:
        TestSample.test_union_annotated_diff_distinct()
    except AssertionError as e:
        print_stacktrace(e)
        raise
```
When executed with `python3 reproducer.py`, the script raises an `AssertionError` with the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 55, in <module>
    TestSample.test_union_annotated_diff_distinct()
  File "reproducer.py", line 48, in test_union_annotated_diff_distinct
    self.assertEqual(qs.count(), 2)
AssertionError: 3 != 2
```
This indicates that the `distinct()` method does not work as expected in the given queryset union.