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

def test_reproducer():
    try:
        result = jurisdiction_qs('GB').filter(jurisdiction='GB').count()
        if result != 8:
            raise AssertionError("Expected count to be 8, but got {}".format(result))
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    test_reproducer()

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
```

This script sets up a Django project, defines the `Buss` model and the `jurisdiction_qs` function, and then tests whether the issue is present. If the issue is present, it prints the stack trace and exits with code 1.