import os
import sys
import django
from django.conf import settings
from django.core.management import execute_from_command_line
from django.db import models

# Define a simple setting configuration for Django
settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'test_db.sqlite3',
        }
    },
    INSTALLED_APPS=('__main__',),
    SECRET_KEY='a',
)

django.setup()

# Define initial models
class Bar(models.Model):
    pass

class Foo(models.Model):
    bar = models.ManyToManyField('Bar', blank=True)

# Dynamically create migrations and migrate the database for initial models
execute_from_command_line(['manage.py', 'makemigrations'])
execute_from_command_line(['manage.py', 'migrate'])

# Modify the Foo model to cause the intended issue
Foo.bar.through._meta.managed = False  # Avoid removing the old M2M table
Foo._meta.local_many_to_many = []    # Clear existing M2M fields in Foo's meta
# Redefine Foo to have a M2M field pointing to itself
Foo.add_to_class('bar', models.ManyToManyField('self', blank=True))

# Attempt to generate a second set of migrations to apply the changes
try:
    execute_from_command_line(['manage.py', 'makemigrations'])
    execute_from_command_line(['manage.py', 'migrate'])
    raise RuntimeError("Migration should not succeed.")
except Exception as e:
    # Print the expected stack trace if there's an issue during migration
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

    print_stacktrace(e)
    # An OperationalError or a similar issue should trigger an AssertionError
    assert "no such column: app_foo_bar.from_foo_id" in str(e), "The issue could not be reproduced"

# Clean up by removing the test database file
os.remove('test_db.sqlite3')
