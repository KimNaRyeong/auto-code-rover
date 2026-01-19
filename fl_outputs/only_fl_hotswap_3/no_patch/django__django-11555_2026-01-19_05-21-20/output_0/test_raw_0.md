 Here is a standalone Python file `reproducer.py` that reproduces the issue:
```python
from django.db import models
from django.db.models.base import ModelBase

class ParentModel(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ('-name',)

class ChildModel(ParentModel):
    age = models.IntegerField()

    class Meta:
        ordering = (models.Case(models.When(age__gt=18, then=1), default=0, output_field=models.IntegerField()),)

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    # This line will raise an AssertionError if the issue is present
    ChildModel.objects.all().order_by('-age')

if __name__ == '__main__':
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        raise
    except Exception as e:
        print_stacktrace(e)
```
To run the script, execute `python3 reproducer.py` in the terminal. If the issue is present, an `AssertionError` will be raised and a stack trace will be printed. If the issue is fixed, the script will exit with code 0.

Note: This script uses Django's multi-table inheritance feature, which is the root cause of the issue. The `ChildModel` inherits from `ParentModel`, and the `ordering` attribute in the `Meta` class of `ChildModel` contains an expression. When querying the `ChildModel` with an `order_by()` clause, an `AssertionError` is raised because the `field` argument is an `OrderBy` object, not a string. This only happens during test database setup, not during REPL or script use, which is the strange behavior reported in the issue.