Here is the reproducer script:

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
        class MyModel(models.Model):
            name = models.CharField(max_length=255)

        index = models.Index(fields=['-name'], name='idx', opclasses=['text_pattern_ops'])
        create_index_sql = str(index.create_sql())
        if "  " in create_index_sql:
            raise AssertionError("Expected whitespace is not present")
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    django.setup()
    reproduce_issue()
```

This script sets up the Django environment using `django.setup()` before attempting to create an index.