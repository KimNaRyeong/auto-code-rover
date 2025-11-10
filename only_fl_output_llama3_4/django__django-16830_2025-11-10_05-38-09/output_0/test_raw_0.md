Here is the reproducer script:

```python
import django
from django.db import models
from django.test import TestCase

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

class Reproducer(TestCase):
    def test_force_insert_flag(self):
        class ParentModel(models.Model):
            id = models.BigIntegerField(primary_key=True)

        class ChildModel(ParentModel):
            pass

        try:
            child_model = ChildModel(id=1)
            child_model.save(force_insert=True)
        except Exception as e:
            print_stacktrace(e)
            raise
        else:
            exit(0)

if __name__ == "__main__":
    django.setup()
    Reproducer().run_tests()
```

This script sets up a Django test case, defines the `ParentModel` and `ChildModel`, creates an instance of `ChildModel`, and attempts to save it with the `force_insert=True` flag. If any exception occurs during this process, it prints the stack trace using the provided function and then raises the exception again.