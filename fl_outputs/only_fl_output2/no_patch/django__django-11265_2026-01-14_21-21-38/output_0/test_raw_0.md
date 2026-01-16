```python
import os
import sys
import django
from django.conf import settings
from django.db import models
from django.db.models import Q, FilteredRelation

# Define settings for Django to run standalone
def setup_django():
    settings.configure(
        DEBUG=True,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:",
            }
        },
        INSTALLED_APPS=("__main__",),
        USE_TZ=True,
    )
    django.setup()

# Models definition
class Author(models.Model):
    name = models.CharField(max_length=255)

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name="books", on_delete=models.CASCADE)

# Test function for the issue
def test_with_join_exclude():
    setup_django()

    # Migrations
    from django.db import connection
    with connection.schema_editor() as schema_editor:
        schema_editor.create_model(Author)
        schema_editor.create_model(Book)

    # Setup test data
    author1 = Author.objects.create(name="Alice")
    book1 = Book.objects.create(title="Poem by Alice", author=author1)

    try:
        result = Author.objects.annotate(
            book_alice=FilteredRelation('books', condition=Q(books__title__iexact='poem by alice')),
        ).exclude(book_alice__isnull=False)

        # Assert to trigger an AssertionError if fixed or show an error if present
        assert list(result) == [], "Expected empty queryset"
    
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

    print("Test passed. The issue has been fixed.")
    sys.exit(0)

# Helper function to print stack trace
def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

if __name__ == "__main__":
    test_with_join_exclude()
```