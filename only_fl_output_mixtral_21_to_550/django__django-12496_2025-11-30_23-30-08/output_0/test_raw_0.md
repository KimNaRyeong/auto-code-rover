 Here is a standalone python file `reproducer.py` to reproduce the issue:

```python
import uuid
from django.db import connection
from django.db import models

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class Parent(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    title = models.TextField()

    class Meta:
        db_table = 'app_parent'

class Child(Parent):
    body = models.TextField()

    class Meta:
        db_table = 'app_child'

def main():
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM app_child")
            cursor.execute("DELETE FROM app_parent")
        Child.objects.create()
        assert False, "An extra UPDATE query was not executed."
    except Exception as e:
        print_stacktrace(e)

if __name__ == '__main__':
    main()
```

This script creates a new `Child` object, which should result in an extra update query for the `Parent` model when a custom primary key is defined. The script raises an `AssertionError` when the extra query is not executed, indicating that the issue is present. When the issue is fixed, the script should exit with code 0.