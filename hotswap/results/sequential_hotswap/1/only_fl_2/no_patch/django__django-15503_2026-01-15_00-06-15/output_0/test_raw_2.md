To create a script that accurately attempts to reproduce the reported issue, we'll encapsulate the logic surrounding Django's `JSONField` and its ability to query numeric keys properly. The script below is designed to set up a minimal Django environment, define a model using `JSONField`, populate the database with sample data, and run a test case querying by a numeric key.

Save this script as `reproducer.py` in the root directory of your project and execute it with `python3 reproducer.py`. This setup ensures that we're working within a minimalist Django framework environment capable of reproducing the reported behavior concerning numeric keys in `JSONField`.

```python
import os
import django

from django.conf import settings
from django.db import models


def setup_django_environment():
    settings.configure(
        DEBUG=True,
        INSTALLED_APPS=[
            '__main__',
        ],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'testdb.sqlite3',
            }
        },
        USE_TZ=True,
    )
    django.setup()


# Model definition
class JsonFieldHasKeyTest(models.Model):
    data = models.JSONField()


# Function for detailed test failure reporting
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


# Main run function for the script
def run():
    setup_django_environment()

    # Applying migrations
    from django.core.management import call_command
    call_command('migrate')

    # Create test data
    test_instance = JsonFieldHasKeyTest.objects.create(data={'foo': 'bar', '1111': 'value'})
    test_instance.save()

    from django.db.models import Q
    try:
        # Attempt to query using a numeric key as string
        found_instances_by_string = JsonFieldHasKeyTest.objects.filter(data__has_key='1111').count()
        assert found_instances_by_string == 1, "Should have found 1 entry with string key '1111'"

        # Optionally, uncomment to test numeric key directly if that reflects the original issue more accurately
        # found_instances_by_numeric = JsonFieldHasKeyTest.objects.filter(data__has_key=1111).count()
        # assert found_instances_by_numeric == 1, "Should have found 1 entry with numeric key 1111"

        print("Test passed: Issue not reproduced. Numeric key '1111' was found.")

    except AssertionError as e:
        print_stacktrace(e)
        os._exit(1)  # Use os._exit to ensure the process exits with the correct status in case of failure


if __name__ == '__main__':
    run()
```

This script will create a minimal Django environment needed to test the scenario described in the issue. It will:

1. Define a model `JsonFieldHasKeyTest` with a `JSONField`.
2. Populate the database with an instance that includes a numeric key '1111'.
3. Attempt to query this instance using the key as a string, mirroring the original issue's conditions.

It's important to note that direct numeric querying (i.e., using a number without quotes) is commented out because your initial report specifies querying with a numeric key treated as a string ('1111'). Adjust the script according to your exact needs, especially if testing other database backends or Django configurations is required.