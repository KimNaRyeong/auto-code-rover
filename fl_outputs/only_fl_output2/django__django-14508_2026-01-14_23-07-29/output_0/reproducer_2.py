"""
reproducer.py
Standalone script to trigger and demonstrate issue with Django model inheritance.
"""

import os
import sys

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

# Configure Django settings in a minimal setup
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reproducer_settings")

from django.conf import settings
settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    INSTALLED_APPS=('__main__',),
    USE_TZ=True,
)

# Initialize Django
import django
django.setup()

# Define models
from django.db import models

class SomeTestModel(models.Model):
    some_field = models.CharField(max_length=100)

    class Meta:
        abstract = True

    @property
    def other_field(self):
        return "[OTHER] %s" % self.some_field

class OtherModel(SomeTestModel):
    other_field = models.CharField(max_length=100)

class AndMoreOther(SomeTestModel):
    not_important_field = models.CharField(max_length=100)

def test_issue():
    try:
        # Attempt to instantiate the model that raises the AttributeError
        o = OtherModel()
        raise AssertionError("Expected an AttributeError when overwriting a @property with a field, but it did not occur.")
    except AttributeError as e:
        print_stacktrace(e)

if __name__ == "__main__":
    try:
        test_issue()
    except AssertionError as expected_issue:
        print("The test did not reproduce the issue as expected.", file=sys.stderr)
        raise expected_issue
    else:
        print("The AttributeError due to the @property being overwritten by a field was successfully reproduced.")
        sys.exit(0)  # Exit with code 0 to indicate the script executed as expected, reproducing the issue.
