To create a standalone script that accurately reproduces the issue within a Django environment without needing to modify the existing Django project settings or rely on its specific configuration, you can follow the provided structure below. The script dynamically sets up Django models and configurations, which allows for isolating the reproduction of the described issue regarding Django multi-table inheritance behavior with a custom primary key.

This script does not depend on a pre-existing Django project. Instead, it programmatically configures Django to ensure that it can be executed in any environment where Django is installed. Please ensure Django is installed in your environment, or install it via `pip install django`.

```python
"""
reproducer.py
This script reproduces the issue of an unexpected extra UPDATE query when creating a child model instance,
where the parent model uses a custom primary key.
"""

import uuid
import os
import sys

from django.conf import settings
from django.core.management import execute_from_command_line
from django.db import models, connection

# Dynamically configure the Django settings
settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    INSTALLED_APPS=(
        '__main__',  # Makes Django recognize this script as an app
    ),
    USE_TZ=True,
)

# Initialize Django
execute_from_command_line(['manage.py', 'migrate'])

# Define models to reproduce the issue
class Parent(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    title = models.TextField()

    class Meta:
        app_label = '__main__'

class Child(Parent):
    body = models.TextField()

    class Meta:
        app_label = '__main__'


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

def reproduce_issue():
    # Create an instance of the Child model
    Child.objects.create()

    # Capture query log
    query_log = connection.queries

    # Check for unexpected UPDATE queries
    unexpected_updates = [
        query for query in query_log if 'UPDATE' in query['sql'].upper()
    ]

    if unexpected_updates:
        # Issue present: The parent model should not have a separate UPDATE query upon creation
        raise AssertionError("Detected unexpected UPDATE query(-ies) on parent model creation.")

try:
    reproduce_issue()
    print("No unexpected UPDATE query detected. The issue appears to be fixed.")
    sys.exit(0)
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)
```

This script sets up a minimal environment necessary for Django to run, defines the parent and child models inline with the specific conditions that trigger the issue (custom primary key on the parent), and then attempts to reproduce the problem by observing the SQL queries generated during the model creation process.

This standalone approach ensures the script can be executed in any Django-supported environment without additional setup, making it a useful tool for both demonstrating the problem and verifying its resolution.