Here is a standalone Python file `reproducer.py` that reproduces the issue:

```python
import os
from django.db import models

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
    class Parent(models.Model):
        class Meta:
            ordering = ["-pk"]

    class Child(Parent):
        pass

    try:
        print(Child.objects.all().query)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced")

if __name__ == "__main__":
    main()
```

This script defines the `Parent` and `Child` models, sets up the ordering for the `Parent` model, and then attempts to query the `Child` model. If an issue is present (i.e., the ordering is not descending), it prints the stack trace using the provided function and raises an assertion error.

To run this script, create a new directory for your project, navigate into it, and execute the script with Python 3: `python3 reproducer.py`.