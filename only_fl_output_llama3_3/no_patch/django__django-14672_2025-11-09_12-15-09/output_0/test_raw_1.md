Here is the reproducer script:

```python
import os
import sys
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
    try:
        from models import Parent, ProxyParent, Child, ManyToManyModel
        make_hashable = models.make_hashable
        many_to_many_field = Child.many_to_many_field.through_fields
        if isinstance(many_to_many_field, list):
            raise AssertionError("TypeError: unhashable type: 'list'")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == '__main__':
    main()
```

This script tries to reproduce the issue by importing the models and checking if `many_to_many_field.through_fields` is a list. If it is, an AssertionError is raised with the message "TypeError: unhashable type: 'list'". The stack trace of this error is then printed and the script exits with code 1.

Please note that you need to have Django installed in your Python environment for this script to run correctly.