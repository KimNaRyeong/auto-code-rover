Here is the reproducer script:

```python
import django
from django.db import models
from django.db.models import Q

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
        import django
        from django.db import models

        class SomeModel(models.Model):
            some_foreign_key = models.ForeignKey('SomeOtherModel', on_delete=models.CASCADE)

        django.setup()
        SomeModel.objects.all().order_by("some_foreign_key__non_existing_field")
        assert False, "Expected FieldError"
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    main()
```

This script sets up Django before attempting to order the query set by a non-existent field on the related model.