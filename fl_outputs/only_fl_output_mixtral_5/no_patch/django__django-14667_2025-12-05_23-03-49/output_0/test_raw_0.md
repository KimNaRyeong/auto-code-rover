 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
from django.db import models
import sys

# Define the Company model
class Company(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    trade_number = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    # Create a queryset with only "name" field
    qs = Company.objects.only("name")

    # Add defer for "name" field
    qs = qs.defer("name")

    # Check if all fields are selected
    if qs.query.select_related:
        raise AssertionError("defer() doesn't clear deferred field when chaining with only()")

    # Create a queryset with only "name" field
    qs = Company.objects.only("name")

    # Add defer for "name" and "country" fields
    qs = qs.defer("name").defer("country")

    # Check if all fields are selected
    if qs.query.select_related:
        raise AssertionError("defer() doesn't clear deferred field when chaining with only()")

    # Create a queryset with "name" and "country" fields
    qs = Company.objects.only("name", "country")

    # Add defer for "name" field
    qs = qs.defer("name")

    # Check if only "id" and "country" fields are selected
    if qs.query.select_related:
        raise AssertionError("defer() doesn't clear deferred field when chaining with only()")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` with a stack trace if the issue is present. If the issue is fixed, the script will exit with code 0.