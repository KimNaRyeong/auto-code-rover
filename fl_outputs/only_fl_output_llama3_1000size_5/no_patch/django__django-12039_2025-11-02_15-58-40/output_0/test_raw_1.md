Here is the standalone Python file `reproducer.py` to reproduce the issue:

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
        create_index_sql = f"CREATE INDEX {index.name} ON {MyModel._meta.db_table} ({'-name' if index.ordering else 'name'}{f' DESC' if index.ordering else ''}{f' {index.opclass}' if index.opclass else ''})"
        if " DESC" not in create_index_sql:
            raise AssertionError("Expected 'DESC' suffix")
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    reproduce_issue()
```

This script should raise an `AssertionError` when the issue is present and print a stack trace.