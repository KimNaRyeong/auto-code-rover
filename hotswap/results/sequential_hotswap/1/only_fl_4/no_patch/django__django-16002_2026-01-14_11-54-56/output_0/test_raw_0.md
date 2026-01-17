```python
import os
import django
from django.conf import settings
from django.db import models

def setup_django_environment():
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(os.getcwd(), 'db.sqlite3'),
            }
        },
        INSTALLED_APPS=(
            '__main__',  # Register this module as an app for our model
        ),
        USE_TZ=True,
    )
    django.setup()

class MyModel(models.Model):
    value = models.DecimalField(max_digits=10, decimal_places=5)

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
    setup_django_environment()

    # Ensuring models are ready
    django.core.management.call_command('migrate', verbosity=0)

    # Creating a model instance with value='nan'
    obj = MyModel.objects.create(value="nan")
    obj.save()

    # Trying to retrieve the object
    try:
        obj = MyModel.objects.get(pk=1)
    except Exception as e:
        print_stacktrace(e)
        assert isinstance(e, TypeError), "The issue is expected to be a TypeError"
        return

    # If no exception was raised, then the issue is fixed
    print("No issue detected, the problem seems to be fixed.")
    exit(0)

if __name__ == '__main__':
    main()
```

This script sets up a minimal Django environment programmatically, creates a model `MyModel` with a `DecimalField` attribute, and runs through the process of storing and retrieving a value that reproduces the described issue. The `print_stacktrace` function is used to clearly output the error details, allowing for precise debugging. The script exits with code 0 if the exception (indicating the presence of the issue) is caught, and asserts a `TypeError` to ensure the right type of issue is identified, thus providing a clear mechanism for reproducing and identifying the resolution of the outlined problem.