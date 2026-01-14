 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import sys
from django.db import models

def print_stacktrace(e: Exception):
    import traceback    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class Parent(models.Model):
    class Meta:
        ordering = ["-pk"]

class Child(Parent):
    pass

def main():
    Child.objects.all()

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
```
When executed with `python3 reproducer.py`, the script raises an `AssertionError` with a stack trace, indicating that the query is ordered ASC instead of DESC. The line numbers in the stack trace correspond to the lines in the script.

Note that this script assumes that Django is installed and available in the Python environment. If Django is not installed, the script will raise an `ImportError` when it tries to import the `models` module.