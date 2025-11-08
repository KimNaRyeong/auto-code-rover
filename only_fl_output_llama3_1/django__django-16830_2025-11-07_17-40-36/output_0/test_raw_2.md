Here is the reproducer script:

```python
import django
from django.db import models

django.setup()

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

class ParentModel(models.Model):
    id = models.BigIntegerField(primary_key=True)

class ChildModel(ParentModel):
    pass

def main():
    try:
        child_model = ChildModel(id=1)
        child_model.save(force_insert=True)
        print("Expected UPDATE statement not executed")
    except AssertionError as e:
        print_stacktrace(e)
        raise
    else:
        print("Test passed, no issue found")
        exit(0)

if __name__ == "__main__":
    main()
```

This script sets up a Django project, defines the `ParentModel` and `ChildModel`, creates an instance of `ChildModel`, and then tries to save it with the `force_insert=True`. If the issue is present, it will print the stack trace and raise an `AssertionError`.