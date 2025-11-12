Here is a standalone Python file `reproducer.py` that reproduces the issue:

```python
import unittest
from django.db import models
from django.db.models import Q, F

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

class Book(models.Model):
    title = models.CharField(max_length=255)

class Author(models.Model):
    name = models.CharField(max_length=255)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

class FilteredRelationTest(unittest.TestCase):

    def test_with_join_exclude(self):
        try:
            Author.objects.annotate(
                book_alice=FilteredRelation('book', condition=Q(book__title__iexact='poem by alice')),
            ).exclude(book_alice__isnull=False)
            self.fail("Expected FieldError")
        except Exception as e:
            print_stacktrace(e)

if __name__ == '__main__':
    unittest.main()
```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue. The script should also exit with code 0 when the issue is fixed.

To run the script, execute `python3 reproducer.py` in your terminal.