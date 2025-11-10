Here is the reproducer script:

```python
import django
from django.db import models

def main():
    try:
        class Company(models.Model):
            id = models.IntegerField()
            name = models.CharField(max_length=255)
            trade_number = models.CharField(max_length=255)
            country = models.CharField(max_length=255)

        query1 = Company.objects.only("name").defer("name")
        if query1.query != "SELECT \"company\".\"id\", \"company\".\"country\" FROM \"company\"":
            raise AssertionError("Expected only 'id' and 'country' columns to be selected, but got unexpected columns.")

        query2 = Company.objects.only("name", "country").defer("name")
        if query2.query != "SELECT \"company\".\"id\", \"company\".\"country\" FROM \"company\"":
            raise AssertionError("Expected only 'id' and 'country' columns to be selected, but got unexpected columns.")

    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

    else:
        print("Test passed. No unexpected columns were selected.")
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

This script creates a custom model, then uses the `only` and `defer` methods to test the expected behavior. If the queries do not match the expected results, it raises an `AssertionError`. The `print_stacktrace` function is used to print the stack trace of the error.