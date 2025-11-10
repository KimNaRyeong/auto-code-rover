Here is the reproducer script:

```python
import os
from django.db import models
from django.core.exceptions import AssertionError

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
    os.system('python manage.py makemigrations')
    os.system('python manage.py migrate')

    class Node(models.Model):
        id = models.BigIntegerField(primary_key=True)
        point = None

    class Relation(models.Model):
        id = models.BigIntegerField(primary_key=True)
        nodes = models.ManyToManyField(Node)

    try:
        reproduce_issue()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        print("Issue not present")
        exit(0)

if __name__ == "__main__":
    reproduce_issue()
```

This script creates two Django models, `Node` and `Relation`, with a Many-To-Many relationship. The `reproduce_issue` function attempts to create the migration files for these models using the `makemigrations` and `migrate` commands. If an `AssertionError` is raised during this process, it means that the issue is present and the script prints the stack trace of the error.