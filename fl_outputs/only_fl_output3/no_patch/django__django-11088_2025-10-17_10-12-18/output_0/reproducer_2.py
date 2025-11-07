"""
reproducer.py
-------------
Reproduces the issue where default value modification on a BinaryField from '' to b'' causes migration reverse failure.
"""

import os
import sys
import django
from django.conf import settings
from django.db import models
from django.core.management import call_command

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

# Configure Django settings
settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
        }
    },
    INSTALLED_APPS=('__main__',),
    MIGRATION_MODULES={'__main__': 'migrations'},
    SECRET_KEY='some-secret-key',
)

django.setup()

# Define initial model
class TableOne(models.Model):
    field1 = models.BinaryField(default='')

# Programmatic migration to simulate issue reproduction.
try:
    # Initial migration
    call_command('makemigrations', '__main__', interactive=False, verbosity=3)
    call_command('migrate', '__main__', interactive=False, verbosity=3)

    # Modify model inside the try block to catch exceptions if they occur during the process.
    # This change simulates editing the models.py file between migrations
    TableOne._meta.get_field('field1').default = b''

    # Second migration after modifying the default
    call_command('makemigrations', '__main__', interactive=False, verbosity=3)
    call_command('migrate', '__main__', interactive=False, verbosity=3)

    # Now, attempt to reverse the migration
    call_command('migrate', '__main__', 'zero', interactive=False, verbosity=3)

    print("The issue did not occur. Migration reversal was successful.")

except Exception as e:
    print_stacktrace(e)
    assert False, "The issue occurred. Please check the traceback."

