Here is the reproducer script in a code block:

```python
import django
from django.db import models

def main():
    try:
        from django.db.models import Q
        from django.db.models.expressions import F
    except ImportError as e:
        print_stacktrace(e)
        exit(1)

    class Company(models.Model):
        id = models.IntegerField()
        name = models.CharField(max_length=255)
        trade_number = models.CharField(max_length=255)
        country = models.CharField(max_length=255)

    try:
        # Reproduce the issue
        queryset1 = Company.objects.only("name").defer("name")
        queryset2 = Company.objects.only("name", "country").defer("name")

        # Check if the querysets return unexpected fields
        assert set(queryset1.query.columns) == {"company.id", "company.name"}
        assert set(queryset2.query.columns) == {"company.id", "company.name", "company.country"}

    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

    # If the issue is fixed, exit with code 0
    else:
        print("Issue not present")
        exit(0)

if __name__ == "__main__":
    main()
```

This script first tries to import `Q` and `F` from Django's ORM. If this fails (which it should), it prints the stack trace of the `ImportError` and exits with code 1. Then, it defines a `Company` model and attempts to reproduce the issue by creating two querysets: one that uses `.only()` and then `.defer()`, and another that uses `.only()` with multiple fields and then `.defer()`. It checks if the generated SQL queries return unexpected fields, and if they do, it prints the stack trace of the `AssertionError` and exits with code 1. If the issue is not present, it prints a message indicating that the issue was not found and exits with code 0.