Given the complexities previously encountered, here's a refined approach to creating a standalone Python file named `reproducer.py` to reproduce the issue mentioned. This version addresses setting up Django configurations, model migrations, and executing the tests as intended, while providing clear and concise output on success or failure.

```python
"""
reproducer.py
"""

import os
import sys
from django.conf import settings
from django.db import models
from django.core.management import execute_from_command_line


def prepare_environment():
    settings.configure(
        DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'testdb.sqlite3',
            }
        },
        INSTALLED_APPS=('__main__',),
        USE_TZ=True,
    )
    execute_from_command_line(['manage.py', 'migrate'])


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


# Define the model
class JsonFieldHasKeyTest(models.Model):
    data = models.JSONField()


def run_tests():
    # Clean the database for a fresh start
    JsonFieldHasKeyTest.objects.all().delete()

    # Creating test data
    try:
        JsonFieldHasKeyTest.objects.create(data={'foo': 'bar'})
        JsonFieldHasKeyTest.objects.create(data={'1111': 'bar'})
    except Exception as e:
        print_stacktrace(e)
        return

    # Running the test cases
    try:
        assert JsonFieldHasKeyTest.objects.filter(data__has_key='foo').count() == 1, \
            "Should have found 1 entry with key 'foo'"
        assert JsonFieldHasKeyTest.objects.filter(data__has_key='1111').count() == 1, \
            "Should have found 1 entry with key '1111'"
        print("Test passed. No issues detected.")
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)


if __name__ == "__main__":
    prepare_environment()
    try:
        from django.apps import apps
        apps.populate(settings.INSTALLED_APPS)
        from django.db import connections
        from django.db.utils import OperationalError
        try:
            conn = connections['default']
            conn.prepare_database()
        except OperationalError as e:
            print("Could not connect to the database. Make sure it is configured correctly.")
            sys.exit(1)
    except ImportError as e:
        print_stacktrace(e)
        sys.exit(1)

    run_tests()
```

This script starts by setting up a minimal Django environment tailored for this specific test scenario. It configures Django to use an SQLite database to replicate the issue. The `prepare_environment` function takes care of necessary steps such as configuring Django settings and applying migrations.

The script defines a `JsonFieldHasKeyTest` model with a single `JSONField`, then proceeds to populate the database with example data. It then runs assertions to check whether the `has_key` lookup works correctly for both string and numeric keys within the `JSONField`. An `AssertionError` is raised if the lookup fails, specifically when it does not find an entry with a numeric key, alongside printing a stack trace for clarity.

Remember, before you run this script, make sure Django is installed in your environment. You can do so by running `pip install django` in your virtual environment. After setting up, execute this script using Python 3 with the command `python3 reproducerer.py` from the terminal. The script will exit with code 0 if the test passes (indicating a possible fix for the issue) or provide a detailed stack trace on failure, highlighting the problem remains.