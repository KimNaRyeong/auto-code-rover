Creating a standalone `reproducer.py` script that creates a minimal Django environment within the same file simplifies the execution and avoids the external dependency on a settings file like `reproducer_settings.py`. This approach integrates all necessary components into a single file for ease of execution and reproduction of the issue.

```python
import os
import sys
from django.conf import settings


# Configure Django settings directly within the script
def setup_django_env():
    settings.configure(
        SECRET_KEY='a-very-secret-key',
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'django.contrib.auth',
            '__main__',
        ],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        USE_I18N=True,
        USE_L10N=True,
        USE_TZ=True,
    )
    import django
    django.setup()


# Define the model and the operation causing the issue
def define_models_and_test():
    from django.db import models
    from django.db.models.functions import ExtractYear

    class MyModel(models.Model):
        duration = models.DurationField()

    try:
        # Reproducing the issue
        MyModel.objects.annotate(year=ExtractYear('duration')).filter(year__gt=1)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced") from e


# Function to print the stack trace
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


# Main function that sets up the environment, configures Django, and tests the issue
def main():
    setup_django_env()
    from django.core.management import call_command
    # Migrate database and prepare environment
    call_command('migrate', '--no-input')

    # Define models and test the issue
    define_models_and_test()

    print("No issue found. Exiting without error.")
    sys.exit(0)  # A successful exit


if __name__ == "__main__":
    try:
        main()
    except AssertionError as error:
        sys.exit(0)  # Exit with 0 to indicate the issue was successfully reproduced
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        sys.exit(1)
```

This script sets up a Django environment, defines a model with a `DurationField`, and attempts to trigger the described issue with `ExtractYear` in a way that should raise an `AssertionError` when the issue is present. The script exits with code 0 when the issue is successfully reproduced, indicating that the described problem still exists within the Django ORM handling of `DurationField` with `ExtractYear`.