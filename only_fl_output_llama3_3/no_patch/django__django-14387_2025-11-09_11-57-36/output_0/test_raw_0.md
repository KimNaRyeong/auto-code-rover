Here is the reproducer script:

```python
import django
from django.db import models
from django.db.models import Q

django.setup()

class Buss(models.Model):
    MAX_LENGTH = 25
    CHOICES = [('Universal', 'Universal'), ('GB', 'GB'), ('US', 'US'), ('Company', 'Company')]
    jurisdiction = models.CharField(max_length=MAX_LENGTH, choices=CHOICES)
    name = models.CharField(max_length=MAX_LENGTH)

    class Meta:
        unique_together = [('jurisdiction', 'name')]

def jurisdiction_qs(for_jurisdiction):
    qs = Buss.objects.filter(jurisdiction=for_jurisdiction)
    if for_jurisdiction != 'Universal':
        qs = qs | Buss.objects.filter(jurisdiction='Universal').exclude(name__in=qs.values_list('name', flat=True))
    if for_jurisdiction != 'Company':
        qs = qs | Buss.objects.filter(jurisdiction='Company').exclude(name__in=qs.values_list('name', flat=True))
    return qs

def main():
    try:
        assert jurisdiction_qs('GB').filter(jurisdiction='GB').count() == 8
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)

if __name__ == '__main__':
    main()
```

This script sets up a Django project, defines the `Buss` model and the `jurisdiction_qs` function, and then attempts to reproduce the issue by asserting that the count of the filtered queryset is 8. If the assertion fails, it prints the stack trace using the provided function and exits with code 1.