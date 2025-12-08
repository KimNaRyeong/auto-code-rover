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

    # Check the query
    if qs.query.select_related.related_fields != ["id", "trade_number", "country"]:
        raise AssertionError("Unexpected fields selected with defer() after only()")

    # Add another defer for "country" field
    qs = qs.defer("country")

    # Check the query
    if qs.query.select_related.related_fields != ["id", "trade_number", "country"]:
        raise AssertionError("Unexpected fields selected with multiple defer() after only()")

    # Create a queryset with only "name" and "country" fields
    qs = Company.objects.only("name", "country")

    # Add defer for "name" field
    qs = qs.defer("name")

    # Check the query
    if qs.query.select_related.related_fields != ["id", "country"]:
        raise AssertionError("Unexpected fields selected with defer() after only() with multiple fields")

if __name__ == "__main__":
    try:
        main()
        print("No issues found")
        sys.exit(0)
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
```
When executed with `python3 reproducer.py`, the script should raise an `AssertionError` and print a stack trace, indicating that the issue is present. The script should also exit with code 1.

If the issue is fixed, the script should print "No issues found" and exit with code 0.