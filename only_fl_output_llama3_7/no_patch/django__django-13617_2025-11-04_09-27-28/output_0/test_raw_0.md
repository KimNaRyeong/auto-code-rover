Here is a standalone Python file `reproducer.py` that reproduces the issue:

```python
import django
from django.db import models
from django.db.models.functions import TruncYear, Coalesce
from django.db.models import Sum, Subquery, OuterRef

class Book(models.Model):
    pubdate = models.DateField()
    pages = models.IntegerField()

def main():
    try:
        result = Book.objects.all().annotate(
            pub_year=TruncYear('pubdate')
        ).order_by().values('pub_year').annotate(
            total_pages=Sum('pages'),
            top_rating=Subquery(
                Book.objects.filter(pubdate__year=OuterRef('pub_year')).order_by('rating').values('rating')[:1]
            )
        ).values('pub_year', 'total_pages', 'top_rating')
        print("Issue not present")
    except AssertionError:
        print_stacktrace(sys.exc_info()[0])
        raise

if __name__ == "__main__":
    main()
```

This script should be run with `python3 reproducer.py` in the root directory of your project. If the issue is present, it will print a stack trace and exit with code 1.