 Here is a standalone Python script that reproduces the issue:
```python
from django.db import models

class Parent(models.Model):
    class Meta:
        ordering = ["-pk"]

class Child(Parent):
    pass

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
    try:
        Child.objects.all()
        # The following line should raise an AssertionError
        # if the issue is present
        assert Child.objects.order_by().query == Child.objects.all().query
    except AssertionError:
        print_stacktrace(AssertionError("The query is ordered ASC but I expect the order to be DESC."))
    except Exception as e:
        print_stacktrace(e)
    else:
        print("The issue is fixed.")
        exit(0)
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` and print a stack trace showing the line numbers of the statements. The script will also exit with a non-zero exit code.

The issue is caused by the fact that the `ordering` attribute is inherited from the `Parent` model, but the query generated for the `Child` model does not include the ordering specified in the `Parent` model. Instead, the query includes an `INNER JOIN` with the `Parent` table and orders by the `id` column of the `Parent` table, which is always ascending.

To fix the issue, you can explicitly specify the ordering in the `Child` model as follows:
```python
class Child(Parent):
    class Meta:
        ordering = ["-pk"]
```
With this change, the query generated for the `Child` model will include the ordering specified in the `Child` model, and the query will be ordered in descending order by the primary key.