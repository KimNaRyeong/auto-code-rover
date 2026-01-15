```python
# reproducer.py

import os
import sys
from django.conf import settings
from django.core.management import execute_from_command_line
from django.db import models

# Set up a minimal Django project
settings.configure(
    INSTALLED_APPS=["__main__"],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
)

# Define models according to the issue
class Parent(models.Model):
    class Meta:
        ordering = ["-pk"]

class Child(Parent):
    pass

# Function to print stack trace as specified
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

# Main function to execute the script and assert the issue
def main():
    # Mimic the `manage.py` environment
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "__main__")
    execute_from_command_line(['manage.py', 'migrate'])

    # Test the issue
    try:
        query = str(Child.objects.all().query)
        expected_ordering = 'ORDER BY "myapp_parent"."id" DESC'
        assert expected_ordering in query, "Child query doesn't respect parent Meta ordering"
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    else:
        print("Issue fixed or not present.")
        sys.exit(0)

if __name__ == "__main__":
    main()
```

This script initializes a minimal Django application within a single file. It defines two models as per the given issue description, with `Child` inheriting from `Parent` and the parent model having a Meta class with the ordering attribute set to `["-pk"]`. The script then migrates the model schema to an in-memory SQLite database and queries the `Child` model, expecting the results to be ordered by the `id` field in descending order. If the generated SQL query does not match this expectation, it will raise an `AssertionError` indicating that the issue is present, and print a detailed stack trace using the provided `print_stacktrace` function. If the issue is not present, the script exits with code 0, indicating that the issue is fixed or not reproducible.