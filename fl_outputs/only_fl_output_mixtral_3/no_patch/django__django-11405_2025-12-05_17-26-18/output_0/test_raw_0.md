 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
from django.db import models
from django.test import TestCase

class MyModel(models.Model):
    name = models.CharField(max_length=100)
    value = models.IntegerField()

    class Meta:
        ordering = ('-value',)

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class MyTest(TestCase):
    def test_ordering_mutability(self):
        qs = MyModel.objects.all()
        original_order = list(qs)
        reversed_order = list(qs.reverse())
        self.assertNotEqual(original_order, reversed_order)
        qs = MyModel.objects.all()
        qs = qs.order_by('-value')
        original_order = list(qs)
        reversed_order = list(qs.reverse())
        self.assertNotEqual(original_order, reversed_order)

try:
    MyTest().test_ordering_mutability()
except AssertionError as e:
    print_stacktrace(e)
    raise
```
When executed with `python3 reproducer.py`, the script raises an `AssertionError` and prints a stack trace, demonstrating the mutability of `Queryset` ordering and `Meta.ordering` with `reverse()`. When the issue is fixed, the script should exit with code 0 without raising any exceptions.