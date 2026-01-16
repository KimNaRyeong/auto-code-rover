```python
# reproducer.py
import os
import django
from django.conf import settings
from django.db import models

def setup_django():
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=(
            '__main__',
        ),
        USE_TZ=True,
    )
    django.setup()

# Define your Company model here
class Company(models.Model):
    name = models.CharField(max_length=100)
    trade_number = models.CharField(max_length=100)
    country = models.CharField(max_length=50)

    class Meta:
        app_label = '__main__'

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
    setup_django()
    from django.db import connection

    # Applying migrations
    from django.core.management import call_command
    call_command('migrate')

    # Creating a Company instance for the test
    Company.objects.create(name="Django Software Foundation", trade_number="123456", country="USA")

    # Testing the behaviour

    # Case 1
    queryset = Company.objects.only("name").defer("name")
    with connection.cursor() as cursor:
        queryset._fetch_all()
        query = str(queryset.query)
        if "trade_number" in query or "country" in query:
            raise AssertionError("Case 1: SQL query incorrectly includes trade_number or country")

    # Case 2
    queryset = Company.objects.only("name").defer("name").defer("country")
    with connection.cursor() as cursor:
        queryset._fetch_all()
        query = str(queryset.query)
        if "trade_number" in query:
            raise AssertionError("Case 2: SQL query incorrectly includes trade_number")

    # Expected behavior case
    try:
        queryset = Company.objects.only("name", "country").defer("name")
        with connection.cursor() as cursor:
            queryset._fetch_all()
            query = str(queryset.query)
            if "id" not in query or "country" not in query:
                raise AssertionError("Expected behavior case: SQL query should include only id and country")
    except AssertionError as e:
        print_stacktrace(e)

if __name__ == '__main__':
    try:
        reproduce_issue()
        print("No issues detected. The script exited without raising an AssertionError.")
    except AssertionError as e:
        print_stacktrace(e)
        raise e
```

This script sets up a minimal Django environment with an in-memory SQLite database. We define a `Company` model directly in the script to keep everything self-contained. The script then attempts to reproduce the issue described by executing queries with various combinations of `.only()` and `.defer()`.

When executed, this script should raise an `AssertionError` if it detects the mentioned issue with the `.defer()` not clearing fields when chained with `.only()`. If the Django behavior is correct (matches expected), it prints a message indicating no issues were detected. 

Remember to have Django installed in your Python environment to run this script. You can install Django using `pip`:

```
pip install django
```