```python
# reproducer.py
import os
import django
from django.conf import settings
from django.db import models

def configure_django():
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'db.sqlite3',
            }
        },
        INSTALLED_APPS=('__main__',), # Trick Django to include this script as an app for our model
    )
    django.setup()

# Define a minimal Django model
class Company(models.Model):
    name = models.CharField(max_length=255)
    trade_number = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

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

def main():
    configure_django()
    models.Model.check(django.db.connection)  # Initial model check and creation if necessary

    # Checking the unwanted behavior
    only_defer_sql = str(Company.objects.only("name").defer("name").query)

    try:
        assert "SELECT" in only_defer_sql, "Generated SQL does not start with SELECT."
        assert "FROM" in only_defer_sql, "Generated SQL does not contain FROM clause."
        assert '"company"."trade_number"' not in only_defer_sql, "Field 'trade_number' is unexpectedly selected."
        assert '"company"."country"' not in only_defer_sql, "Field 'country' is unexpectedly selected."
        print("Issue not present.")
    except AssertionError as e:
        print_stacktrace(e)

if __name__ == "__main__":
    main()
```

This script initializes a minimal Django environment, defines a simple `Company` model, and checks if the described issue with `QuerySet.defer()` and `only()` methods occurs. In case the issue persists, it runs a check on the generation of the SQL query to ensure fields are being deferred as expected. If the assertion fails (implying the issue is present), it catches the `AssertionError` and prints a detailed stack trace using the provided `print_stacktrace` function.