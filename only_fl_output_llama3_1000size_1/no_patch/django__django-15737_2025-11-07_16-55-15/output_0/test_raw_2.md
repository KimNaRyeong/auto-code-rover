Here is the reproducer script:

```python
import django
from django.db import models

def main():
    try:
        from django.db.models.fields.related import ForeignKeyDeferredAttribute
        class Parent(models.Model):
            name = models.CharField(max_length=255)

        class Child(models.Model):
            parent = models.ForeignKey(Parent, on_delete=models.CASCADE)

        parent = Parent(name='parent_object')
        child = Child(parent=parent)
        parent.save()
        child.save()
        print(child.parent.name)  # This should raise an AssertionError
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        print("Issue not present")
        exit(0)

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
    django.setup()
    main()

```

This script should be run with `python3 reproducer.py`. It will create a Parent and Child model, save them to the database, and then try to access the parent's name. If the issue is present, it will raise an AssertionError and print the stack trace.