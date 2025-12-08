 Here is a standalone Python file `reproducer.py` that reproduces the issue:
```python
from django.core.exceptions import FieldError
from django.db import models
from django.db.models.query import FilteredRelation, Q, QuerySet
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

class FavoriteBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'book',)

class Book(models.Model):
    name = models.CharField(max_length=100)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def test_with_join_exclude():
    user1 = User.objects.create(username='user1')
    book1 = Book.objects.create(name='book1')
    book2 = Book.objects.create(name='book2')
    FavoriteBook.objects.create(user=user1, book=book1)

    qs = User.objects.annotate(
        favorite_books=FilteredRelation(
            'favoritebook_set',
            condition=Q(favoritebook_set__book__name='book1')
        )
    )

    try:
        qs.exclude(favorite_books__isnull=False)
    except FieldError as e:
        print_stacktrace(e)
        raise AssertionError("Expected no FieldError, but got one")

if __name__ == "__main__":
    test_with_join_exclude()
    print("No FieldError raised, test passed.")
```
When executed with `python3 reproducer.py`, the script will print the stack trace of the `FieldError` and raise an `AssertionError`. This reproduces the issue described in the original post.

Note that the code above assumes that the `Book` and `User` models are defined in the project, and that the `FilteredRelation` class is available from `django.db.models.query`. If these assumptions are not met, the script may not work as expected.