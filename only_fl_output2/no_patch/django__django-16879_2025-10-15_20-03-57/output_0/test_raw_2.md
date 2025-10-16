To create a standalone `reproducer.py` Python script that will correctly instantiate a Django environment, define necessary models, and execute an aggregation query leading to the specified issue, follow the instructions closely. This script accounts for the correct setup of Django to avoid common pitfalls regarding `INSTALLED_APPS` configuration and database setup:

```python
# reproducer.py

import os
import sys
import django
from django.conf import settings
from django.db import models
from django.db.models import F, Sum, Case, When, FloatField, Count, OuterRef, Subquery
from django.db.models.functions import Round

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

def setup_django():
    settings.configure(
        DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'mydatabase',
            }
        },
        INSTALLED_APPS=(
            '__main__',  # This app is included to make the script self-contained
        ),
        TIME_ZONE='UTC',
    )
    django.setup()
    # This creates the database schema.
    from django.core.management import call_command
    call_command('migrate', verbosity=0)

def run_test():
    try:
        total_books_qs = (
            Book.objects.filter(authors__pk=OuterRef("pk"))
            .order_by()
            .values("pk")
            .annotate(total=Count("pk"))
            .values("total")
        )
        
        annotated_authors = Author.objects.annotate(
            total_books=Subquery(total_books_qs.annotate(
                total_books=F("total")
            ).values("total_books")),
            total_books_a=Subquery(total_books_qs.filter(
                title__istartswith="a"
            ).annotate(
                total_books_a=F("total")
            ).values("total_books_a")),
        ).values(
            "pk",
            "total_books",
            "total_books_a",
        ).order_by("-total_books")
        
        totals = annotated_authors.aggregate(
            sum_total_books=Sum("total_books"),
            sum_total_books_a=Sum("total_books_a"),
            a_over_total_rate=Case(
                When(
                    sum_total_books=0,
                    then=0,
                ),
                default=Round(
                    (Sum("total_books_a") / Sum("total_books")) * 100, 2
                ),
                output_field=FloatField(),
            ),
        )

        assert totals['sum_total_books'] is not None, "sum_total_books is None"
        assert totals['sum_total_books_a'] is not None, "sum_total_books_a is None"
        assert 'a_over_total_rate' in totals, "a_over_total_rate computation failed"
        print("Test Passed: Issue is not present.")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

class Author(models.Model):
    name = models.CharField(max_length=100)

class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author)

if __name__ == '__main__':
    setup_django()
    
    try:
        run_test()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
```

Remember, this script is designed to be run in a Django-project-like environment where you manage Django settings dynamically within the script. This approach circumvents the need to have a complete Django project structure for the sole purpose of reproducing the bug, making it highly suitable for quick tests or demonstrations of specific issues.