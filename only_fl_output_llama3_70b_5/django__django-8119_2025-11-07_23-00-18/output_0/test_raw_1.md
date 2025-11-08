Here is a standalone Python file `reproducer.py` to reproduce the issue:
```
from django.db import models
from django.db.models import F, Q

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
    # This should raise an error if the issue is present
    MyModel.objects.filter(F('some_field').lower() == 'anssi')
    print("Issue is fixed!")
    exit(0)
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Issue is still present")
```
This script defines a Django model and attempts to use an expression in a `.filter()` call. If the issue is present, it should raise an error, which will be caught and printed with a stack trace using the `print_stacktrace` function. If no error is raised, it means the issue is fixed, and the script will exit with code 0.

To run this script, save it to a file named `reproducer.py` in the root directory of your project, then execute it with `python3 reproducer.py`.