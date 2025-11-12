Here is a standalone Python file `reproducer.py` that reproduces the issue:

```python
import unittest
from django.db import models
from django.db.models import Q, F

class Book(models.Model):
    title = models.CharField(max_length=255)

class Author(models.Model):
    name = models.CharField(max_length=255)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

class FilteredRelationTest(unittest.TestCase):

    def test_with_join_exclude(self):
        self.assertSequenceEqual(
            Author.objects.annotate(
                book_alice=FilteredRelation('book', condition=Q(book__title__iexact='poem by alice')),
            ).exclude(book_alice__isnull=False),
            []
        )

if __name__ == '__main__':
    unittest.main()
```

To run the script, execute `python3 reproducer.py` in your terminal. The script should raise an `AssertionError` when the issue is present and print a stack trace of the issue.

Note: Make sure you have Django installed in your Python environment to run this script.