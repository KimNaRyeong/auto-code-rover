Below is the `reproducer.py` standalone Python script intended to reproduce the described issue and follow your instructions for error handling and reporting. Please note that this script requires a Django project setup with an application named `app` (you may need to adjust the import paths based on your project structure and application name). Also, ensure your database settings are correctly configured to use PostgreSQL, as the issue involves database interactions specific to PostgreSQL.

```python
import os
import django
import uuid
from django.db import models
from django.conf import settings

# Set up Django project environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
django.setup()

class CustomAssertionError(Exception):
    pass

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

# Define models according to the issue
class Parent(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    title = models.TextField()

    class Meta:
        app_label = 'app'

class Child(Parent):
    body = models.TextField()

    class Meta:
        app_label = 'app'

def check_for_extra_update_query():
    from django.db import connection

    # Clear previously created objects and reset auto-increment values for consistency
    Parent.objects.all().delete()

    # Enable query logging
    connection.queries_log.clear()

    # Trigger the object creation as described
    Child.objects.create()

    # Look for the problematic "UPDATE" query
    update_queries = [q for q in connection.queries if q['sql'].startswith('UPDATE')]
    if update_queries:
        # If such query exists, the issue is reproduced
        raise CustomAssertionError("Detected unexpected UPDATE query on parent model creation.")

try:
    check_for_extra_update_query()
except CustomAssertionError as e:
    print_stacktrace(e)
    os._exit(1)  # Ensure the script exits with error status
else:
    print("The issue has been fixed.")
    os._exit(0)  # Exit with success status when the issue is absent
```

Make sure to replace `'your_project.settings'` with the actual path to your Django project's settings module. This script tries to create a child model instance and checks if an unexpected UPDATE query is performed on the parent model. If such a query is detected, it raises a custom error and prints a detailed stack trace. If the issue is fixed, it will exit gracefully announcing the fix.