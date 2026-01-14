 I apologize for the mistake in my previous response. Here is the corrected `reproducer.py` script that reproduces the issue:
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
        original_ordering = list(qs.query.order_by)
        qs = qs.reverse()
        self.assertNotEqual(original_ordering, list(qs.query.order_by))

if __name__ == '__main__':
    try:
        MyTest.test_ordering_mutability()
    except AssertionError as e:
