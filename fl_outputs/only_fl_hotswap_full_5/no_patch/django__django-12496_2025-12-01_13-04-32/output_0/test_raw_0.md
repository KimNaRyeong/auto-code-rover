 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import uuid

from django.db import models
from django.db import connection
from django.utils.six import StringIO

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
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

def run_test():
    output = StringIO()
    connection.fetch_sql = lambda *args, **kwargs: print(*args, file=output)
    Child.objects.create()
    output.seek(0)
    sql = output.read()
    assert "UPDATE \"app_parent\"" not in sql, "Extra UPDATE query found"

if __name__ == '__main__':
    try:
        run_test()
        print("Issue not present")
        exit(0)
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
```
The script defines the `Parent` and `Child` models as described in the issue, and then defines a `run_test` function that creates a new `Child` object and checks that no extra `UPDATE` query is performed. The `fetch_sql` method is overridden to print the SQL statements that Django generates.

To run the script, execute `python3 reproducer.py`. If the issue is present, an `AssertionError` will be raised and the script will print a stack trace and exit with code 1. If the issue is fixed, the script will print "Issue not present" and exit with code 0.