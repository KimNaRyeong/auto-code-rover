Here is a standalone Python file `reproducer.py` to reproduce the issue:
```
from django.db import models
from django.conf import settings

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

class MyModel(models.Model):
    some_field = models.CharField(max_length=255)

try:
    # Try to use an expression in a filter call
    MyModel.objects.filter(F('some_field').lower() == 'anssi')
    # If the issue is fixed, this should not raise an exception
    print("Issue is fixed!")
    exit(0)
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Expressions in filter calls are not allowed")

if __name__ == "__main__":
    settings.configure()
    models.setup_test_environment()
```
<|start_header_id|>