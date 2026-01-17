 Here is a standalone Python file `reproducer.py` that reproduces the issue:
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

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

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
    book1 = Book.objects.create(title='Book 1', author=author1)
    book2 = Book.objects.create(title='Book 2', author=author2)
    FavoriteBook.objects.create(user=user, content_object=book1)

    try:
        queryset = Author.objects.annotate(
            book_alice=FilteredRelation('book', condition=Q(book__title__iexact='Book 1')),
        ).exclude(book_alice__isnull=False)

        # The following assertion will fail, causing an AssertionError to be raised
        assert len(queryset) == 1
        assert queryset[0] == author2

    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == '__main__':
    test_with_join_exclude()
```
To run the script, save it in the root directory of your Django project and execute it with `python3 reproducer.py`. The script will print a stack trace and raise an `AssertionError` if the issue is present. If the issue is fixed, the script will exit with code 0.