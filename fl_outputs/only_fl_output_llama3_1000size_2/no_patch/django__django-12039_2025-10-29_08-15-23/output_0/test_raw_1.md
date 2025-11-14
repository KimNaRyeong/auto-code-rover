Here is the standalone Python file `reproducer.py` that reproduces the issue:

```python
import django
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

def reproduce_issue():
    try:
        index = models.Index(fields=['-name'], name='idx', opclasses=['text_pattern_ops'])
        if " DESC" not in str(index.create_sql()):
            raise AssertionError("Expected ' DESC' suffix")
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    reproduce_issue()
```

This script creates a Django index with the specified fields and opclasses, then checks if the created SQL contains the expected " DESC" suffix. If not, it raises an `AssertionError` and prints the stack trace using the provided function.