Here is the reproducer script:

```python
import django
from django.db import models
from paiyroll.models import Buss

def jurisdiction_qs(for_jurisdiction):
    qs = Buss.objects.filter(jurisdiction=for_jurisdiction)
    if for_jurisdiction != 'Universal':
        qs = qs | Buss.objects.filter(jurisdiction='Universal').exclude(name__in=qs.values_list('name', flat=True))
    if for_jurisdiction != 'Company':
        qs = qs | Buss.objects.filter(jurisdiction='Company').exclude(name__in=qs.values_list('name', flat=True))
    return qs

def main():
    django.setup()
    
    try:
        jurisdiction_qs('GB')
        assert len(jurisdiction_qs('GB').filter(jurisdiction='US')) == 0
        assert len(jurisdiction_qs('GB').filter(jurisdiction='GB')) == 8
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == '__main__':
    main()
```

This script sets up the Django environment, defines the `jurisdiction_qs` function, and then attempts to reproduce the issue by calling `jurisdiction_qs('GB')`, filtering by `jurisdiction='US'`, and asserting that the result is 0. It also filters by `jurisdiction='GB'` and asserts that the result is 8. If either of these assertions fails, it prints a stack trace using the provided `print_stacktrace` function and raises an `AssertionError`.