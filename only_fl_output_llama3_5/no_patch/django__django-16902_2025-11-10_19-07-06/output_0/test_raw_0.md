Here is the reproducer script:

```python
import django
from django.db import models
from django.db.models.functions import Right, Length

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
    class MyModel(models.Model):
        foo = models.CharField(max_length=255)

    my_model = MyModel(foo='hello')
    result = my_model.annotate(suffix=models.functions.Right(my_model.foo, models.functions.Length(my_model.foo) - models.functions.Length(my_model.foo))).values('suffix')

    if 'hello' in [row['suffix'] for row in result]:
        raise AssertionError("RIGHT function on Oracle and SQLite returns improper value when the length is zero.")

if __name__ == "__main__":
    try:
        reproduce_issue()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        print("Issue not present. Exiting with code 0.")
        exit(0)
```

This script creates a simple Django model, populates it with some data, and then uses the `Right` function to annotate the model instance. It checks if the result is as expected (i.e., an empty string) and raises an `AssertionError` if not. The script also prints the stack trace of the error using the provided `print_stacktrace` function.