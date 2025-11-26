Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import os
import sys
from django.db import models
from django.test.utils import setup_test_environment, teardown_test_environment

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

os.environ['DJANGO_SETTINGS_MODULE'] = 'reproducer.settings'

setup_test_environment()

# Create a test Django project
from django.conf import settings

settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:'
        }
    },
    INSTALLED_APPS=[
        'myapp'
    ]
)

from django.apps.registry import Apps
from django.app import AppConfig

class MyAppConfig(AppConfig):
    name = 'myapp'

Apps(app_configs=[MyAppConfig])

# Define the models
from myapp.models import *

class Parent(models.Model):
    class Meta:
        ordering = ["-pk"]

class Child(Parent):
    pass

try:
    # Create the database tables
    from django.core.management import call_command
    call_command('migrate', verbosity=0)

    # Insert some data
    for i in range(10):
        Parent.objects.create()

    # Query the Child model and check the ordering
    query = str(Child.objects.all().query)
    assert "DESC" in query, f"Expected DESC ordering, but got {query}"
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)

teardown_test_environment()
sys.exit(0)
```
This script sets up a test Django project, defines the `Parent` and `Child` models, creates some data, and then queries the `Child` model to check if the ordering is correct. If the ordering is not DESC, it raises an `AssertionError` with a stack trace.