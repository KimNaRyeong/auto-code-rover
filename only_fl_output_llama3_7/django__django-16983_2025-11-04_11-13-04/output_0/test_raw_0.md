Here is the reproducer script:

```python
import django
from django.db import models
from django.contrib.admin import ModelAdmin
from django.contrib import admin

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

def main():
    try:
        class Book(models.Model):
            pass

        class Author(models.Model):
            books = models.ManyToManyField(Book, through='BookAuthor')

        class BookAuthor(models.Model):
            book = models.ForeignKey(Book, on_delete=models.CASCADE)
            author = models.ForeignKey(Author, on_delete=models.CASCADE)

        admin.site.register(Book)
        admin.site.register(Author)

        admin.ModelAdmin.filter_horizontal([Author])
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        print("Issue not present")
        exit(0)

if __name__ == "__main__":
    main()
```

This script creates a simple Django model with a ManyToManyField using an intermediary model. It then attempts to use the `filter_horizontal` method on the `Author` model, which should raise an `AssertionError` if the issue is present. The script prints the stack trace of the error and exits with code 1. If the issue is not present, it simply prints a message and exits with code 0.