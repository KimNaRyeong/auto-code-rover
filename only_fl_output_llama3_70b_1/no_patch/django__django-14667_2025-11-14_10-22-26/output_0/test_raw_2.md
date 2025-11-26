Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import os
import sys
from django.conf import settings
from django.db import models
from django.test.utils import setup_test_environment

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

settings.configure(DEBUG=True, DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3'}})

setup_test_environment()

class Company(models.Model):
    name = models.CharField(max_length=255)
    trade_number = models.IntegerField()
    country = models.CharField(max_length=255)

def test_defer_only_issue():
    try:
        qs1 = Company.objects.only("name").defer("name")
        assert set(qs1.query.get_columns()) == {"id"}, f"Expected only 'id' column, got {qs1.query.get_columns()}"

        qs2 = Company.objects.only("name").defer("name").defer("country")
        assert set(qs2.query.get_columns()) == {"id"}, f"Expected only 'id' column, got {qs2.query.get_columns()}"
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)

if __name__ == "__main__":
    test_defer_only_issue()
```
This script defines a `Company` model with four fields: `id`, `name`, `trade_number`, and `country`. It then tests two querysets:

1. `Company.objects.only("name").defer("name")`
2. `Company.objects.only("name").defer("name").defer("country")`

For each queryset, it checks if the generated SQL query selects only the `id` column using the `get_columns()` method of the queryset's `query` object. If the assertion fails, it prints a stack trace of the issue using the provided `print_stacktrace()` function and exits with code 1.

Note that I added the `setup_test_environment()` call to ensure that Django's test environment is set up correctly. This should fix the `AppRegistryNotReady` error you were seeing.