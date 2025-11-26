Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'

from django.test import TestCase
from django.db.models import Q, F
from django.db.models.query_utils import FilteredRelation

class Author(models.Model):
    name = models.CharField(max_length=100)

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

def test_with_join_exclude():
    Author.objects.create(name='author1')
    Book.objects.create(title='poem by alice', author=Author.objects.get(name='author1'))

    annotated_authors = Author.objects.annotate(
        book_alice=FilteredRelation('book', condition=Q(book__title__iexact='poem by alice')),
    ).exclude(book_alice__isnull=False)

    try:
        authors = list(annotated_authors)
        assert len(authors) == 0
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue is present")

if __name__ == '__main__':
    test_with_join_exclude()
```
This script creates a simple Django project with two models, `Author` and `Book`, and then tries to reproduce the issue by annotating the `Author` model with a filtered relation and excluding authors where the annotated field is not null. If the issue is present, it will raise an `AssertionError` and print the stack trace of the error.