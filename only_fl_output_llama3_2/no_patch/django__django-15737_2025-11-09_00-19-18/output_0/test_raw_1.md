Here is the reproducer script in a code block:

```python
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

try:
    from django.db import models

    class Parent(models.Model):
        name = models.CharField(max_length=255)

    class Child(models.Model):
        parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
        name = models.CharField(max_length=255)

    parent = Parent(name='parent_object')
    child = Child(parent=parent)
    parent.save()
    child.save()
    print(child.parent.name)  # This line should raise an AssertionError
except AssertionError as e:
    print_stacktrace(e)
    exit(0)
else:
    print("Issue not present. Exiting with code 0.")
    exit(0)

```

This script reproduces the issue by creating `Parent` and `Child` models, saving them to the database, and then trying to access the parent of a child object. If the issue is present, an `AssertionError` should be raised, which will trigger the print_stacktrace function and exit with code 0.