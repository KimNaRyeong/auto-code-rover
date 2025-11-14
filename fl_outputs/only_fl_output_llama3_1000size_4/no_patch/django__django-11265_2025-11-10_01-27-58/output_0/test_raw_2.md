Here is the reproducer script:

```python
import unittest
from django.db import models
from django.db.models import Q, F

def main():
    class Test(unittest.TestCase):
        def test_with_join(self):
            self.assertSequenceEqual(
                models.Author.objects.annotate(
                    book_alice=FilteredRelation('book', condition=Q(book__title__iexact='poem by alice')),
                ).exclude(book_alice__isnull=False),
                []
            )

    try:
        Test('test_with_join').run()
    except Exception as e:
        print_stacktrace(e)
        raise

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

if __name__ == '__main__':
    main()
```

This script creates a test case that reproduces the issue. The test case uses `FilteredRelation` and `exclude` to filter the results, which should raise an exception if the issue is present.