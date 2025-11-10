Here is the reproducer script in a code block:

```python
import django
from django.db import models

django.setup()

class Parent(models.Model):
    name = models.CharField(max_length=255)

class Child(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

def main():
    try:
        parent = Parent(name='parent_object')
        child = Child(parent=parent)
        parent.save()
        child.save()
        print(child.parent.name)  # This line should raise an AssertionError
    except AssertionError as e:
        print_stacktrace(e)
        exit(0)

if __name__ == "__main__":
    main()

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
```

To run the script, save it to a file named `reproducer.py` and execute it with Python 3: `python3 reproducer.py`.