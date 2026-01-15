Here's a stand-alone Python script named `reproducer.py` designed to reproduce the described issue. It includes creating a simple Django project environment to test the `Company` model's behavior with the `defer()` and `only()` queryset methods. This script will raise an `AssertionError` if the generated SQL query does not match the expected result, indicating the issue is present. When the issue is fixed, it should exit with code 0 without any exception.

```python
import os
import sys
import django
from django.conf import settings
from django.db import models
from django.db.models.query import QuerySet


def setup_django_environment():
    settings.configure(
        DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}},
        INSTALLED_APPS=("__main__",),
        USE_I18N=False,
        USE_TZ=False,
    )
    django.setup()


def create_models():
    class Company(models.Model):
        name = models.CharField(max_length=255)
        trade_number = models.CharField(max_length=255)
        country = models.CharField(max_length=255)

    return Company


def check_generated_sql():
    Company = create_models()

    queryset1 = Company.objects.only("name").defer("name")
    sql1 = str(queryset1.query)

    queryset2 = Company.objects.only("name").defer("name").defer("country")
    sql2 = str(queryset2.query)

    expected_sql = "SELECT \"company\".\"id\" FROM \"company\""

    return sql1 == expected_sql and sql2 == expected_sql


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


def main():
    setup_django_environment()

    try:
        correct_sql_generated = check_generated_sql()
        assert correct_sql_generated, "Generated SQL does not match expectations."
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
    else:
        print("Issue is fixed, no AssertionError raised.")
        sys.exit(0)


if __name__ == "__main__":
    main()
```

This script dynamically configures a Django environment to use an SQLite in-memory database, declares a `Company` model with the specified fields, and then checks the generated SQL for the stated issue. The `main()` function orchestrates the setup, test execution, and validation phases, while the `print_stacktrace` function provides detailed error output when an assertion fails due to a mismatch between the generated and expected SQL. This script assumes the environment is suitable for running Django code snippets and that Django is installed.