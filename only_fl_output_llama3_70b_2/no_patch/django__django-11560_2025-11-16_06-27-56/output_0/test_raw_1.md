Here is the revised `reproducer.py` file that reproduces the issue:
```
import os
import sys
from django.conf import settings
from django.apps import apps
from django.db import models
from django.db.models.functions import ExtractYear
from django.core.exceptions import ValidationError

# Configure Django settings
settings.configure(INSTALLED_APPS=['reproducer'], DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}})
apps.set_installed_apps(['reproducer'])

# Create a test model with a DurationField
class MyModel(models.Model):
    duration = models.DurationField()

def main():
    # Try to annotate and filter on ExtractYear of a DurationField
    try:
        MyModel.objects.annotate(year=ExtractYear('duration')).filter(year__gt=1)
        raise AssertionError("Expected ValueError or ValidationError, but no exception was raised")
    except (ValueError, ValidationError) as e:
        print_stacktrace(e)

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

if __name__ == "__main__":
    main()
```
This script configures Django settings, creates a test model with a `DurationField`, and then tries to annotate and filter on the `ExtractYear` of the `DurationField`. If no exception is raised, it raises an `AssertionError`. If a `ValueError` or `ValidationError` is raised, it prints the stack trace using the provided function.