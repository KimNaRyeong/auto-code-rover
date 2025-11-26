Here is a standalone Python script `reproducer.py` to reproduce the issue:
```
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

class MyModel(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ['name']

class TestQuerysetOrdering(TestCase):
    def test_ordering(self):
        MyModel.objects.create(name='Alice')
        MyModel.objects.create(name='Bob')

        qs = MyModel.objects.all().order_by('name').reverse()
        self.assertEqual(qs.ordered, True)
        self.assertEqual(qs.query.order_by, ['-name'])

        # This should raise an AssertionError if the issue is present
        assert qs.query.order_by == ['-name'], "Queryset ordering is mutable"

try:
    django.setup()
    TestQuerysetOrdering('test_ordering').run()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
```
This script defines a Django model `MyModel` with a Meta ordering set to `['name']`. It then creates two instances of the model and runs a test case that checks if the queryset ordering is mutable.

If the issue is present, the `assert` statement will raise an `AssertionError`, which will be caught and printed with a stack trace using the provided `print_stacktrace` function. The script will exit with code 1 in this case.

If the issue is fixed, the script will exit with code 0.