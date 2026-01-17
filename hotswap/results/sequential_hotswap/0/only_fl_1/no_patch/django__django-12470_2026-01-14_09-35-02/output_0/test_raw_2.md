Below is an updated standalone Python script designed to set up a basic Django environment, with models that replicate the described issue. This script uses Django configuration within itself to provide a minimal setup for reproducing the problem related to inheriting models and query ordering.

When executed, the script will attempt to validate if a query on the `Child` model results in the expected ordering as defined in the `Parent` model's `Meta` class. If the script finds that the results do not match the expected ordering, it will raise an `AssertionError` and print a stack trace.

Please ensure Django is installed in your environment before running this script. You can do so by running `pip install Django` in your terminal.

```python
# reproducer.py
import os
import sys
import django
from django.conf import settings
from django.core.management.commands.runserver import Command as runserver
from django.db import models

# Configure Django settings
settings.configure(
    DEBUG=True,
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }
    },
    INSTALLED_APPS=(
        "__main__",  # This script is the 'app'
    ),
    USE_TZ=True,
)

django.setup()

# Models definition
class Parent(models.Model):
    class Meta:
        ordering = ["-pk"]

class Child(Parent):
    pass

# Setup the environment
runserver.validate(models)

# Function to print stack trace
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

### Testing code starts here
try:
    Child.objects.create()  # Ensure at least one object exists
    
    # Inspecting generated SQL query
    query = str(Child.objects.all().query)
    print(f"Query: {query}")

    # Check if order is DESC as expected from Parent.Meta.ordering
    assert "ORDER BY" in query and "-pk" in query, "Child query does not correctly order by '-pk'"

except Exception as e:
    print_stacktrace(e)
    sys.exit(1) # Exit with error

print("Test passed - Child objects query ordering as expected.")
sys.exit(0) # Exit without error
```

This script constructs a minimum viable Django application, including model definitions and a simple test to validate the specific behavior in question. Notice that the script configures a SQLite in-memory database, ensuring no external database setup is required. The inclusion of a custom function to print stack strace helps in detailed error analysis if the documented behaviour does not meet expectations upon script execution.