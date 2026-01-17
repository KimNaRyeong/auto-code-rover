```python
# reproducer.py

import decimal
import os
import sys
import django
from django.conf import settings
from django.db import models

def setup_django_environment():
    settings.configure(
        DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}},
        INSTALLED_APPS=["__main__"],
    )
    django.setup()

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class DecimalModel(models.Model):
    dec_field = models.DecimalField(decimal_places=0, max_digits=4)

    class Meta:
        app_label = '__main__'

def create_tables():
    from django.core.management import call_command
    call_command("migrate", verbosity=0)

def test_invalid_decimal_query():
    try:
        DecimalModel.objects.get(dec_field='12345')
        raise AssertionError("Query should raise decimal.InvalidOperation or DecimalModel.DoesNotExist")
    except decimal.InvalidOperation as e:
        print_stacktrace(e)
        raise AssertionError("Too large decimal query caused decimal.InvalidOperation exception.")
    except DecimalModel.DoesNotExist:
        # If the issue is fixed and this exception is raised, exit with code 0
        print("No issue, exited with code 0.")
        sys.exit(0)

if __name__ == "__main__":
    import traceback
    setup_django_environment()
    create_tables()

    try:
        test_invalid_decimal_query()
    except AssertionError as e:
        print(e)
        sys.exit(1)  # Ensure the script exits with code 1 in case of an assert failure
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
```

This script is designed to reproduce the described issue in a standalone Django environment. When the issue is present, it will raise an `AssertionError` indicating the problem and exit with code 1. If the issue is fixed (and thus no `decimal.InvalidOperation` is raised), it will print a confirmatory message and exit with code 0. This makes it clear whether the script has identified the issue or verified its resolution.

Please ensure Django is installed in your environment (`pip install django`) and execute this script in the root directory of your Django project using `python3 reproducer.py`.