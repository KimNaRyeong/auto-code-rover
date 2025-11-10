Here is the reproducer script:

```python
import django
from django.db import models
from django.core.exceptions import ImproperlyConfigured

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

def main():
    try:
        from django.db import models
        class OurModel(models.Model):
            our_field = models.JSONField()

        first_filter = {'our_field__key__in': [0]}
        first_items = OurModel.objects.filter(**first_filter)
        if len(first_items) != 0:
            raise AssertionError("Expected no items, but got {}".format(len(first_items)))

        second_filter = {'our_field__key': 0}
        second_items = OurModel.objects.filter(**second_filter)
        if len(second_items) != 312:
            raise AssertionError("Expected 312 items, but got {}".format(len(second_items)))
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        print("Issue not present. Exiting with code 0.")
        exit(0)

if __name__ == '__main__':
    main()
```

This script should be executed by `python3 reproducer.py` and it will raise an `AssertionError` when the issue is present, printing a stack trace of the issue.