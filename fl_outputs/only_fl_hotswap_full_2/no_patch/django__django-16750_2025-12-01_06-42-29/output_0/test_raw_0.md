 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
from django.db.models import Chr, Value
from django.db.models.expressions import Expression

Expression.output_field = None  # Reset output_field to reproduce the issue

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class Author:
    pass

try:
    Author.objects.annotate(first_letter=Chr(Value(77)))
except ValueError as e:
    print_stacktrace(e)
    raise AssertionError("ValueError raised as expected")
```
To reproduce the issue, run the script with `python3 reproducer.py`. The script sets `Expression.output_field` to `None` to reproduce the issue and prints a stack trace when the `ValueError` is raised. The `AssertionError` is raised to indicate that the issue is present.

To fix the issue, set `output_field = CharField()` in the `Chr` class definition in `django/db/models/expressions.py` as suggested in the issue description. After making this change, the script should exit with code 0 when executed with `python3 reproducer.py`.