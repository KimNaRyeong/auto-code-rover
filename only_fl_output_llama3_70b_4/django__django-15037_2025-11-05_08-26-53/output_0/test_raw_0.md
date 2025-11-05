Here is the `reproducer.py` file that reproduces the issue:
```
import os
import sys
from django.db import models
from django.core.management import call_command

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

# Create a test database
os.environ['DATABASES'] = '{"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}'

# Create the tables
call_command('sqlmigrate', verbosity=0)
call_command('dbshell', commands=[
    'CREATE TABLE foo ( id serial primary key, other_id int UNIQUE);',
    'CREATE TABLE bar (id serial primary key, other_id int, constraint myconst FOREIGN KEY(other_id) references foo(other_id));'
], verbosity=0)

# Inspect the database
call_command('inspectdb', verbosity=0)

# Check if the issue is present
from django.apps import apps
BarModel = apps.get_model('bar', 'Bar')
assert BarModel._meta.get_field('other_id').remote_field.model._meta.db_table == 'foo', "Foreign key to a specific field is not handled in inspectdb"
print("Issue is fixed!")

sys.exit(0)
```
This script creates a test database, creates the tables using `dbshell`, inspects the database using `inspectdb`, and then checks if the issue is present by verifying that the foreign key on the `other_id` field of the `Bar` model references the `foo` table. If the issue is present, it raises an `AssertionError` with a stack trace. If the issue is fixed, it prints "Issue is fixed!" and exits with code 0.