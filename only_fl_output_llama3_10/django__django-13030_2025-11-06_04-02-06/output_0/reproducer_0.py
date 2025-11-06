import django
from django.db import models, connection
from django.core.exceptions import AssertionError

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

def reproduce_issue():
    from example.core.models import Author, Book
    a1 = Author.objects.create()
    Book.objects.create(author=a1)
    Book.objects.create(author=None)
    try:
        Book.objects.prefetch_related('author')
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue not fixed")

if __name__ == "__main__":
    django.setup()
    reproduce_issue()
