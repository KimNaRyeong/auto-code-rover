Given the request, below is a simplified standalone Python script, named `reproducer.py`, designed to run in a Django project's root directory. This script follows the issue description regarding the `QuerySet.defer()` method not clearing a deferred field when chained with `only()`. For correctness, ensure your Django environment is properly set up, including a `Company` model with the fields `id`, `name`, `trade_number`, and `country`. This script attempts to reproduce the issue and will raise an `AssertionError` if the unexpected behavior is observed, printing a detailed stack trace per the provided function.

To validate the script's operation, ensure that your Django settings are configured correctly, particularly the `DATABASES` setting, so that the script can interact with your database.

```python
# reproducer.py
import django
from django.conf import settings
from django.db import models
from django.db.models.query import QuerySet

def setup():
    settings.configure(
        DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'mydatabase',
            }
        },
        INSTALLED_APPS=(
            '__main__',
        ),
        TIME_ZONE='UTC',
        USE_TZ=True,
    )
    django.setup()

    class Company(models.Model):
        name = models.CharField(max_length=255)
        trade_number = models.CharField(max_length=255)
        country = models.CharField(max_length=255)

        class Meta:
            app_label = '__main__'

    globals()['Company'] = Company  # Making Company accessible globally

    from django.core.management import call_command
    call_command('migrate', '--noinput')

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

def check_query(expected, queryset):
    sql, params = queryset.query.sql_with_params()
    print(f"Executing SQL: {sql}")
    assert sql == expected, "SQL query does not match the expected output."

def main():
    setup()
    
    try:
        # Assuming Company model and setup was successful
        Company.objects.create(name='Acme Corporation', trade_number='123456789', country='Wonderland')

        # The following lines are the core issue reproduction
        sql_test_1 = str(Company.objects.only("name").defer("name").query)
        sql_test_2 = str(Company.objects.only("name").defer("name").defer("country").query)
        sql_expected = str(Company.objects.only("id").query)  # Only 'id' should be selected

        assert sql_expected in sql_test_1, "defer() following only() did not produce the expected SQL query."
        assert sql_expected in sql_test_2, "Chaining defer() following only() with an extra defer() did not produce the expected SQL query."

    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

    print("The issue was not reproduced. Exiting with code 0.")
    sys.exit(0)

if __name__ == "__main__":
    main()
```

Before running the script:
- Ensure Django is installed in your environment.
- Replace `'mydatabase'` with the path to your actual SQLite database file, or adjust the `DATABASES` setting to match your configuration.
- This script attempts to create a table for the `Company` model and insert a test record. Adjustments might be necessary based on your current database schema.
- The assertion for SQL string comparisons is simplistic and may require more precise handling to accurately assess whether the generated SQL query matches the expected behavior described.

Execute this script in the root directory of your Django project using the command:

```bash
python3 reproducer.py
```

This script is intended to demonstrate the issue as described. For an actual deployment or extended testing, a more sophisticated approach to handling model registration and migrations may be necessary.