import os
import django
from django.conf import settings
from django.db import models
from django.core.management import call_command
from django.db.utils import OperationalError

# Configure Django for a standalone script
def setup_django():
    settings.configure(
        INSTALLED_APPS=['__main__'],  # Use this script as an app
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'db.sqlite3',
            }
        },
        USE_TZ=True,
    )
    django.setup()

# Prints stack trace for exceptions
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

setup_django()

# Define model before change
class Bar(models.Model):
    pass

class FooBefore(models.Model):
    bar = models.ManyToManyField(Bar, blank=True)

# Run initial migrations
call_command('makemigrations', interactive=False, verbosity=0)
call_command('migrate', interactive=False, verbosity=0)

# Change the model to simulate the after change
class FooAfter(models.Model):
    bar = models.ManyToManyField('self', blank=True)

# Attempt to add a Foo instance to itself, simulating access after the migration
try:
    foo_instance = FooAfter.objects.create()
    foo_instance.bar.add(foo_instance)
    foo_instance.save()
    print("The issue did not manifest. Exiting with code 0.")
    os._exit(0)  # Success path
except OperationalError as e:
    print_stacktrace(e)
    raise AssertionError("OperationalError encountered as expected due to the migration issue.")

