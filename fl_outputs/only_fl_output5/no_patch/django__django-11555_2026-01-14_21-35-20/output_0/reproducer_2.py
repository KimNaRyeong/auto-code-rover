import os
import django
from django.db import models
from django.db.models.functions import Lower
from django.conf import settings

def initialize_django():
    settings.configure(
        DEBUG=True,
        INSTALLED_APPS=['__main__'],  # Consider current script as an app for Django
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
    )
    django.setup()

# Initialize Django within this script
initialize_django()

# Define models according to the issue's description

class Parent(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = [Lower('name')]  # Using expressions within Meta.ordering

class Child(Parent):
    extra_field = models.CharField(max_length=255)

# Function to print stack trace clearly
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

# Try to reproduce the issue
try:
    # Mocking operations that could reveal the issue
    parent = Parent(name="Test")
    parent.save()
    child = Child(name="Test Child", extra_field="Extra")
    child.save()
    assert Child.objects.first().name == "Test Child", "Child object was not retrieved correctly"
    print("Success: The issue did not occur, or it has been fixed.")
except AssertionError as e:
    print_stacktrace(e)
    raise e
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("An unexpected error occurred, likely related to the issue described.")

