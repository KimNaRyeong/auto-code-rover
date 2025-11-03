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
        django.db.models.options.configure()
        create_index_sql = index.create_sql()
        if " DESC" not in create_index_sql:
            raise AssertionError("Expected 'DESC' suffix")
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    reproduce_issue()
```

To run the script, execute `python3 reproducer.py` from the root directory of your project. If the issue is present, it should raise an `AssertionError`, print a stack trace, and exit with code 1.