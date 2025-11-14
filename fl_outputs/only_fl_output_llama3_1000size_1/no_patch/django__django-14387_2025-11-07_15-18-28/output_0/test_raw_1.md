Here is the reproducer script:

```python
import django
from django.db import models as db_models

def jurisdiction_qs(for_jurisdiction):
    class Buss(db_models.Model):
        MAX_LENGTH = 25
        CHOICES = [('Universal', 'Universal'), ('GB', 'GB'), ('US', 'US'), ('Company', 'Company')]
        jurisdiction = db_models.CharField(max_length=MAX_LENGTH, choices=CHOICES)
        name = db_models.CharField(max_length=MAX_LENGTH)
        class Meta:
            unique_together = [('jurisdiction', 'name')]

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
        raise

if __name__ == "__main__":
    django.setup()
    main()
```

This script sets up a Django environment and then calls the `jurisdiction_qs` function with `'GB'` as an argument. It then tries to assert that the count of the resulting queryset filtered by `jurisdiction='GB'` is 8. If this assertion fails, it prints the stack trace using the provided function and raises the exception again.

To run the script, save it in a file named `reproducer.py`, navigate to the directory containing the file, and execute it with `python3 reproducer.py`.