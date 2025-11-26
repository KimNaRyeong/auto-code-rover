Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import os
from django.db import models
from django.test.utils import setup_test_environment

setup_test_environment()

os.environ['DJANGO_SETTINGS_MODULE'] = 'reproducer.settings'

class Company(models.Model):
    name = models.CharField(max_length=255)
    trade_number = models.IntegerField()
    country = models.CharField(max_length=255)

def test_defer_only_issue():
    qs1 = Company.objects.only("name").defer("name")
    assert set(qs1.query.get_columns()) == {"id"}, f"Expected only 'id' column, got {qs1.query.get_columns()}"

    try:
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

If you run this script with `python3 reproducer.py`, it should raise an `AssertionError` when the issue is present and print a stack trace of the issue. When the issue is fixed, the script should exit with code 0.