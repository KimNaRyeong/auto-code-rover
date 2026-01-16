```python
import os
import django
from django.conf import settings
from django.core.management import execute_from_command_line

# Minimal Django configuration for the script to run
settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
        }
    },
    INSTALLED_APPS=(
        '__main__',  # This script is the app
    ),
    USE_TZ=True,
)

# Define the model inside the script
from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=100)
    trade_number = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

# Function to print stack trace
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

# The main script execution
if __name__ == '__main__':
    # Initialize Django to avoid "AppRegistryNotReady" exception
    django.setup()

    # Create the database and table
    execute_from_command_line(['manage.py', 'migrate'])

    # Reproducing the issue
    try:
        # Insert a dummy company to make sure SQL runs without optimizing out the query
        Company.objects.create(name="Test Company", trade_number="123456", country="Testland")

        # The query that should not behave as expected
        problematic_query = Company.objects.only("name").defer("name")
        # Generate the SQL query without executing it
        sql_str = str(problematic_query.query)
        if "trade_number" in sql_str or "country" in sql_str:
            raise AssertionError("Deferred field was not cleared when chaining with only(), unexpected fields in SQL query.")

        problematic_query_2 = Company.objects.only("name").defer("name").defer("country")
        sql_str_2 = str(problematic_query_2.query)
        if "trade_number" in sql_str_2:
            raise AssertionError("Deferred fields were not cleared when chaining with only(), unexpected fields in SQL query.")

    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    except Exception as e:
        print_stacktrace(e)
        exit(1)
    else:
        print("No issue detected.")
        exit(0)
```

Note: Before running this script, ensure you have Django installed in your environment or activated virtual environment. You can install Django using pip:

```
pip install Django
```

This script uses a minimal Django configuration within the script itself and creates an in-memory SQLite database to avoid any external dependencies. It tries to reproduce the issue as described, by checking if the generated SQL query contains fields that were intended to be deferred. If the issue is present, it raises an `AssertionError` and prints a detailed stack trace. If the issue is not present, it concludes with "No issue detected." and exits with code 0.