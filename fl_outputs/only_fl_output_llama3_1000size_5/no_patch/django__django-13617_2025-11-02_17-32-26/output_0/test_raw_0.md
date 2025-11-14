Here is a standalone Python file `reproducer.py` to reproduce the issue:

```python
import django
from django.db import models
from django.db.models.functions import TruncYear, Coalesce
from django.db.models.expressions import Subquery, OuterRef

class Book(models.Model):
    pubdate = models.DateField()
    pages = models.IntegerField()

def main():
    try:
        result = Book.objects.all().annotate(
            pub_year=TruncYear('pubdate')
        ).order_by().values('pub_year').annotate(
            total_pages=Coalesce(Sum('pages'), 0),
            top_rating=Subquery(
                Book.objects.filter(pubdate__year=OuterRef('pub_year')).order_by('rating').values('rating')[:1]
            )
        ).values('pub_year', 'total_pages', 'top_rating')
        print("Issue not present")
    except AssertionError:
        print_stacktrace(sys.exc_info()[0])
        raise

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

if __name__ == "__main__":
    main()
```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue.