Here is the reproducer script:

```python
import django
from django.db import models
from django.db.models import Q

def jurisdiction_qs(for_jurisdiction):
    qs = Buss.objects.filter(jurisdiction=for_jurisdiction)
    if for_jurisdiction != 'Universal':
        qs = qs | Buss.objects.filter(jurisdiction='Universal').exclude(name__in=qs.values_list('name', flat=True))
    if for_jurisdiction != 'Company':
        qs = qs | Buss.objects.filter(jurisdiction='Company').exclude(name__in=qs.values_list('name', flat=True))
    return qs

def main():
    try:
        result = jurisdiction_qs('GB').filter(jurisdiction='GB').count()
        assert result == 8, "Expected count to be 8 but got {}".format(result)
    except AssertionError as e:
        print_stacktrace(e)
        raise
    finally:
        if not isinstance(e, AssertionError):
            print("Issue fixed. Exiting with code 0.")
            exit(0)

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

django.setup()

if __name__ == '__main__':
    main()
```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue.