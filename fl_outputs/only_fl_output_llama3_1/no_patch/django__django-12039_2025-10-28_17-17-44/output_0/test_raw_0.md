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

        index = models.Index(fields=['-name'], name='idx')
        if 'text_pattern_ops' in str(index.create_sql()):
            raise AssertionError("Expected whitespace to be removed")
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    django.setup()
    reproduce_issue()
```

You can run this script by executing `python3 reproducer.py` in the root directory of your project. If the issue is present, it will raise an `AssertionError`, print a stack trace, and exit with code 1.