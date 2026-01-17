 Here is a standalone Python file `reproducer.py` to reproduce the issue:
```python
from django.core.exceptions import FieldError
from django.db import models
from django.db.models.query import FilteredRelation, Q, QuerySet
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

class FavoriteBook(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Author(models.Model):
    name = models.CharField(max_length=100)
    favorite_books = models.ManyToManyField(FavoriteBook, related_name='authors')

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
    user = User.objects.create(username='testuser')
    author1 = Author.objects.create(name='Author 1')
    author2 = Author.objects.create(name='Author 2')
    favorite_book1 = FavoriteBook.objects.create(user=user, content_object=author1)
    favorite_book2 = FavoriteBook.objects.create(user=user, content_object=author2)

    qs = Author.objects.annotate(
        book_alice=FilteredRelation('favorite_books', condition=Q(favorite_books__content_object__name__iexact='Author 1')),
    )

    try:
        result = list(qs.exclude(book_alice__isnull=False))
    except FieldError as e:
        print_stacktrace(e)
        raise AssertionError("Expected no FieldError, but got one")

    assert len(result) == 1
    assert result[0].name == 'Author 2'

if __name__ == "__main__":
    test_with_join_exclude()
    print("No FieldError raised, test passed.")
```
To execute the script, run `python3 reproducer.py`. The script should raise an `AssertionError` and print a stack trace of the issue.

The issue is caused by the `split_exclude` function in `django/db/models/sql/query.py`, which creates a new query without preserving the extra data from the original query. This results in a `FieldError` when trying to use the `exclude` method on a queryset with an annotated `FilteredRelation`.