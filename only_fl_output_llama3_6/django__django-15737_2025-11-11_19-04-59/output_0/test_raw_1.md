Here is the reproducer script in a code block:

```python
import django
from django.db import models

def main():
    try:
        from .models import Parent, Child  # Try to import the models
    except ImportError as e:
        print_stacktrace(e)
        exit(1)

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

if __name__ == "__main__":
    main()
```

This script attempts to import the `Parent` and `Child` models. If the issue is present, this should raise an `ImportError` and print the stack trace using the provided function.