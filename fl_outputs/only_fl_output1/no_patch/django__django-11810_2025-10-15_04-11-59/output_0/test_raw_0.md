Sure, here is a `reproducer.py` script designed to setup a minimal Django environment, define the necessary models, and then reproduce the issue based on the descriptions you've provided. This script checks for the problematic behavior and raises an `AssertionError` when the issue occurs as described, then prints a stack trace of the problem.

```python
import os
import sys
from django.conf import settings
from django.core.management import execute_from_command_line


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


# Dynamically configure the Django settings
settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'mydatabase',
        }
    },
    INSTALLED_APPS=(
        '__main__',  # This script will contain the app and models
    ),
)

# Define the models inline
from django.db import models


class ModelA(models.Model):
    pass


class ModelB(models.Model):
    pass


class ModelC(models.Model):
    model_a = models.ForeignKey('ModelA', on_delete=models.CASCADE)
    model_b = models.ForeignKey('ModelB', on_delete=models.CASCADE)


# Mimic the standard Django startup process
if __name__ == "__main__":
    execute_from_command_line(['manage.py', 'migrate'])

    # Reproduce the issue as described
    try:
        query_1 = ModelC.objects.select_related('model_a')
        print('QUERY 1:', str(query_1.query))
        query_2 = query_1.select_related('model_b')
        print('QUERY 2:', str(query_2.query))
        print('QUERY 1 AGAIN:', str(query_1.query))

        if str(query_1.query) == str(query_2.query):
            raise AssertionError("The original QuerySet was mutated after chaining select_related, which is incorrect.")
        else:
            print("The issue did not occur; the original QuerySet remains unmutated.")

    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with error status when the issue is reproduced

    sys.exit(0)  # Exit successfully if the issue is not present
```

This script includes:
- Dynamically setting up a minimal Django configuration allowing it to run standalone.
- Defining several simple models within the script for demonstration purposes.
- Reproducing the issue specified based on the `select_related` usage and checking whether the problem occurs as described.
- Utilizing the `print_stacktrace` function to print an informative stack trace if an `AssertionError` is raised.
- Exiting with code 0 if the problem is fixed, or raising an exception and printing the stack trace if the issue is present.