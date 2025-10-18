If you are looking to create a standalone Python script (`reproducer.py`) that reproduces a specific issue concerning the `Chr` function in Django, which is supposed to raise a `ValueError` due to an incorrect handling of its argument, the script would look something like this. This script integrates the function to print stack traces as you requested, and is designed to demonstrate whether the issue is present. Assuming you have a Django project set up and this script is run at the root where `manage.py` is located, here's how you could structure it:

```python
import os
import sys
import django
from django.conf import settings
from django.core.management import execute_from_command_line
from django.db import models
from django.db.models.functions import Chr
from django.db.models import Value

# Define a function to print stack traces
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

# Ensure Django is set up with minimal necessary settings
def setup_django_environment():
    settings.configure(
        DEBUG=True,
        SECRET_KEY='a-very-secret-key',
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'db.sqlite3',
            }
        },
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            '__main__',  # Allows the Author model to be recognized
        ]
    )
    django.setup()

# Define the Author model used in query
class Author(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        app_label = '__main__'

def reproduce_issue():
    setup_django_environment()
    
    # Simulate running migrations to create the Author model table
    # Warning: This will generate files and a db.sqlite3 in your project root
    execute_from_command_line(['manage.py', 'makemigrations'])
    execute_from_command_line(['manage.py', 'migrate'])
    
    try:
        # Attempt to reproduce the issue as described
        Author.objects.annotate(first_letter=Chr(Value(77)))
        # If no error is raised, we assume the issue is resolved
        print("Issue seems to be resolved.")
        sys.exit(0)
    except ValueError as e:
        if 'invalid literal for int() with base 10' in str(e):
            print_stacktrace(e)
            raise AssertionError("The issue is present.") from e
        else:
            # Handle unexpected ValueError differently
            print_stacktrace(e)
            sys.exit(1)
    except Exception as e:
        # Catch-all for any other unexpected exceptions
        print_stacktrace(e)
        sys.exit(1)

if __name__ == '__main__':
    reproduce_issue()
```

This script sets up a minimal Django environment, defines an `Author` model, and attempts to execute a query that should trigger the reported `ValueError`. It will print a detailed stack trace if the error occurs as described or exit normally indicating the issue might be resolved.

**Important:** This script executes Django management commands (`makemigrations` and `migrate`) which will alter your project's state by creating migration files and a database. Use this script with caution, ideally in a test environment or where these changes are acceptable.