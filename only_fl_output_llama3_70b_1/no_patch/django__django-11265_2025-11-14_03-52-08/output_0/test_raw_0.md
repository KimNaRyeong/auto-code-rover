Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'django.tests.filtered_relation.settings'

from django.db import models
from django.db.models.query_utils import Q
from django.test import TestCase
from django.db.models.fields.related import FilteredRelation

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)

class Author(models.Model):
    name = models.CharField(max_length=100)

def test_with_join_exclude():
    Author.objects.create(name='author1')
    Book.objects.create(title='poem by alice', author_id=1)

    annotated_qs = Author.objects.annotate(
        book_alice=FilteredRelation('book', condition=Q(book__title__iexact='poem by alice')),
    )

    try:
        result = annotated_qs.exclude(book_alice__isnull=False)
        assert len(result) == 0, "Exclude on annotated FilteredRelation does not work"
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Exclude on annotated FilteredRelation does not work")

if __name__ == '__main__':
    test_with_join_exclude()
```
This script creates a simple Django project with two models `Author` and `Book`, and then tries to reproduce the issue by annotating the `Author` queryset with a `FilteredRelation` and then excluding on that annotation. If the issue is present, it will raise an `AssertionError` with a stack trace of the error.