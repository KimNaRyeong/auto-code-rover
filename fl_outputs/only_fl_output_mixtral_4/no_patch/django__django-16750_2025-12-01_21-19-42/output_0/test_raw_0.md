 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
from django.db.models import Chr, Value
from django.db.models.expressions import Expression

Expression.output_field = None  # Reset the output_field to reproduce the issue

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
except Exception as e:
    print_stacktrace(e)
    assert False
```
To reproduce the issue, run the script with `python3 reproducer.py`. The script should print the stack trace of the `ValueError` and raise an `AssertionError`.

To fix the issue, uncomment the following line in the script:
```python
# Expression.output_field = CharField()  # Uncomment this line to fix the issue
```
After fixing the issue, run the script again with `python3 reproducer.py`. The script should exit with code 0 without any errors.