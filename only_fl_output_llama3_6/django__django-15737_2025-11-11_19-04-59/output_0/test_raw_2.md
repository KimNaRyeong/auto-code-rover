Here is the reproducer script in a code block:

```python
import django
from django.db import models

def main():
    class Parent(models.Model):
        name = models.CharField(max_length=255)

    class Child(models.Model):
        parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
        name = models.CharField(max_length=255)

    def reproduce_issue():
        parent = Parent(name='parent_object')
        child = Child(parent=parent)
        parent.save()
        child.save()
        assert child.parent.name == 'parent_object'
        print_stacktrace(AssertionError("Issue not reproduced"))

    reproduce_issue()

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

if __name__ == "__main__":
    main()
```

This script defines two Django models, `Parent` and `Child`, with a foreign key relationship. The `reproduce_issue` function creates instances of these models, saves them to the database, and then attempts to access the parent object through the child object. If the issue is present, this should raise an `AssertionError` and print the stack trace using the provided function.