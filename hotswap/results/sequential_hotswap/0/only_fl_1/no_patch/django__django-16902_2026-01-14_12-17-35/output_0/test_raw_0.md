Below is a Python script named `reproducer.py` designed to replicate the described issue. This script assumes that you have a Django project set up with a database backend where this issue can occur (either Oracle or SQLite as mentioned). Furthermore, it's important to adjust your database settings accordingly in your `settings.py` for this script to connect to the correct database.

For this script to run, ensure you have Django and the necessary database drivers installed in your environment. The script creates a temporary model to avoid dependencies on existing models and migrations.

```python
import os
import django
from django.conf import settings
from django.db import models
from django.db.models.functions import Right, Length

# Setup Django without an actual project
settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',  # Change to 'django.db.backends.oracle' for Oracle
            'NAME': ':memory:',  # Use your database name if using Oracle
        }
    },
    INSTALLED_APPS=('__main__',),
    USE_TZ=True,
)

django.setup()

# Define a temporary model for the repro
class MyModel(models.Model):
    foo = models.CharField(max_length=255)

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

def test_right_function_returns_empty_string():
    # Ensuring the table exists
    MyModel.objects.create(foo='Test')  

    # Attempt to reproduce the issue
    try:
        results = MyModel.objects.annotate(
            suffix=Right("foo", Length("foo") - Length("foo"))
        )
        assert results[0].suffix == "", "RIGHT function did not return an empty string when length is 0."
        print("The issue is fixed.")
    except AssertionError as e:
        print_stacktrace(e)
        raise e

if __name__ == '__main__':
    try:
        test_right_function_returns_empty_string()
    except Exception as e:
        exit(1)
```

This script:
- Configures a minimal Django environment.
- Defines a `MyModel` class with a `CharField`.
- Implements a test function `test_right_function_returns_empty_string` that tries to reproduce the issue described.
- Uses the `Right` and `Length` functions to compute a suffix expecting an empty string when the length is 0.
- Raises an `AssertionError` if the behavior does not match the expected outcome (i.e., it does not return an empty string when length is 0).
- Calls `print_stacktrace` to print the stack trace if the assertion fails.

Remember to adapt the `DATABASES` configuration in the `settings.configure` call to match your database backend and connection details, especially if you're testing against Oracle.

To run this script, save it as `reproducer.py` in the root of your Django project and execute it with `python3 reproducer.py`. Make sure to set up your environment correctly for Django to access your database.