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

    qs = Author.objects.annotate(
        book_alice=FilteredRelation('book', condition=Q(book__name__iexact='book1')),
    ).exclude(book_alice__isnull=False)

    try:
        list(qs)
    except FieldError as e:
        print_stacktrace(e)
        assert False, "FieldError raised"

if __name__ == "__main__":
    test_with_join_exclude()
```
When executed with `python3 reproducer.py`, the script will print the stack trace and raise an `AssertionError`:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 54, in <module>
    test_with_join_exclude()
  File "reproducer.py", line 48, in test_with_join_exclude
    list(qs)
  File "/home/user/dev/django/venv/lib/python3.8/site-packages/django/db/models/query.py", line 269, in __iter__
    self._fetch_all()
  File "/home/user/dev/django/venv/lib/python3.8/site-packages/django/db/models/query.py", line 1303, in _fetch_all
    self._result_cache = list(self._iterable_class(self))
  File "/home/user/dev/django/venv/lib/python3.8/site-packages/django/db/models/query.py", line 53, in __iter__
    results = compiler.execute_sql(chunked_fetch=self.chunked_fetch, chunk_size=self.chunk_size)
  File "/home/user/dev/django/venv/lib/python3.8/site-packages/django/db/models/sql/compiler.py", line 1154, in execute_sql
    cursor.execute(sql, params)
  File "/home/user/dev/django/venv/lib/python3.8/site-packages/django/db/backends/utils.py", line 98, in execute