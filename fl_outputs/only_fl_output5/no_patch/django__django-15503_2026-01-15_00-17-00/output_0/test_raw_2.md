Certainly, here's an approach to writing a standalone `reproducer.py` script to replicate the specific issue within a Django application. The emphasis will be on initializing a minimal Django setup within the script, demonstrating the problem with `has_key` and numeric keys, and appropriately handling any exceptions to provide a clear output and correct exit code based on the presence of the issue.

```python
"""
reproducer.py
Reproduces the issue with has_key, has_keys, and has_any_keys JSONField() lookups not handling numeric keys on SQLite, MySQL, and Oracle.
"""

import os
import django
from django.conf import settings
from django.db import models
from django.core.management import call_command

# Define minimal Django configuration
settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    INSTALLED_APPS=('__main__',),
    USE_TZ=True,
)

django.setup()

# Define the model
class JsonFieldHasKeyTest(models.Model):
    data = models.JSONField()

    class Meta:
        app_label = '__main__'

# Perform Django setup tasks
call_command('migrate')

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

def test_json_field_has_key():
    JsonFieldHasKeyTest.objects.create(data={'foo': 'bar', '1': 'baz'})
    
    try:
        assert JsonFieldHasKeyTest.objects.filter(data__has_key='foo').exists(), "Should find 'foo' key"
        assert JsonFieldHasKeyTest.objects.filter(data__has_key='1').exists(), "Should find '1' key"
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)

    print("Test passed, numeric keys are properly handled.")
    sys.exit(0)

if __name__ == '__main__':
    test_json_field_has_key()
```

This script:
- Sets up a minimal Django configuration tailored for the script's purposes.
- Defines a single `JsonFieldHasKeyTest` model with a `JSONField`.
- Applies migrations to the in-memory SQLite database to avoid filesystem dependencies.
- Inserts a test record into the database.
- Runs assertions to confirm whether the `has_key` lookup properly handles numeric keys.
- Uses the provided `print_stacktrace` function to format any `AssertionError` raised if the lookups don't behave as expected.

This script should be saved in the root directory of your Django project and run using the command `python3 reproducer.py`. Depending on the outcome of the test (whether the issue is reproduced or not), it will either print the stack trace and exit with code 1 or confirm successful handling of numeric keys and exit with code 0.