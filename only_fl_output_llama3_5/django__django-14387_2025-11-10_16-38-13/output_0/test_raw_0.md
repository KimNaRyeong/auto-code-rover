Here is the reproducer script:

```python
import django
from django.db import models
from django.db.models import Q

def jurisdiction_qs(for_jurisdiction):
    qs = models.Buss.objects.filter(jurisdiction=for_jurisdiction)
    if for_jurisdiction != 'Universal':
        qs = qs | models.Buss.objects.filter(jurisdiction='Universal').exclude(name__in=qs.values_list('name', flat=True))
    if for_jurisdiction != 'Company':
        qs = qs | models.Buss.objects.filter(jurisdiction='Company').exclude(name__in=qs.values_list('name', flat=True))
    return qs

def main():
    django.setup()
    Buss.MAX_LENGTH = 25
    Buss.CHOICES = [('Universal', 'Universal'), ('GB', 'GB'), ('US', 'US'), ('Company', 'Company')]
    Buss._meta.unique_together = [('jurisdiction', 'name')]

    try:
        qs = jurisdiction_qs('GB')
        assert len(qs.filter(jurisdiction='GB')) == 8
    except AssertionError as e:
        print_stacktrace(e)
        raise

    if __name__ == '__main__':
        main()
```

This script sets up the Django environment, defines the `Buss` model and the `jurisdiction_qs` function, and then attempts to reproduce the issue by calling `jurisdiction_qs('GB')` and asserting that the result of filtering by `jurisdiction='GB'` is 8. If the assertion fails, it prints a stack trace using the provided `print_stacktrace` function and raises an `AssertionError`.