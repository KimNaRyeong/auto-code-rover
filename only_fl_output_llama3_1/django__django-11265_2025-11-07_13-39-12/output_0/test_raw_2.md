Here is the standalone Python file `reproducer.py` to reproduce the issue:

```python
import unittest
from django.db import models
from django.db.models import Q, F
from django.db.models.expressions import FilteredRelation

class Author(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE)

class Book(models.Model):
    title = models.CharField(max_length=255)

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

class TestReproducer(unittest.TestCase):

    def test_with_join_exclude(self):
        try:
            Author.objects.annotate(
                book_alice=FilteredRelation('book', condition=Q(book__title__iexact='poem by alice')),
            ).exclude(book_alice__isnull=False)
            self.fail("Expected AssertionError")
        except Exception as e:
            print_stacktrace(e)

if __name__ == '__main__':
    try:
        TestReproducer().test_with_join_exclude()
    except SystemExit as e:
        if e.code != 0:
            raise
    else:
        exit(0)
```

This script will run the test case and if any exception occurs, it will print the stack trace.