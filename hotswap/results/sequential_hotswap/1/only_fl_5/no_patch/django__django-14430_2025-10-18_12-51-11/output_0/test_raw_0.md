```python
# reproducer.py

import os
import django
from django.conf import settings
from django.db import models
from django.db.models import Sum, Value
from django.db.models.functions import Coalesce
from django.core.exceptions import EmptyResultSet

# Minimal Django settings.
settings.configure(
    DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": "db.sqlite3"}},
    INSTALLED_APPS=["__main__"],
    USE_TZ=True,
)

django.setup()


class OrderItem(models.Model):
    quantity = models.IntegerField()

    class Meta:
        app_label = "__main__"


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


def main():
    # Ensuring the table is created.
    with django.db.connection.schema_editor() as schema_editor:
        schema_editor.create_model(OrderItem)
    
    # Test with matched Queryset. Sum will return 50.
    matched_sum_result = OrderItem.objects.filter(pk__in=[1]).aggregate(test=Coalesce(Sum('quantity'), Value(0)))
    assert matched_sum_result['test'] == 50, "Failed: Expected sum to be 50 on matched queryset"

    # Test with unmatched Queryset. Sum will return 0.
    unmatched_sum_result = OrderItem.objects.filter(pk__in=[-1]).aggregate(test=Coalesce(Sum('quantity'), Value(0)))
    assert unmatched_sum_result['test'] == 0, "Failed: Expected sum to be 0 on unmatched queryset"
  
    try:
        # Test with unmatched Queryset (using empty list).
        # Expect Coalesce to return 0, but gets None due to EmptyResultSet behavior.
        empty_list_result = OrderItem.objects.filter(pk__in=[]).aggregate(test=Coalesce(Sum('quantity'), Value(0)))
        assert empty_list_result['test'] == 0, "Failed: Expected sum to be 0 on unmatched queryset with empty list"
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
    print("Issue fixed; exiting with code 0")
    sys.exit(0)
```

This Python script sets up a minimal Django environment to reproduce the issue described. Here's a breakdown of its functionality:

- It first configures a minimal set of Django settings necessary to run, indicating that it should use an SQLite database for simplicity.
- It defines a single Django model, `OrderItem`, in the global namespace because the script isn’t part of an actual Django project/app with a dedicated models module.
- The script contains a function to print an exception's stack trace for debugging purposes.
- The core of the script (`main` function) demonstrates the issue by attempting to aggregate over an empty and non-empty set of model instances using the `Coalesce` function to provide a default value when no rows are matched. It specifically looks for the behaviour difference when filtering with an empty list, which is expected to produce an aggregative zero result (`Coalesce(Sum('quantity'), Value(0))`) but instead results in `None` due to the `EmptyResultSet` issue.
- Assertions are used to enforce the expected behavior, and the script exits with a status code based on the outcome of these assertions.

To run this script, make sure Django is installed in your environment (`pip install django`), and then execute it with Python 3. If the issue is present, the script will exit with code 1 and will print the stack trace of the assertion error. Once the issue is fixed in Django, this script should exit with code 0, indicating everything is working as expected.