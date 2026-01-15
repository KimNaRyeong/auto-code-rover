```python
# reproducer.py
import os
import sys
import django
from django.conf import settings
from django.db import models

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def setup_django_environment():
    settings.configure(
        DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
            }
        },
        INSTALLED_APPS=(
            '__main__',  # This script is the main application
        ),
    )
    django.setup()

# Define Models
class Parent(models.Model):
    class Meta:
        ordering = ["-pk"]

class Child(Parent):
    pass

# Initialize Django
setup_django_environment()

# Perform migration (no need to create a physical one for the repro)
models.Model.check = lambda self: None
from django.core.management import call_command
call_command('migrate', interactive=False)

# Reproduce the issue
def test_ordering_of_inherited_model():
    # Create some instances just in case the query relies on existing records
    for _ in range(3):
        Child.objects.create()
    
    # Check the query
    query_str = str(Child.objects.all().query)
    expected_order_by = 'ORDER BY "myapp_parent"."id" DESC'
    if expected_order_by not in query_str:
        raise AssertionError(f"Query does not have the expected ORDER BY clause. Found: {query_str}")

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

if __name__ == '__main__':
    try:
        test_ordering_of_inherited_model()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    print("No issue detected.")
    sys.exit(0)
```

This script sets up a minimal Django environment, defining `Parent` and `Child` models wherein `Child` inherits from `Parent`. It then creates some instances of `Child`, generates a query, and checks if the ordering specified in the parent model's Meta class is correctly applied to the query for the child model. If the issue is detected (i.e., the ordering is not as expected), it will raise an `AssertionError` and print a detailed stack trace. If the issue has been resolved, it will exit with code 0, indicating success.