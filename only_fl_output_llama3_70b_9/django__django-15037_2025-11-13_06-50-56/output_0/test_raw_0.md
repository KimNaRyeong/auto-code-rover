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

# Create the tables in the database
call_command('migrate', verbosity=0, interactive=False)

# Create the tables manually
from django.db import connection
cursor = connection.cursor()
cursor.execute("CREATE TABLE foo (id serial primary key, other_id int UNIQUE)")
cursor.execute("CREATE TABLE bar (id serial primary key, other_id int, constraint myconst FOREIGN KEY(other_id) references foo(other_id))")

# Run inspectdb to generate the models
call_command('inspectdb', verbosity=0)

# Check if the generated model for bar has a foreign key to foo(other_id)
from django.apps import apps
BarModel = apps.get_model('bar')
assert BarModel._meta.get_field('other_id').remote_field.model.__name__ == 'foo' and \
       BarModel._meta.get_field('other_id').remote_field.field_name == 'other_id', "Foreign key to a specific field is not handled in inspectdb"

print("Issue fixed!")
sys.exit(0)
```
This script creates a test database, creates the tables manually, runs `inspectdb` to generate the models, and then checks if the generated model for `bar` has a foreign key to `foo(other_id)`. If the issue is present, it raises an `AssertionError` with a stack trace. If the issue is fixed, it prints "Issue fixed!" and exits with code 0.