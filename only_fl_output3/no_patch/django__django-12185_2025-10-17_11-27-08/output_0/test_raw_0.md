To create a standalone Python file named `reproducer.py` for reproducing the described issue, follow these instructions. Remember, this script assumes you have Django installed and configured with a database that allows window functions (e.g., PostgreSQL). It simulates the creation of a simple model and database setup to demonstrate the issue with window functions in Django's ORM. Make sure you have Django available in your environment before running this script.

```python
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reproducer_settings")
import django
from django.conf import settings
from django.db import models, NotSupportedError, connection
from django.db.models import F, Window, Lag, Case, When, Value, BooleanField

# Define a minimal setting for Django ORM to work
MINIMAL_SETTINGS = {
    'INSTALLED_APPS': [
        '__main__',  # This module (reproducer.py) will be considered an app by Django
    ],
    'DATABASES': {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    'USE_TZ': True,
}

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def setup():
    settings.configure(**MINIMAL_SETTINGS)
    django.setup()

    # Define a simple Employee model to simulate the issue
    class Employee(models.Model):
        name = models.CharField(max_length=100)
        salary = models.DecimalField(max_digits=10, decimal_places=2)
        department = models.CharField(max_length=100)

        class Meta:
            app_label = '__main__'

    # Create tables
    with connection.schema_editor() as schema_editor:
        schema_editor.create_model(Employee)

    return Employee

def main():
    Employee = setup()

    # Attempt to reproduce the issue
    try:
        Employee.objects.annotate(
            lag=Window(
                expression=Lag(expression='salary', offset=1),
                partition_by=F('department'),
                order_by=[F('salary').asc(), F('name').asc()],
            ),
            is_changed=Case(
                When(salary=F('lag'), then=Value(False)),
                default=Value(True), output_field=BooleanField()
            ),
        )
    except NotSupportedError as e:
        print_stacktrace(e)
        raise AssertionError("Window expressions not allowed in conditional statements in the SELECT clause.") from e

    print("Success: The issue is not present.")

if __name__ == "__main__":
    main()
```

This script sets up an in-memory SQLite database for simplicity; you need to adjust the `DATABASES` configuration in `MINIMAL_SETTINGS` if your use case involves another database that supports window functions, such as PostgreSQL. The script defines a minimal Django setting environment, creates a basic `Employee` model with necessary fields, and executes an annotation query with a window function in a `Case` statement, intended to reproduce the described issue. Lastly, it attempts to catch and print the stack trace of the `NotSupportedError` exception, which is raised when Django does not allow window expressions in conditional statements in the `SELECT` clause, as reported.